from selenium.webdriver.support.ui import WebDriverWait


class BasePageElement():
    """Base page class that is initialized on every page object class."""

    def __set__(self, obj, value):
        """Sets the text to the value supplied"""

        d = obj.driver
        WebDriverWait(d, 100).until(
            lambda driver: d.find_element_by_name(self.locator))
        d.find_element_by_name(self.locator).clear()
        d.find_element_by_name(self.locator).send_keys(value)

    def __get__(self, obj, owner):
        """Gets the text of the specified object"""

        d = obj.driver
        WebDriverWait(d, 100).until(
            lambda driver: driver.find_element_by_name(self.locator))
        element = d.find_element_by_name(self.locator)
        return element.get_attribute("value")