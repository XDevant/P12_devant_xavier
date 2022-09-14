from rest_framework.test import APITestCase


class TestSalesContract(APITestCase):

    def test_contracts_url(self):
        self.client.login(username="de@de.co", password="mdp1")
        response = self.client.get('http://127.0.0.1:8000/contracts/')
        assert response.status_code == 200

    def test_contract_1_url(self):
        self.client.login(username="de@de.co", password="mdp1")
        response = self.client.get('http://127.0.0.1:8000/contracts/1/')
        assert response.status_code == 200

    def test_contract_2_url(self):
        self.client.login(username="de@de.co", password="mdp1")
        response = self.client.get('http://127.0.0.1:8000/contracts/2/')
        assert response.status_code == 404

    def test_contract_2_sale_2_url(self):
        self.client.login(username="do@do.co", password="mdp2")
        response = self.client.get('http://127.0.0.1:8000/contracts/2/')
        assert response.status_code == 200

    def test_contract_1_sale_2_url(self):
        self.client.login(username="do@do.co", password="mdp2")
        response = self.client.get('http://127.0.0.1:8000/contracts/1/')
        assert response.status_code == 404


class TestSupportContract(APITestCase):
    def test_contracts_url(self):
        self.client.login(username="bi@bi.co", password="mdp3")
        response = self.client.get('http://127.0.0.1:8000/contracts/')
        assert response.status_code == 200

    def test_contract_1_url(self):
        self.client.login(username="bi@bi.co", password="mdp3")
        response = self.client.get('http://127.0.0.1:8000/contracts/1/')
        assert response.status_code == 404

    def test_contract_2_url(self):
        self.client.login(username="bi@bi.co", password="mdp3")
        response = self.client.get('http://127.0.0.1:8000/contracts/2/')
        assert response.status_code == 404

    def test_contract_2_support_2_url(self):
        self.client.login(username="bo@bo.co", password="mdp4")
        response = self.client.get('http://127.0.0.1:8000/contracts/2/')
        assert response.status_code == 404

    def test_contract_1_support_2_url(self):
        self.client.login(username="bo@bo.co", password="mdp4")
        response = self.client.get('http://127.0.0.1:8000/contracts/1/')
        assert response.status_code == 404
