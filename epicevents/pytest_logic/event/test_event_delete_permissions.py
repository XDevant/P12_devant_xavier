import pytest
from pytest_logic.fake_logs import user_logs


@pytest.mark.django_db
class TestEventDelete:
    @pytest.mark.parametrize("user", [pytest.param(user_logs[i]) for i in range(6)])
    def test_do_not_delete_event(self, api_client, user):
        username, password = user
        api_client.login(username=username, password=password)
        response = api_client.delete('http://127.0.0.1:8000/events/1/')
        assert response.status_code == 403
