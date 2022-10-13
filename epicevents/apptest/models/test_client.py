import pytest
from copy import deepcopy
from django.db.utils import IntegrityError
from authentication.models import User
from crm.models import Client
from crm.fixtures.test_data import test_clients


@pytest.fixture
def prospects():
    clients = deepcopy(test_clients)
    return clients


@pytest.mark.django_db
class TestClientModel:
    @pytest.mark.parametrize("index", range(1, 5))
    def test_client_i_was_created(self, index, prospects):
        client = Client.objects.get(id=index)
        email = prospects[index - 1]['email']
        print(f"\nChecking if client {index} email={client.email} matches"
              f" loaded fixture {index} email={email}.  ",
              end='')
        assert client.email == email
        assert len(Client.objects.all()) == 4

    def test_client_create_update(self, prospects):
        contact = User.objects.filter(role='sales')[0]
        prospect = prospects[0]
        prospect["sales_contact"] = contact
        prospect["email"] = "old@email.test"
        prospect["first_name"] = "new_first_name"
        client = Client.objects.create(**prospect)
        assert client.email == "old@email.test"
        client_id = client.id
        assert client.date_updated is None
        assert not client._state.adding
        print(f"\nChecking if un updated client {client} "
              f"was created with old email. ",
              end='')
        client.email = "new@email.test"
        assert not client._state.adding
        client.save()
        assert client.date_updated is not None
        assert not client._state.adding
        new_client = Client.objects.get(id=client_id)
        assert new_client.email == "new@email.test"
        print(f" And if {client} was updated with new email.  ",
              end='')

    def test_client_create_email_unicity_failure(self, prospects):
        contact = User.objects.filter(role='sales')[0]
        prospect = prospects[0]
        prospect["sales_contact"] = contact
        print("\nChecking if creation of a client with"
              " already existing email raises Integrity error.  ",
              end='')
        with pytest.raises(IntegrityError):
            Client.objects.create(**prospect)

    def test_client_create_unique_together_failure(self, prospects):
        contact = User.objects.filter(role='sales')[0]
        prospect = prospects[0]
        prospect["sales_contact"] = contact
        prospect["email"] = "old@email.test"
        print("\nChecking if creation of a client with"
              " already existing names raises Integrity error.  ",
              end='')
        with pytest.raises(IntegrityError):
            Client.objects.create(**prospect)
