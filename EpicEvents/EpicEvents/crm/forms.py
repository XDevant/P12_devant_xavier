from django import forms
from .models import Client, Contract, Event


class ClientChangeForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'email', 'phone', 'mobile', 'company_name', 'sales_contact')
        read_only_fields = ('date_created', 'date_updated')


class ContractChangeForm(forms.ModelForm):

    class Meta:
        model = Contract
        fields = ('sales_contact', 'client', 'status', 'amount', 'payment_due')
        read_only_fields = ('date_created', )


class EventChangeForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('support_contact', 'client', 'event_status', 'attendees', 'event_date', 'notes')
        read_only_fields = ('date_created', 'date_updated', )
