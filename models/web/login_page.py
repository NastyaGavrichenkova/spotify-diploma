import allure
from selene.support.shared import browser


class LoginPage:

    def open_from_main_screen(self):
        with allure.step('Open the login page from the main screen'):
            browser.element('[data-testid=login-button]').click()

    def open_by_link(self):
        with allure.step('Open the login page by the link'):
            browser.open('https://accounts.spotify.com/en/login?continue=https%3A%2F%2Fopen.spotify.com%2F')

    def authorization(self, login, password):
        with allure.step(f'Enter the login {login}'):
            browser.element('#login-username').type(login)
        with allure.step('Enter the password'):
            browser.element('#login-password').type(password)
        with allure.step('Log in'):
            browser.element('#login-button').click()
