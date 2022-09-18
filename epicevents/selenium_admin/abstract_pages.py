from selenium.webdriver.common.by import By
from selenium.webdriver.remote.errorhandler import InvalidElementStateException
from time import sleep


class BasePage:
    """Base class to initialize the base page that will be called from all
    pages"""

    def __init__(self, driver, data):
        self.driver = driver
        self.url = data.url
        self.title = data.title
        self.form = data.form

    def title_url_matches(self):
        """Verifies that we reached the expected page of the admin site"""
        print(f" Asserting  {self.title} in Page Title and url == {self.url}")
        return self.title in self.driver.title and self.url == self.driver.current_url

    def fill_form(self):
        for key, value in self.form.items():
            form_input = self.driver.find_element(By.ID, 'id_' + key)
            try:
                form_input.clear()
                form_input.send_keys(value)
            except InvalidElementStateException:
                form_input.send_keys(value)
            sleep(1)

    def submit_form(self):
        submit = self.driver.find_element(By.NAME, '_save')
        submit.click()

    def find_link_and_follow(self, model, action=None):
        selector = f'tr.model-{model} a'
        if action:
            selector += f'.{action}link'
        link = self.driver.find_element(By.CSS_SELECTOR, selector)
        link.click()


class PkPage(BasePage):
    def __init__(self, driver, data):
        super().__init__(driver, data)
        self.url_start = data.url_start
        self.url_end = data.url_end
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
            self.url = self.url_start + pk + self.url_end
            self.pk = int(pk)
            return self.pk > 0


class SearchPage(BasePage):
    def __init__(self, driver, data):
        super().__init__(driver, data)
        self.search = data.search

    def search_created(self):
        search_input = self.driver.find_element(By.ID, "searchbar")
        search_input.send_keys(self.search)
        search_input.submit()
