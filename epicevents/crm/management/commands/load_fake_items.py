from django.core.management.base import BaseCommand
from authentication.models import User, UserManager
import crm.fixtures.test_data as data
from crm.models import Client, Contract, Event


class Command(BaseCommand):
    help = 'load fake data for testing, 2 clients, 2 contracts, 2 events'

    def add_arguments(self, parser):
        help_1 = 'Loads the data in the test_db template but not in default db'
        parser.add_argument('-c', '--copy', action='store_true', help=help_1)

    def handle(self, *args, **options):
        client_count = 0
        contract_count = 0
        event_count = 0
        if options["copy"]:
            db = "copy"
        else:
            db = "default"
        sales_list = User.objects.db_manager(db).filter(role="sales")
        support_list = User.objects.db_manager(db).filter(role="support")

        for client, contract, event in zip(data.test_clients, data.test_contracts, data.test_events):
            client_index = client["sales_contact"] % len(sales_list)
            client["sales_contact"] = sales_list[client_index]
            new_client = Client.objects.db_manager(db).create(**client)
            client_count += 1

            contract["sales_contact"] = sales_list[client_index]
            contract["client"] = new_client
            new_contract = Contract.objects.db_manager(db).create(**contract)
            contract_count += 1

            event["support_contact"] = support_list[client_index]
            event["client"] = new_client
            event["event_status"] = new_contract
            Event.objects.db_manager(db).create(**event)
            event_count += 1
        print(f"{client_count} clients created",
              f"{contract_count} contracts created",
              f"{event_count} events created")
