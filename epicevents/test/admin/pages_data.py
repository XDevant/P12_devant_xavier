BASE_URL = "http://127.0.0.1:8000/"
SLEEP_TIME = 0


class BaseData:
    url = ""
    title = ""
    form = {}
    search = ""
    pk = 0
    sleep_time = SLEEP_TIME


class LoginData(BaseData):
    url = BASE_URL + "admin/login/?next=/admin/"
    title = "Log in | Django site admin"


class LogoutData(BaseData):
    url = BASE_URL + "admin/logout/"
    title = "Logged out | Django site admin"


class HomeData(BaseData):
    url = BASE_URL + "admin/"
    title = "Site administration | Django site admin"


class UserData(BaseData):
    url = BASE_URL + "admin/authentication/user/"
    title = "Select user to change | Django site admin"
    search = "ma@la.co"


class AddUserData(BaseData):
    url = BASE_URL + "admin/authentication/user/add/"
    title = "Add user | Django site admin"
    form = {"first_name": "Mi", "last_name": "Lou", "email": "mi@lou.co", "role": "support"}


class ChangeUserData(BaseData):
    url = BASE_URL + "admin/authentication/user/$pk$/change/"
    title = "Change user | Django site admin"
    form = {"first_name": "Ma", "last_name": "La", "email": "ma@la.co", "role": "sales"}

    def __init__(self, pk=-1):
        self.pk = pk


class ConfirmationData(BaseData):
    url = BASE_URL + "admin/"
    title = "Are you sure? | Django site admin"

    def __init__(self, app, model):
        self.url += app + '/' + model + '/'


class ItemData(BaseData):
    _item_search = {"client": "third@client.co", "contract": "", "event": ""}
    url = BASE_URL + "admin/crm/"

    def __init__(self, model):
        self.url += model + '/'
        self.search = self._item_search[model]
        self.title = f"Select {model} to change | Django site admin"


class AddItemData(BaseData):
    _client_form = {"first_name":  "third",
                    "last_name":  "client",
                    "email":  "third@client.co",
                    "phone":  "01",
                    "mobile":  "08",
                    "company_name":  "World",
                    "sales_contact": "ma@la.co"}
    _contract_form = {"sales_contact": "ma@la.co",
                      "client":  1,
                      "status":  "False",
                      "amount":  25,
                      "payment_due_0":  "2022-08-17",
                      "payment_due_1":  "18:33:30"}
    _event_form = {"support_contact": "bi@bi.co",
                   "client":  1,
                   "event_status":  1,
                   "attendees":  25,
                   "event_date_0":  "2022-08-17",
                   "event_date_1": "18:33:30",
                   "notes": "bla"}
    _item_form = {"client": _client_form, "contract": _contract_form, "event": _event_form}
    url = BASE_URL + "admin/crm/"

    def __init__(self, model):
        self.url += f"{model}/add/"
        self.title = f"Add {model} | Django site admin"
        self.form = self._item_form[model]


class ChangeItemData(BaseData):
    _client_form = {"phone":  "01020304"}
    _contract_form = {"amount": 100}
    _event_form = {"notes": "selenium event"}
    _item_form = {"client": _client_form, "contract": _contract_form, "event": _event_form}
    url = BASE_URL + "admin/crm/"

    def __init__(self, model, pk=-1):
        self.url += f"{model}/$pk$/change/"
        self.title = f"Change {model} | Django site admin"
        self.form = self._item_form[model]
        self.pk = pk
