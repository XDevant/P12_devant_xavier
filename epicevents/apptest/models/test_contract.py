import pytest
from copy import deepcopy
from django.db.utils import IntegrityError
from authentication.models import User, UserManager
from crm.models import Client, Contract
from crm.fixtures.test_data import test_contracts


@pytest.fixture
def prospects():
    contracts = deepcopy(test_contracts)
    return contracts


@pytest.mark.django_db
class TestClientModel:
    @pytest.mark.parametrize("index", range(8))
    def test_client_i_was_created(self, index, prospects):
        amount = prospects[index]['amount']
        contract = Contract.objects.get(amount=amount)
        print(f"\nChecking if contract {contract.id} amount={contract.amount} matches"
              f" loaded fixture {index} amount={amount}.  ",
              end='')
        assert contract.amount == amount
