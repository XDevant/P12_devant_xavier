from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
import pytest
from time import sleep


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


class TestUserStories:
    def test_live_server(self, selenium):
        selenium.get('http://127.0.0.1:8000/admin/')
        assert selenium.title == "Log in | Django site admin"
        email = selenium.find_element(By.CSS_SELECTOR, 'input[id="id_username"]')
        email.clear()
        email.send_keys("za@za.co")
        sleep(1)
        password = selenium.find_element(By.CSS_SELECTOR, 'input[id="id_password"]')
        password.clear()
        password.send_keys("mdp5")
        password.submit()
        sleep(1)
        assert selenium.current_url == 'http://127.0.0.1:8000/admin/'

    def test_admin_story_1(self, selenium):
        pass
