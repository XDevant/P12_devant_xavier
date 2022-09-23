from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
import pytest
import pages


class Memory:
    last_created_user = 0
    last_created_client = 0
    last_created_contract = 0
    last_created_event = 0


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
        login_page = pages.LoginPage(selenium)
        assert login_page.get_page(autolog=False)
        assert login_page.log_user()

    def test_admin_can_cru_user(self, selenium):
        home_page = pages.HomePage(selenium)
        assert home_page.get_page("za@za.co")
        home_page.find_nav_link_and_follow('user', 'add')

        add_user_page = pages.AddUserPage(selenium)
        assert add_user_page.title_url_matches()
        assert add_user_page.send_form()

        change_user_page = pages.ChangeUserPage(selenium)
        assert change_user_page.get_pk_and_update_url('user')
        assert change_user_page.title_url_matches()
        assert change_user_page.send_form()

        user_page = pages.UserPage(selenium)
        assert user_page.title_url_matches()

    @pytest.mark.parametrize("item", ["client", "contract", "event"])
    def test_superuser_can_create_items(self, selenium, item):
        home_page = pages.HomePage(selenium)
        assert home_page.get_page("super@user.com")
        assert home_page.find_nav_link_and_follow(item, 'add')

        add_item_page = pages.AddItemPage(selenium, item)
        assert add_item_page.title_url_matches()
        form_update = None
        if item != 'client':
            form_update = {"client": Memory.last_created_client}
        assert add_item_page.send_form(form_update=form_update)
        setattr(Memory, f"last_created_{item}", add_item_page.pk)

    def test_admin_can_change_item(self, selenium):
        pass

    def test_superuser_can_cascade_delete_items(self, selenium):
        client_page = pages.ItemPage(selenium, "client")
        assert client_page.get_page("super@user.com")
        assert client_page.find_list_link_and_follow(Memory.last_created_client)

        change_item_page = pages.ChangeItemPage(selenium, "client")
        assert change_item_page.get_pk_and_update_url("client")
        assert change_item_page.title_url_matches()
        assert change_item_page.delete_item()

        confirmation_page = pages.ConfirmationPage(selenium, 'crm', 'client')
        assert confirmation_page.title_url_matches()
        assert confirmation_page.confirm_delete()
        assert client_page.title_url_matches()

    def test_admin_can_find_and_delete_user(self, selenium):
        home_page = pages.HomePage(selenium)
        assert home_page.get_page("za@za.co")
        home_page.find_nav_link_and_follow('user')

        user_page = pages.UserPage(selenium)
        assert user_page.title_url_matches()
        user_page.search_created()
        assert ">0 results" not in selenium.page_source
        user_page.check_result_1_box()
        user_page.select_action_and_go('delete')

        confirmation_page = pages.ConfirmationPage(selenium, 'authentication', 'user')
        assert confirmation_page.title_url_matches()
        assert confirmation_page.confirm_delete()
        assert user_page.title_url_matches()
        user_page.search_created()
        assert ">0 results" in selenium.page_source
        assert user_page.logout()
        logout_page = pages.LogoutPage(selenium)
        assert logout_page.title_url_matches()
