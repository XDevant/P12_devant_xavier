import pytest
from copy import deepcopy
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
        assert len(Contract.objects.all()) == 8

    def test_client_create_update(self, prospects):
        prospect = prospects[0]
        client = Client.objects.get(id=1)
        prospect["client"] = client
        contract = Contract.objects.create(**prospect)
        assert contract.amount == prospect['amount']
        contract_id = contract.id
        assert contract.client == client
        assert contract.sales_contact == client.sales_contact
        assert contract.payment_due == prospect['payment_due']
        assert contract.date_updated is None
        assert not contract._state.adding
        print(f"\nChecking if un updated contract {contract} "
              f"was created with correct data. Amount:{contract.amount}$",
              end='')
        contract.amount = 6789.
        contract.save()
        assert contract.date_updated is not None
        new_contract = Contract.objects.get(id=contract_id)
        assert new_contract.amount == 6789.
        print(f" And if {contract} was updated with new amount: "
              f"{new_contract.amount}$. ", end='')
