from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.serializers import ValidationError
from datetime import datetime
from .models import Client, Contract, Event, Status
from .serializers import ClientSerializerSelector, ContractSerializerSelector, EventSerializerSelector
from .permissions import IsSaleContactCRUOrSupportContactReadOnly, IsSaleContactCRU, IsInChargeOrReadOnly
from authentication.models import User


class MultipleSerializerMixin:
    serializer_class = None
    multi_serializer_class = None
    detail = False

    def get_serializer_class(self):
        if self.multi_serializer_class is not None and self.detail:
            return self.multi_serializer_class.detail
        return self.serializer_class


class ClientViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ClientSerializerSelector.list
    multi_serializer_class = ClientSerializerSelector
    permission_classes = [DjangoModelPermissions, IsSaleContactCRUOrSupportContactReadOnly]
    queryset = Client.objects.all()
    filterset_fields = {'last_name': ['exact', 'icontains'], 'email': ['exact', 'icontains']}

    def perform_create(self, serializer):
        """
        We set the user as sales_contact while saving the new client
        """
        current_user = self.request.user
        serializer.save(sales_contact=current_user)

    def perform_update(self, serializer):
        serializer.save(date_updated=datetime.now())

    def partial_update(self, *args, **kwargs):
        """This method is not implemented"""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_queryset(self):
        """We filter the project list to show only the projects the user is
        contributor of."""
        queryset = super(ClientViewSet, self).get_queryset()
        user = self.request.user
        user_groups = getattr(user, 'groups')
        if isinstance(user, User):
            if user_groups.filter(name='admin').exists() or user.is_superuser:
                return queryset
            elif user_groups.filter(name='sales').exists():
                return queryset.filter(sales_contact=user)
            elif user_groups.filter(name='support').exists():
                user_events = Event.objects.filter(support_contact=user)
                user_client_ids = [event.client.id for event in user_events]
                return queryset.filter(id__in=user_client_ids)
        return User.objects.none()


class ContractViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ContractSerializerSelector.list
    multi_serializer_class = ContractSerializerSelector
    permission_classes = [DjangoModelPermissions, IsSaleContactCRU]
    queryset = Contract.objects.all()
    filterset_fields = {'client__last_name': ['exact', 'icontains'],
                        'client__email': ['exact', 'icontains'],
                        'date_created': ['exact', 'gt', 'lt'],
                        'amount': ['exact', 'gt', 'lt']}

    def perform_create(self, serializer):
        """
        We set the user as sales_contact while saving the new contract
        """
        current_user = self.request.user
        try:
            client_id = serializer.initial_data['client_id']
            client = Client.objects.get(id=client_id, sales_contact=self.request.user)
        except Exception:
            message = "Invalid client id"
            raise ValidationError(message)
        serializer.save(sales_contact=current_user, client=client, status=False)

    def perform_update(self, serializer):
        try:
            client_id = serializer.initial_data['client_id']
            client = Client.objects.get(id=client_id)
        except Exception:
            message = "Invalid client id"
            raise ValidationError(message)
        serializer.save(client=client, date_updated=datetime.today())

    def partial_update(self, *args, **kwargs):
        """This method is not implemented"""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_queryset(self):
        """We filter the project list to show only the contracts the user is
        contact of."""
        queryset = super(ContractViewSet, self).get_queryset()
        user = self.request.user
        user_groups = getattr(user, 'groups')
        if isinstance(user, User):
            if user_groups.filter(name='admin').exists() or user.is_superuser:
                return queryset
            else:
                return queryset.filter(sales_contact=user)


class EventViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = EventSerializerSelector.list
    multi_serializer_class = EventSerializerSelector
    permission_classes = [DjangoModelPermissions, IsInChargeOrReadOnly]
    queryset = Event.objects.all()
    filterset_fields = {'client__last_name': ['exact', 'icontains'],
                        'client__email': ['exact', 'icontains'],
                        'date_created': ['exact', 'gt', 'lt', 'range']}

    def perform_create(self, serializer):
        """
        We set the user as sales_contact while saving the new contract
        """
        try:
            contact_email = serializer.initial_data['contact_email']
            contact = User.objects.get(email=contact_email, role="support")
        except Exception:
            message = "Invalid support contact email, event contact must be a support team member"
            raise ValidationError(message)
        try:
            contract_id = serializer.initial_data['status']
            contract = Contract.objects.get(id=contract_id, sales_contact=self.request.user, status=False)
            client = contract.client
            contract.status = True
            assert client.sales_contact == self.request.user
            contract.save()
            event_status = Status.objects.create(contract=contract)
        except Exception:
            message = "Invalid contract id"
            raise ValidationError(message)
        serializer.save(support_contact=contact, client=client, event_status=event_status)

    def perform_update(self, serializer):
        old_event = Event.objects.get(id=serializer.initial_data['id'])
        try:
            contact_email = serializer.initial_data['contact_email']
            contact = User.objects.get(email=contact_email)
            assert contact == self.request.user or self.request.user.groups.filter(name='admin').exists()
        except Exception:
            message = "Invalid support contact email"
            raise ValidationError(message)
        try:
            client_id = serializer.initial_data['client_id']
            client = Client.objects.get(id=client_id)
            assert client == old_event.client
        except Exception:
            message = "Invalid client id"
            raise ValidationError(message)

        serializer.save(support_contact=contact, client=client, date_updated=datetime.today())

    def partial_update(self, *args, **kwargs):
        """This method is not implemented"""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_queryset(self):
        """We filter the project list to show only the events the user is
        contact of."""
        queryset = super(EventViewSet, self).get_queryset()
        user = self.request.user
        user_groups = getattr(user, 'groups')
        if isinstance(user, User):
            if user_groups.filter(name='admin').exists() or user.is_superuser:
                return queryset
            elif user_groups.filter(name='sales').exists():
                return queryset.filter(client__sales_contact=user)
            elif user_groups.filter(name='support').exists():
                return queryset.filter(support_contact=user)
        return User.objects.none()
