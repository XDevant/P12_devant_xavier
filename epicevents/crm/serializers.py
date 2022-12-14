from rest_framework import serializers
from .models import Client, Contract, Event


class ClientListSerializer(serializers.ModelSerializer):
    """"""
    contact = serializers.StringRelatedField(source='sales_contact')

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'mobile',
                  'company_name', 'contact', 'date_created']
        read_only_fields = ['date_created', 'contact']


class ClientDetailSerializer(serializers.ModelSerializer):
    contact = serializers.StringRelatedField(source='sales_contact')

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'mobile',
                  'company_name', 'contact', 'date_created', 'date_updated']
        read_only_fields = ['contact', 'date_created', 'date_updated']


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
        fields = ['id', 'client_id', 'status', 'contact',
                  'amount', 'payment_due', 'date_created']
        read_only_fields = ['status', 'contact', 'date_created']


class ContractDetailSerializer(ContractListSerializer):

    class Meta:
        model = Contract
        fields = ['id', 'client', 'status', 'contact', 'amount',
                  'payment_due', 'date_created', 'date_updated']
        read_only_fields = ['client', 'status', 'contact', 'date_created',
                            'date_updated']


class ContractSerializerSelector:
    """Import container for the view, and it's get_serializer method"""
    list = ContractListSerializer
    detail = ContractDetailSerializer


class EventListSerializer(serializers.ModelSerializer):
    """"""
    contact = serializers.StringRelatedField(source='support_contact')
    status = serializers.StringRelatedField(source='event_status')

    class Meta:
        model = Event
        fields = ['id', 'client', 'status', 'contact',
                  'attendees', 'event_date', 'notes', 'date_created']
        read_only_fields = ['client', 'status', 'contact', 'date_created']


class EventDetailSerializer(EventListSerializer):

    class Meta:
        model = Event
        fields = ['id', 'client', 'status', 'contact', 'attendees',
                  'event_date', 'notes', 'date_created', 'date_updated']
        read_only_fields = ['client', 'status', 'contact',
                            'date_created', 'date_updated']


class EventSerializerSelector:
    """Import container for the view, and it's get_serializer method"""
    list = EventListSerializer
    detail = EventDetailSerializer
