from selenium.webdriver.common.by import By


class BasePageLocator:
    """"""
    submit_form = (By.NAME, '_save')
    login_form = (By.ID, 'id_username')
    logout = (By.ID, "logout-form")
    created_successfully = (By.CSS_SELECTOR, "ul.messagelist li.success a")

    def __init__(self, key=None, model=None, action=None):
        if key is not None:
            self.fill_form = (By.ID, 'id_' + key)
        if model is not None:
            selector = f'tr.model-{model} a'
            if action is not None:
                selector += f'.{action}link'
            self.find_nav_link_and_follow = (By.CSS_SELECTOR, selector)


class PkPageLocator:
    delete_item = (By.CSS_SELECTOR, 'a.deletelink')


class ListPageLocator:
    def __init__(self, link_url):
        selector = f'a[href="{link_url}"]'
        self.find_list_link_and_follow = (By.CSS_SELECTOR, selector)


class SearchPageLocator(ListPageLocator):
    search_created = (By.ID, "searchbar")
    check_result_1_box = (By.NAME, "_selected_action")

    def __init__(self, link_url, action=None):
        if action is not None:
            super().__init__(link_url)
            self.select_action_and_go = (By.CSS_SELECTOR,
                                         f"option[value='{action}_selected']")


class ConfirmationPageLocator:
    confirm_delete = (By.CSS_SELECTOR, "input[value='Yes, I’m sure']")


class Selector:
    logout = '<form id="logout-form" method="post" action="/admin/logout/">'

    def __init__(self, email=None):
        if email is not None:
            self.logged = f"<strong>{email}</strong>."
