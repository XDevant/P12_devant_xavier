from rest_framework.test import APITestCase


class TestSalesEvent(APITestCase):

    def test_events_url(self):
        self.client.login(username="de@de.co", password="mdp1")
        response = self.client.get('http://127.0.0.1:8000/events/')
        assert response.status_code == 200

    def test_event_1_url(self):
        self.client.login(username="de@de.co", password="mdp1")
        response = self.client.get('http://127.0.0.1:8000/events/1/')
        assert response.status_code == 200

    def test_event_2_url(self):
        self.client.login(username="de@de.co", password="mdp1")
        response = self.client.get('http://127.0.0.1:8000/events/2/')
        assert response.status_code == 404

    def test_event_2_sale_2_url(self):
        self.client.login(username="do@do.co", password="mdp2")
        response = self.client.get('http://127.0.0.1:8000/events/2/')
        assert response.status_code == 200

    def test_event_1_sale_2_url(self):
        self.client.login(username="do@do.co", password="mdp2")
        response = self.client.get('http://127.0.0.1:8000/events/1/')
        assert response.status_code == 404


class TestSupportEvent(APITestCase):
    def test_events_url(self):
        self.client.login(username="bi@bi.co", password="mdp3")
        response = self.client.get('http://127.0.0.1:8000/events/')
        assert response.status_code == 200

    def test_event_1_url(self):
        self.client.login(username="bi@bi.co", password="mdp3")
        response = self.client.get('http://127.0.0.1:8000/events/1/')
        assert response.status_code == 200

    def test_event_2_url(self):
        self.client.login(username="bi@bi.co", password="mdp3")
        response = self.client.get('http://127.0.0.1:8000/events/2/')
        assert response.status_code == 404

    def test_event_2_support_2_url(self):
        self.client.login(username="bo@bo.co", password="mdp4")
        response = self.client.get('http://127.0.0.1:8000/events/2/')
        assert response.status_code == 200

    def test_event_1_support_2_url(self):
        self.client.login(username="bo@bo.co", password="mdp4")
        response = self.client.get('http://127.0.0.1:8000/events/1/')
        assert response.status_code == 404
