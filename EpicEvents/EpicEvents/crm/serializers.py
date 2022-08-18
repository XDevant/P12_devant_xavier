from rest_framework import serializers
from .models import Client, Contract, Event


class ClientListSerializer(serializers.ModelSerializer):
    """"""
    contact = serializers.StringRelatedField(source='sales_contact')

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'mobile', 'company_name', 'date_created',
                  'contact']
        read_only_fields = ['date_created', 'contact']


class ClientDetailSerializer(serializers.ModelSerializer):
    contact = serializers.StringRelatedField(source='sales_contact')

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'mobile', 'company_name', 'date_created',
                  'date_updated', 'contact']
        read_only_fields = ['date_created', 'contact']


class ClientSerializerSelector:
    """Import container for the view, and it's get_serializer method"""
    list = ClientListSerializer
    detail = ClientDetailSerializer


class ContractListSerializer(serializers.ModelSerializer):
    """"""
    contact = serializers.StringRelatedField(source='sales_contact')
    client_id = serializers.CharField(source='client')

    class Meta:
        model = Contract
        fields = ['id', 'contact', 'client_id', 'date_created', 'status', 'amount', 'payment_due']
        read_only_fields = ['contact', 'date_created']


class ContractDetailSerializer(serializers.ModelSerializer):
    contact = serializers.StringRelatedField(source='sales_contact')
    client_id = serializers.CharField(source='client')

    class Meta:
        model = Contract
        fields = ['id', 'contact', 'client_id', 'date_created', 'date_updated', 'status', 'amount', 'payment_due']
        read_only_fields = ['contact', 'date_created', 'date_updated']


class ContractSerializerSelector:
    """Import container for the view, and it's get_serializer method"""
    list = ContractListSerializer
    detail = ContractDetailSerializer


class EventListSerializer(serializers.ModelSerializer):
    """"""
    contact = serializers.StringRelatedField(source='support_contact')
    related_client = serializers.StringRelatedField(source='client')

    class Meta:
        model = Event
        fields = ['id', 'contact', 'related_client', 'date_created', ]
        read_only_fields = ['contact', 'related_client', 'date_created']


class EventDetailSerializer(serializers.ModelSerializer):
    contact = serializers.StringRelatedField(source='support_contact')
    related_client = serializers.StringRelatedField(source='client')
    related_contract = serializers.StringRelatedField(source='event_status')

    class Meta:
        model = Event
        fields = ['id', 'contact', 'related_client', 'related_contract', 'date_created',
                  'date_updated', 'attendees', 'event_date', 'notes']
        read_only_fields = ['contact', 'related_client', 'date_created', 'date_updated']


class EventSerializerSelector:
    """Import container for the view, and it's get_serializer method"""
    list = EventListSerializer
    detail = EventDetailSerializer
