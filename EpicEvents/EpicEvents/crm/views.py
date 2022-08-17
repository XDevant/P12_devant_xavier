from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from .models import Client, Contract, Event
from .serializers import ClientSerializerSelector, ContractSerializerSelector, EventSerializerSelector
from .permissions import IsSaleContactOrReadOnly, IsInChargeOrReadOnly
from ..authentication.models import User


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
    permission_classes = [IsAuthenticated, IsSaleContactOrReadOnly]
    queryset = Client.objects.all()

    def perform_create(self, serializer):
        """
        We set the user as sales_contact while saving the new client
        """
        current_user = self.request.user
        client = serializer.save(sales_contact=current_user)

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
        user_events = Event.objects.filter(support_contact=user)
        user_client_ids = [event.client.id for event in user_events]
        if isinstance(user, User):
            if user_groups.filter(name='admin').exists() or user.is_superuser:
                return queryset
            elif user_groups.filter(name='sales').exists():
                return queryset.filter(sales_contact=user)
            elif user_groups.filter(name='support').exists():
                return queryset.filter(id__in=user_client_ids)
        return None


class ContractViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ContractSerializerSelector.list
    multi_serializer_class = ContractSerializerSelector
    permission_classes = [IsAuthenticated, IsSaleContactOrReadOnly]
    queryset = Contract.objects.all()


class EventViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = EventSerializerSelector.list
    multi_serializer_class = EventSerializerSelector
    permission_classes = [IsAuthenticated, IsInChargeOrReadOnly]
    queryset = Event.objects.all()
