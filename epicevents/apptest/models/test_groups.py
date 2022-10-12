import pytest
from django.contrib.auth.models import Group
from authentication.models import User, UserManager


@pytest.mark.django_db
class TestGroups:
    @pytest.mark.parametrize("group, nb_perms", [('admin', 10),
                                                 ('sales', 8),
                                                 ('support', 3),
                                                 ('visitor', 0)])
    def test_groups(self, group, nb_perms):
        assert Group.objects.filter(name=group).exists()
        group = Group.objects.get(name=group)
        permissions = group.permissions.all()
        assert len(permissions) == nb_perms

    def test_user_groups(self):
        for user in User.objects.all():
            assert Group.objects.filter(user=user.id).exists()
            if user.role != 'none':
                assert Group.objects.filter(user=user.id,
                                            name=user.role
                                            ).exists()
