
class LoginData:
    url = "http://127.0.0.1:8000/admin/login/?next=/admin/"
    title = "Log in | Django site admin"
    form = {"username": "za@za.co", "password": "mdp5"}


class HomeData:
    url = "http://127.0.0.1:8000/admin/"
    title = "Site administration | Django site admin"
    form = {}


class UserData:
    url = "http://127.0.0.1:8000/admin/authentication/user/"
    title = "Select user to change | Django site admin"
    form = {}
    search = "ma@la.co"


class AddUserData:
    url = "http://127.0.0.1:8000/admin/authentication/user/add/"
    title = "Add user | Django site admin"
    form = {"first_name": "Mi", "last_name": "Lou", "email": "mi@lou.co", "role": "support"}


class ChangeUserData:
    url = ""
    title = "Change user | Django site admin"
    form = {"first_name": "Ma", "last_name": "La", "email": "ma@la.co", "role": "support"}
    url_start = "http://127.0.0.1:8000/admin/authentication/user/"
    url_end = "/change/"
    pk = 0
