import pytest
from copy import deepcopy
from django.db.models import ProtectedError
from authentication.models import User
from authentication.fixtures.fake_users import test_users
from crm.models import Client


@pytest.fixture
def prospects():
    users = deepcopy(test_users)
    return users


@pytest.mark.django_db
class TestUserModel:
    @pytest.mark.parametrize("index", range(1, 6))
    def test_user_i_was_created(self, index, prospects):
        user = User.objects.get(id=index)
        email = prospects[index - 1]['email']
        assert user.email == email

    def test_roles(self):
        assert 6 <= len(User.objects.all())
        assert len(User.objects.filter(role='sales')) >= 2
        assert len(User.objects.filter(role='support')) >= 2
        assert len(User.objects.filter(role='admin')) >= 1
        assert len(User.objects.filter(role='none')) >= 1

    def test_crm_model_protect(self):
        user = User.objects.get(id=1)
        assert len(Client.objects.filter(sales_contact=user)) > 0
        with pytest.raises(ProtectedError):
            user.delete()
