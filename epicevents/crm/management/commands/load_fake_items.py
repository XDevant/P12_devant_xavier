from django.core.management.base import BaseCommand
from authentication.models import User
import crm.fixtures.test_data as data
from crm.models import Client, Contract, Event


class Command(BaseCommand):
    help = 'load fake data for testing, 2 clients, 2 contracts, 2 events'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        sales_list = User.objects.filter(role="sales")
        support_list = User.objects.filter(role="support")
        for client, contract, event in zip(data.test_clients, data.test_contracts, data.test_events):
            client_index = client["sales_contact"] % len(sales_list)
            client["sales_contact"] = sales_list[client_index]
            new_client = Client.objects.create(**client)

            contract["sales_contact"] = sales_list[client_index]
            contract["client"] = new_client
            new_contract = Contract.objects.create(**contract)

            event["support_contact"] = support_list[client_index]
            event["client"] = new_client
            event["event_status"] = new_contract
            Event.objects.create(**event)
