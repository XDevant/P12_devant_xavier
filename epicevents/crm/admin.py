from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Client, Contract, Event, EventStatus
from authentication.models import User
from .forms import ClientAddForm, ClientChangeForm, ContractAddForm,\
                   ContractChangeForm, EventAddForm, EventChangeForm


class ClientAdmin(admin.ModelAdmin):
    add_form = ClientAddForm
    form = ClientChangeForm

    list_display = ('first_name', 'last_name', 'email', 'phone', 'mobile', 'company_name', 'sales_contact')
    ordering = ('sales_contact', 'last_name')
    actions = ['change_contact']

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    @admin.action(
        description='Change clients sales contact',
        permissions=['change'])
    def change_contact(self, request, queryset):
        sales_team = User.objects.filter(role='sales')
        context = dict(self.admin_site.each_context(request))
        if 'apply' in request.POST:
            new_contact_id = request.POST["sales_contact"]
            queryset.update(sales_contact=new_contact_id)
            self.message_user(request,
                              f"Changed sales contact for {queryset.count()} clients.")
            contract = Contract.objects.filter(client__in=queryset)
            contract.update(sales_contact=new_contact_id)

            self.message_user(request,
                              f"Changed sales contact for {contract.count()} contracts.")
            return HttpResponseRedirect(request.get_full_path())
        context['clients'] = queryset
        context['sales_contacts'] = sales_team
        return render(request,
                      'admin/crm/clients/contact.html',
                      context=context)


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
    actions = ['change_contact']

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    @admin.action(
        description='Change events support contact',
        permissions=['change'])
    def change_contact(self, request, queryset):
        support_team = User.objects.filter(role='support')
        context = dict(self.admin_site.each_context(request))
        if 'apply' in request.POST:
            new_contact_id = request.POST["support_contact"]
            queryset.update(support_contact=new_contact_id)
            self.message_user(request,
                              f"Changed support contact for {queryset.count()} events.")
            return HttpResponseRedirect(request.get_full_path())
        context['events'] = queryset
        context['support_contacts'] = support_team
        return render(request,
                      'admin/crm/events/contact.html',
                      context=context)


admin.site.register(Client, ClientAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventStatus)