import allure
from selene import browser


class MainPage:


    def open(self):
        with allure.step('Open the main page'):
            browser.open('/')

    def search(self, value):
        with allure.step('Open the search page'):
            browser.element('[aria-label=Search]').click()
        with allure.step(f'Enter {value} in the search input'):
            browser.element('[data-testid=search-input]').type(value).press_enter()

    def add_playlist(self):
        with allure.step('Open the context menu for creating'):
            browser.element('[style="display: block;"]').click()
        with allure.step('Select "create playlist" option'):
            browser.element('[role=menuitem]:first-child').click()
