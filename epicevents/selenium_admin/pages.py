from selenium.webdriver.common.by import By
import pages_data
from abstract_pages import BasePage, PkPage, SearchPage


class LoginPage(BasePage):
    """Login page data and action methods come here."""
    def __init__(self, driver, data=pages_data.LoginData):
        super().__init__(driver, data)
        self.super_form = data.super_form

    def submit_form(self):
        submit = self.driver.find_element(By.ID, 'id_username')
        submit.submit()

    def log_user(self, superuser=False):
        if superuser:
            self.fill_form(self.super_form)
        else:
            self.fill_form()
        self.submit_form()


class LogoutPage(BasePage):
    def __init__(self, driver, data=pages_data.LogoutData):
        super().__init__(driver, data)


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
    def __init__(self, driver, data=None, pk=-1):
        if data is None:
            data = pages_data.ChangeUserData(pk=pk)
        super().__init__(driver, data)


class ConfirmationPage(BasePage):
    def __init__(self, driver, app_name, model, data=pages_data.ConfirmationData):
        super().__init__(driver, data)
        self.url += app_name + '/' + model + '/'

    def confirm_delete(self):
        selector = (By.CSS_SELECTOR, "input[value='Yes, I’m sure']")
        confirm_input = self.driver.find_element(*selector)
        confirm_input.click()


class ItemPage(SearchPage):
    def __init__(self, driver, model, data=None):
        if data is None:
            data = pages_data.ItemData(model)
        super().__init__(driver, data)


class AddItemPage(PkPage):
    def __init__(self, driver, model, data=None):
        if data is None:
            data = pages_data.AddItemData(model)
        super().__init__(driver, data)


class ChangeItemPage(PkPage):
    def __init__(self, driver, model, data=None, pk=-1):
        if data is None:
            data = pages_data.ChangeItemData(model, pk=pk)
        super().__init__(driver, data)
