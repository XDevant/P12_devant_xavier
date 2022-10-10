from django import forms
from django.db import transaction
from .models import Client, Contract, Event, Status
from authentication.models import User


class ClientAddForm(forms.ModelForm):
    sales_contact = forms.ModelChoiceField(queryset=User.objects.filter(role='sales'))

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'email', 'phone', 'mobile', 'company_name', 'sales_contact')


class ClientChangeForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'email', 'phone', 'mobile', 'company_name')


class ContractAddForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ('client', 'amount', 'payment_due')
        read_only_fields = ('client',)


class ContractChangeForm(forms.ModelForm):

    class Meta:
        model = Contract
        fields = ('amount', 'payment_due')


class EventAddForm(forms.ModelForm):
    contract = forms.ModelChoiceField(queryset=Contract.objects.filter(status=False))
    support_contact = forms.ModelChoiceField(queryset=User.objects.filter(role='support'))

    class Meta:
        model = Event
        fields = ('support_contact', 'contract', 'attendees', 'event_date', 'notes')

    @transaction.atomic()
    def save(self, commit=True):
        contract = Contract.objects.get(id=self.data['contract'])
        contract.status = True
        contract.save()
        event = super().save(commit=False)
        event.client = contract.client
        event.event_status = Status.objects.create(contract=contract)
        if commit:
            event.save()
        return event


class EventChangeForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('attendees', 'event_date', 'notes')
