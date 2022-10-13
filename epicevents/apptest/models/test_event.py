import pytest
from copy import deepcopy
from django.db.utils import IntegrityError
from authentication.models import User
from crm.models import Contract, Event, EventStatus
from crm.fixtures.test_data import test_events


@pytest.fixture
def prospects():
    events = deepcopy(test_events)
    return events


@pytest.mark.django_db
class TestEventModel:
    @pytest.mark.parametrize("index", range(1, 5))
    def test_event_i_was_created(self, index, prospects):
        assert len(EventStatus.objects.all()) == len(Event.objects.all())
        event = Event.objects.get(id=index)
        notes = prospects[index - 1]['notes']
        print(f"\nChecking if event {event} notes={event.notes} matches"
              f" loaded fixture {index} notes={notes}.  ",
              end='')
        assert event.notes == notes
        assert len(Event.objects.all()) == 4

    def test_event_create_and_unicity(self, prospects):
        contact = User.objects.filter(role='support')[0]
        prospect = prospects[0]
        prospect["support_contact"] = contact
        contract = Contract.objects.get(id=2, status=False)
        contract.status = True
        status = EventStatus.objects.create(contract=contract)
        prospect["event_status"] = status
        prospect["client"] = contract.client
        event = Event.objects.create(**prospect)
        assert event.support_contact == contact
        assert event.client == contract.client
        assert status.contract.status
        print("\nEvent was created with success. ", end='')
        assert len(EventStatus.objects.all()) == len(Event.objects.all())
        prospect["attendees"] = 1234
        with pytest.raises(IntegrityError):
            Event.objects.create(**prospect)
        print("\nAnd same contract does not accept a second event. ", end='')

    def test_event_update(self):
        event = Event.objects.get(id=1)
        assert event.attendees != 1234
        event.attendees = 1234
        event.save()
        assert not event._state.adding
        assert event.attendees == 1234

    def test_event_deletion(self):
        event = Event.objects.get(id=1)
        new = deepcopy(event)
        status = new.event_status
        contract = status.contract
        assert contract.status
        event.delete()
        assert len(EventStatus.objects.all()) == len(Event.objects.all())
        contract = Contract.objects.get(id=status.contract.id)
        assert not contract.status
        assert len(EventStatus.objects.filter(contract=contract)) == 0
