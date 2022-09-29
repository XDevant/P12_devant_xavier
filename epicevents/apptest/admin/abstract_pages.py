from selenium.webdriver.remote.errorhandler import InvalidElementStateException, NoSuchElementException
from time import sleep
from .locators import BasePageLocator, PkPageLocator, ListPageLocator, SearchPageLocator, Selector
from .pages_data import LoginData


class BasePage:
    """Base class to initialize the base page that will be called from all
    pages"""

    def __init__(self, driver, data):
        self.driver = driver
        self.url = data.url
        self.title = data.title
        self.form = data.form
        self.sleep_time = data.sleep_time

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
        print(self.form)

        for key, value in form.items():
            locator = BasePageLocator(key).fill_form
            form_input = self.driver.find_element(*locator)
            try:
                form_input.clear()
            except InvalidElementStateException:
                pass
            form_input.send_keys(value)
            sleep(self.sleep_time)

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
            sleep(self.sleep_time)
            return True
        return False

    def _login(self, form):
        self.driver.get(LoginData.url)
        self._fill_form(form)
        self._submit_form(True)

    def get_page(self, logs=None):
        """Navigates to the page url. If logs are provided, will first log the admin if needed.
        Note that without logs provided, any page other than login page will only be reached if
        an admin is already logged.
         Returns True if the page is reached and False otherwise."""
        if logs is not None:
            logs["username"] = logs.pop("email")
            if Selector(logs["username"]).logged not in self.driver.page_source:
                self.logout()
                form = logs
                self._login(form)
        self.driver.get(self.url)
        return self.title_url_matches()

    def _was_created_with_pk(self):
        """Looks for the message following a successfull creation and extracts the id of the created item"""
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
        """Extracts the pk in the driver's current url to update page data that depends on pk
        like url and pk. Return True if a pk is found."""
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
            sleep(self.sleep_time)
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
        sleep(self.sleep_time)
        select_input.submit()
