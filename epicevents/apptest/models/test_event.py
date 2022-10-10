import pytest
from copy import deepcopy
from django.db.utils import IntegrityError
from authentication.models import User, UserManager
from crm.models import Client, Contract, Event
from crm.fixtures.test_data import test_events


@pytest.fixture
def prospects():
    events = deepcopy(test_events)
    return events


@pytest.mark.django_db
class TestClientModel:
    @pytest.mark.parametrize("index", range(1, 5))
    def test_client_i_was_created(self, index, prospects):
        event = Event.objects.get(id=index)
        notes = prospects[index - 1]['notes']
        print(f"\nChecking if event {event} notes={event.notes} matches"
              f" loaded fixture {index} notes={notes}.  ",
              end='')
        assert event.notes == notes
        assert len(Event.objects.all()) == 4

    def test_client_create_update(self, prospects):
        contact = User.objects.filter(role='support')[0]
        prospect = prospects[0]
        prospect["support_contact"] = contact
        prospect.pop("client", None)
        event = Event.objects.create(**prospect)
        assert event.support_contact == contact
