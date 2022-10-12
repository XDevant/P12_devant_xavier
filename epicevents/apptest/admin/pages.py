from selenium.webdriver.remote.errorhandler import NoSuchElementException
from . import pages_data
from .abstract_pages import BasePage, PkPage, ListPage, SearchPage
from .locators import ConfirmationPageLocator


class LoginPage(BasePage):
    """Login methods are BasePage methods to allow autolog from any page."""
    def __init__(self, driver, data=pages_data.LoginData):
        super().__init__(driver, data)

    def log_user(self, logs=None):
        self.get_page(logs)
        return self.title_url_matches(pages_data.HomeData.title, pages_data.HomeData.url)


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

    def send_form(self, login=False, form_update=None):
        ok = super().send_form(login, form_update)
        return ok


class ChangeUserPage(PkPage):
    def __init__(self, driver, data=None, pk=-1):
        if data is None:
            data = pages_data.ChangeUserData(pk=pk)
        super().__init__(driver, data)


class ConfirmationPage(BasePage):
    def __init__(self, driver, app, model, data=None):
        if data is None:
            data = pages_data.ConfirmationData(app, model)
        super().__init__(driver, data)

    def confirm_delete(self):
        try:
            locator = ConfirmationPageLocator.confirm_delete
            confirm_input = self.driver.find_element(*locator)
            confirm_input.click()
            return True
        except NoSuchElementException:
            return False


class ItemPage(ListPage):
    def __init__(self, driver, model, data=None):
        if data is None:
            data = pages_data.ItemData(model)
        super().__init__(driver, data)


class AddItemPage(BasePage):
    def __init__(self, driver, model, data=None):
        if data is None:
            data = pages_data.AddItemData(model)
        super().__init__(driver, data)
        self.pk = 0

    def send_form(self, login=False, form_update=None):
        ok = super().send_form(login, form_update)
        if ok:
            ok, pk = self._was_created_with_pk()
            self.pk = pk
        return ok


class ChangeItemPage(PkPage):
    def __init__(self, driver, model, data=None, pk=-1):
        if data is None:
            data = pages_data.ChangeItemData(model, pk=pk)
        super().__init__(driver, data)
