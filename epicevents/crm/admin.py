from django.contrib import admin
from .models import Client, Contract, Event
from .forms import ClientAddForm, ClientChangeForm, ContractAddForm,\
                   ContractChangeForm, EventAddForm, EventChangeForm


class ClientAdmin(admin.ModelAdmin):
    add_form = ClientAddForm
    form = ClientChangeForm

    list_display = ('first_name', 'last_name', 'email', 'phone', 'mobile', 'company_name', 'sales_contact')
    ordering = ('sales_contact', 'last_name')


class ContractAdmin(admin.ModelAdmin):
    add_form = ContractAddForm
    form = ContractChangeForm

    list_display = ('sales_contact', 'client', 'status', 'amount', 'payment_due')

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)


class EventAdmin(admin.ModelAdmin):
    add_form = EventAddForm
    form = EventChangeForm

    list_display = ('support_contact', 'client', 'event_status', 'attendees', 'event_date', 'notes')

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)


admin.site.register(Client, ClientAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Event, EventAdmin)
