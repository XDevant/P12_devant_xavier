from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
import pytest
from . import pages
import config


class Memory:
    """Stores pk of last created items"""
    last_created_user = 0
    last_created_client = 0
    last_created_contract = 0
    last_created_event = 0


@pytest.fixture(scope="module", params=["chrome"])
def selenium(request):
    driver = request.param
    if driver == "chrome":
        pathfile = config.PATH_WEBDRIVERS + 'chromedriver'
        service = ChromeService(pathfile)
        options = webdriver.ChromeOptions()
        options.add_argument("no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=800,600")
        options.add_argument("--disable-dev-shm-usage")
        options.set_capability("detach", True)
    elif driver == "firefox":
        pathfile = config.PATH_WEBDRIVERS + 'geckodriver'
        service = FirefoxService(pathfile)
        options = webdriver.FirefoxOptions()
        loc = r"C:\Users\xdeva\AppData\Local\Mozilla Firefox\firefox.exe"
        options.binary_location = loc
    else:
        return None
    service.start()
    selenium = webdriver.Remote(service.service_url, options=options)
    yield selenium
    selenium.quit()
    service.stop()


class TestAdminStories:
    def test_admin_login(self, selenium, logins):
        login_page = pages.LoginPage(selenium)
        assert login_page.get_page()
        assert login_page.log_user(logins.admin_1)

    @pytest.mark.parametrize("run", [1, 2])
    def test_admin_can_cru_user(self, selenium, logins, run):
        print("\n", end='')
        home_page = pages.HomePage(selenium)
        assert home_page.get_page(logins.admin_1)
        home_page.find_nav_link_and_follow('user', 'add')

        add_user_page = pages.AddUserPage(selenium)
        assert add_user_page.title_url_matches()
        if run == 2:
            form_update = {"role": "sales"}
            assert add_user_page.send_form(form_update=form_update)
        else:
            assert add_user_page.send_form()

        change_user_page = pages.ChangeUserPage(selenium)
        assert change_user_page.get_pk_and_update_url('user')
        assert change_user_page.title_url_matches()
        if run == 1:
            assert change_user_page.send_form()
        else:
            change_user_page._submit_form()

        user_page = pages.UserPage(selenium)
        assert user_page.title_url_matches()

    @pytest.mark.parametrize("item", ["client", "contract", "event"])
    def test_superuser_can_create_items(self, selenium, item, logins):
        print("\n", end='')
        home_page = pages.HomePage(selenium)
        assert home_page.get_page(logins.superuser)
        assert home_page.find_nav_link_and_follow(item, 'add')

        add_item_page = pages.AddItemPage(selenium, item)
        assert add_item_page.title_url_matches()
        form_update = None
        if item == 'contract':
            form_update = {"client": Memory.last_created_client}
        if item == 'event':
            form_update = {"contract": Memory.last_created_contract}
        assert add_item_page.send_form(form_update=form_update)
        setattr(Memory, f"last_created_{item}", add_item_page.pk)

    @pytest.mark.parametrize("item", ["client", "contract", "event"])
    def test_admin_can_change_item(self, selenium, item, logins):
        print("\n", end='')
        item_page = pages.ItemPage(selenium, item)
        assert item_page.get_page(logins.admin_1)
        pk = getattr(Memory, f"last_created_{item}")
        assert item_page.find_list_link_and_follow(pk)

        change_item_page = pages.ChangeItemPage(selenium, item)
        assert change_item_page.get_pk_and_update_url(item)
        assert change_item_page.title_url_matches()
        assert change_item_page.send_form()

    def test_superuser_can_cascade_delete_items(self, selenium, logins):
        print("\n", end='')
        client_page = pages.ItemPage(selenium, "client")
        assert client_page.get_page(logins.superuser)
        assert client_page.find_list_link_and_follow(
                                            Memory.last_created_client
                                                    )
        change_item_page = pages.ChangeItemPage(selenium, "client")
        assert change_item_page.get_pk_and_update_url("client")
        assert change_item_page.title_url_matches()
        assert change_item_page.delete_item()

        confirmation_page = pages.ConfirmationPage(selenium,
                                                   'crm',
                                                   'client')
        assert confirmation_page.title_url_matches()
        assert confirmation_page.confirm_delete()
        assert client_page.title_url_matches()

    @pytest.mark.parametrize("run", [1, 2])
    def test_admin_can_find_and_delete_user(self, selenium, logins, run):
        print("\n", end='')
        home_page = pages.HomePage(selenium)
        assert home_page.get_page(logins.superuser)
        home_page.find_nav_link_and_follow('user')

        user_page = pages.UserPage(selenium)
        assert user_page.title_url_matches()
        user_page.search_created(run - 1)
        assert ">0 results" not in selenium.page_source
        user_page.check_result_1_box()
        user_page.select_action_and_go('delete')

        confirmation_page = pages.ConfirmationPage(selenium,
                                                   'authentication',
                                                   'user')
        assert confirmation_page.title_url_matches()
        assert confirmation_page.confirm_delete()
        assert user_page.title_url_matches()
        user_page.search_created()
        assert ">0 results" in selenium.page_source
        assert user_page.logout()
        logout_page = pages.LogoutPage(selenium)
        assert logout_page.title_url_matches()
