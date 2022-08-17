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

    class Meta:
        model = Contract
        fields = ['id', 'contact']
        read_only_fields = ['contact']


class ContractDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['id', 'contact']
        read_only_fields = ['contact']


class ContractSerializerSelector:
    """Import container for the view, and it's get_serializer method"""
    list = ContractListSerializer
    detail = ContractDetailSerializer


class EventListSerializer(serializers.ModelSerializer):
    """"""
    contact = serializers.StringRelatedField(source='sales_contact')

    class Meta:
        model = Event
        fields = ['id', 'contact']
        read_only_fields = ['contact']


class EventDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'contact']
        read_only_fields = ['contact']


class EventSerializerSelector:
    """Import container for the view, and it's get_serializer method"""
    list = EventListSerializer
    detail = EventDetailSerializer
