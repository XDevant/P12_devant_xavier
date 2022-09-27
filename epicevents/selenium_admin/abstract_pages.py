from selenium.webdriver.remote.errorhandler import InvalidElementStateException, NoSuchElementException
from time import sleep
from locators import BasePageLocator, PkPageLocator, ListPageLocator, SearchPageLocator, Selector
from pages_data import LoginData


class BasePage:
    """Base class to initialize the base page that will be called from all
    pages"""

    def __init__(self, driver, data):
        self.driver = driver
        self.url = data.url
        self.title = data.title
        self.form = data.form

    def title_url_matches(self, title=None, url=None):
        """Verifies that we reached the expected page of the admin site"""
        if title is None:
            title = self.title
        if url is None:
            url = self.url
        print(f" Asserting  {title} in Page Title and url == {url}")
        return title in self.driver.title and url in self.driver.current_url

    def _fill_form(self, form_update=None):
        form = self.form
        if form_update is not None and isinstance(form_update, dict):
            for key, value in form_update.items():
                form[key] = value
        for key, value in form.items():
            locator = BasePageLocator(key).fill_form
            form_input = self.driver.find_element(*locator)
            try:
                form_input.clear()
            except InvalidElementStateException:
                pass
            form_input.send_keys(value)
            sleep(1)

    def _submit_form(self, login=False):
        if login:
            locator = BasePageLocator.login_form
        else:
            locator = BasePageLocator.submit_form
        submit = self.driver.find_element(*locator)
        submit.submit()

    def send_form(self, login=False, form_update=None):
        try:
            self._fill_form(form_update)
            self._submit_form(login)
            return True
        except NoSuchElementException:
            return False

    def find_nav_link_and_follow(self, model, action=None):
        try:
            locator = BasePageLocator(model=model, action=action).find_nav_link_and_follow
            link = self.driver.find_element(*locator)
            link.click()
            return True
        except NoSuchElementException:
            return False

    def logout(self):
        if Selector.logout in self.driver.page_source:
            locator = BasePageLocator.logout
            link = self.driver.find_element(*locator)
            link.submit()
            sleep(1)
            return True
        return False

    def _login(self, form=None):
        self.driver.get(LoginData.url)
        if form is None:
            self._fill_form(LoginData.form)
        else:
            self._fill_form(form)
        self._submit_form(True)

    def _get_admin_form(self, email):
        for form in LoginData.forms:
            if form["username"] == email:
                return form
        return {}

    def get_page(self, email=None, autolog=True):
        """Navigates to the page url. If admin email is provided, will first log the admin.
        if no email is provided, default autolog=True will log the admin in pages_data.LoginData.form
        only if no admin is currently logged"""
        if email is not None:
            if Selector(email).logged not in self.driver.page_source:
                self.logout()
                form = self._get_admin_form(email)
                self._login(form)
        else:
            if Selector.logout not in self.driver.page_source:
                if autolog:
                    self._login()
        self.driver.get(self.url)
        return self.title_url_matches()

    def _was_created_with_pk(self):
        locator = BasePageLocator.created_successfully
        try:
            link = self.driver.find_element(*locator)
            pk = int(link.text)
            return pk > 0, pk
        except NoSuchElementException:
            return False, 0


class PkPage(BasePage):
    def __init__(self, driver, data):
        super().__init__(driver, data)
        self.pk = data.pk

    def get_pk_and_update_url(self, model):
        real_url = self.driver.current_url
        needle = f'{model}/'
        if needle in real_url:
            url_parts = real_url.split(needle)
            if len(url_parts) < 2:
                print("wrong model")
                return 0
            pk = url_parts[1].split('/')[0]
            self.url = self.url.replace("$pk$", pk)
            self.pk = int(pk)
            return self.pk > 0

    def delete_item(self):
        try:
            locator = PkPageLocator().delete_item
            link = self.driver.find_element(*locator)
            link.click()
            sleep(1)
            return True
        except NoSuchElementException:
            return False


class ListPage(BasePage):
    def __init__(self, driver, data):
        super().__init__(driver, data)
        self.pk = data.pk
        self.target_pk_url = "/admin" + data.url.split("/admin")[-1]

    def find_list_link_and_follow(self, pk):
        try:
            url = self.target_pk_url + str(pk) + '/change/'
            locator = ListPageLocator(url).find_list_link_and_follow
            link = self.driver.find_element(*locator)
            link.click()
            return True
        except NoSuchElementException:
            return False


class SearchPage(ListPage):
    def __init__(self, driver, data):
        super().__init__(driver, data)
        self.search = data.search

    def search_created(self):
        locator = SearchPageLocator.search_created
        search_input = self.driver.find_element(*locator)
        search_input.send_keys(self.search)
        search_input.submit()

    def check_result_1_box(self):
        locator = SearchPageLocator.check_result_1_box
        link = self.driver.find_element(*locator)
        link.click()

    def select_action_and_go(self, action):
        locator = SearchPageLocator('', action=action).select_action_and_go
        select_input = self.driver.find_element(*locator)
        select_input.click()
        sleep(1)
        select_input.submit()
