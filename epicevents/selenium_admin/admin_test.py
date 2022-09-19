from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
import pytest
from time import sleep
import pages


@pytest.fixture(scope="module", params=["chrome"])
def selenium(request):
    driver = request.param
    if driver == "chrome":
        service = ChromeService('C:/ProgramData/Miniconda3/Webdrivers/chromedriver')
        options = webdriver.ChromeOptions()
        options.add_argument("no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=800,600")
        options.add_argument("--disable-dev-shm-usage")
        options.set_capability("detach", True)
    elif driver == "firefox":
        service = FirefoxService('C:/ProgramData/Miniconda3/Webdrivers/geckodriver')
        options = webdriver.FirefoxOptions()
        options.binary_location = r"C:\Users\xdeva\AppData\Local\Mozilla Firefox\firefox.exe"
    else:
        return None
    service.start()
    selenium = webdriver.Remote(service.service_url, options=options)
    yield selenium
    selenium.quit()
    service.stop()


class TestAdminStories:
    def test_admin_login(self, selenium):
        selenium.get('http://127.0.0.1:8000/admin/')
        login_page = pages.LoginPage(selenium)
        assert login_page.title_url_matches()
        login_page.log_user()
        home_page = pages.HomePage(selenium)
        assert home_page.title_url_matches()

    def test_admin_can_cru_user(self, selenium):
        selenium.get('http://127.0.0.1:8000/admin/')
        home_page = pages.HomePage(selenium)
        assert home_page.title_url_matches()
        home_page.find_link_and_follow('user', 'add')

        add_user_page = pages.AddUserPage(selenium)
        assert add_user_page.title_url_matches()
        add_user_page.fill_form()
        add_user_page.submit_form()

        change_user_page = pages.ChangeUserPage(selenium)
        assert change_user_page.get_pk_and_update_url('user')
        assert change_user_page.title_url_matches()
        change_user_page.fill_form()
        change_user_page.submit_form()

        user_page = pages.UserPage(selenium)
        assert user_page.title_url_matches()

    def test_admin_can_find_and_delete_user(self, selenium):
        selenium.get('http://127.0.0.1:8000/admin/')
        home_page = pages.HomePage(selenium)
        assert home_page.title_url_matches()
        home_page.find_link_and_follow('user')

        user_page = pages.UserPage(selenium)
        assert user_page.title_url_matches()
        user_page.search_created()
        assert ">0 results" not in selenium.page_source
        user_page.check_result_1_box()
        user_page.select_action_and_go('delete')

        confirmation_page = pages.ConfirmationPage(selenium, 'authentication', 'user')
        assert confirmation_page.title_url_matches()
        confirmation_page.confirm_delete()
        assert user_page.title_url_matches()
        user_page.search_created()
        assert ">0 results" in selenium.page_source
        user_page.logout()
        logout_page = pages.LogoutPage(selenium)
        assert logout_page.title_url_matches()
