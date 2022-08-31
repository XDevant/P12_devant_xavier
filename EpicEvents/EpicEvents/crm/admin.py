from django.contrib import admin
from .models import Client, Contract, Event
from .forms import ClientChangeForm, ContractChangeForm, EventChangeForm


class ClientAdmin(admin.ModelAdmin):
    form = ClientChangeForm
    list_display = ('first_name', 'last_name', 'email', 'phone', 'mobile', 'company_name', 'sales_contact')
    ordering = ('sales_contact', 'last_name')


class ContractAdmin(admin.ModelAdmin):
    form = ContractChangeForm
    list_display = ('sales_contact', 'client', 'status', 'amount', 'payment_due')


class EventAdmin(admin.ModelAdmin):
    form = EventChangeForm
    list_display = ('support_contact', 'client', 'event_status', 'attendees', 'event_date', 'notes')


admin.site.register(Client, ClientAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Event, EventAdmin)
