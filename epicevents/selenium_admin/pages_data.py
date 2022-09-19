class BaseData:
    url = ""
    title = ""
    form = {}
    search = ""
    super_form = {}
    pk = 0


class LoginData(BaseData):
    url = "http://127.0.0.1:8000/admin/login/?next=/admin/"
    title = "Log in | Django site admin"
    form = {"username": "za@za.co", "password": "mdp5"}
    super_form = {"username": "super@user.co", "password": "supermdp"}


class LogoutData(BaseData):
    url = "http://127.0.0.1:8000/admin/logout/"
    title = "Logged out | Django site admin"


class HomeData(BaseData):
    url = "http://127.0.0.1:8000/admin/"
    title = "Site administration | Django site admin"


class UserData(BaseData):
    url = "http://127.0.0.1:8000/admin/authentication/user/"
    title = "Select user to change | Django site admin"
    search = "ma@la.co"


class AddUserData(BaseData):
    url = "http://127.0.0.1:8000/admin/authentication/user/add/"
    title = "Add user | Django site admin"
    form = {"first_name": "Mi", "last_name": "Lou", "email": "mi@lou.co", "role": "support"}


class ChangeUserData(BaseData):
    title = "Change user | Django site admin"
    form = {"first_name": "Ma", "last_name": "La", "email": "ma@la.co", "role": "support"}
    url = "http://127.0.0.1:8000/admin/authentication/user/$pk$/change/"

    def __init__(self, pk=-1):
        self.pk = pk


class ConfirmationData(BaseData):
    url = "http://127.0.0.1:8000/admin/"
    title = "Are you sure? | Django site admin"


class ItemData(BaseData):
    _item_search = {"client": "", "contract": "", "event": ""}
    url = "http://127.0.0.1:8000/admin/crm/"

    def __init__(self, model):
        self.url += model + '/'
        self.search = self._item_search[model]
        self.title = f"Select {model} to change | Django site admin"


class AddItemData(BaseData):
    _client_form = {}
    _contract_form = {}
    _event_form = {}
    _item_form = {"client": _client_form, "contract": _contract_form, "event": _event_form}
    url = "http://127.0.0.1:8000/admin/crm/"

    def __init__(self, model):
        self.url += f"{model}/add/"
        self.title = f"Add {model} | Django site admin"
        self.form = self._item_form[model]


class ChangeItemData(BaseData):
    _client_form = {}
    _contract_form = {}
    _event_form = {}
    _item_form = {"client": _client_form, "contract": _contract_form, "event": _event_form}
    url = "http://127.0.0.1:8000/admin/crm/"

    def __init__(self, model, pk=-1):
        self.url += f"{model}/$pk$/change/"
        self.title = f"Change {model} | Django site admin"
        self.form = self._item_form[model]
        self.pk = pk
