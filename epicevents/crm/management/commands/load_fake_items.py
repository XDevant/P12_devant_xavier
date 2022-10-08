from django.core.management.base import BaseCommand
from authentication.models import User, UserManager
import crm.fixtures.test_data as data
from crm.models import Client, Contract, Event, Status
from utils.prettyprints import PRR


class Command(BaseCommand):
    help = 'load fake data for testing, 4 clients, 8 contracts, 4 events'

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

        for client, contract, event, contract_2 in zip(data.test_clients,
                                                       data.test_contracts[:4],
                                                       data.test_events,
                                                       data.test_contracts[4:]):
            client_index = client["sales_contact"] % len(sales_list)
            client["sales_contact"] = sales_list[client_index]
            new_client = Client.objects.db_manager(db).create(**client)
            client_count += 1

            contract["sales_contact"] = sales_list[client_index]
            contract["client"] = new_client
            contract["status"] = True
            c = Contract.objects.db_manager(db).create(**contract)
            s = Status.objects.db_manager(db).create(contract=c)
            contract_count += 1

            contract_2["sales_contact"] = sales_list[client_index]
            contract_2["client"] = new_client
            c = Contract.objects.db_manager(db).create(**contract_2)
            Status.objects.db_manager(db).create(contract=c)
            contract_count += 1

            event["support_contact"] = support_list[client_index]
            event["client"] = new_client
            event["event_status"] = s
            Event.objects.db_manager(db).create(**event)
            event_count += 1

        clients = PRR.colorize(f"{client_count}/4", client_count == 4)
        clients += " clients created, "
        contracts = PRR.colorize(f"{contract_count}/8", contract_count == 8)
        contracts += " contracts created, "
        events = PRR.colorize(f"{event_count}/4", event_count == 4)
        events += " events created."
        print(clients + contracts + events)
