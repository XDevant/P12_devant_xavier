from selenium.webdriver.common.by import By
import pages_data
from abstract_pages import BasePage, PkPage, SearchPage


class LoginPage(BasePage):
    """Login page data and action methods come here."""
    def __init__(self, driver, data=pages_data.LoginData):
        super().__init__(driver, data)

    def submit_form(self):
        submit = self.driver.find_element(By.ID, 'id_username')
        submit.submit()


class HomePage(BasePage):
    """Home page action methods come here"""
    def __init__(self, driver, data=pages_data.HomeData):
        super().__init__(driver, data)


class UserPage(SearchPage):
    def __init__(self, driver, data=pages_data.UserData):
        super().__init__(driver, data)


class AddUserPage(BasePage):
    def __init__(self, driver, data=pages_data.AddUserData):
        super().__init__(driver, data)


class ChangeUserPage(PkPage):
    def __init__(self, driver, data=pages_data.ChangeUserData):
        super().__init__(driver, data)
