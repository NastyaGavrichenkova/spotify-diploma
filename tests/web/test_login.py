import allure
from allure_commons.types import Severity
from selene import browser, have
from models.web.login_page import LoginPage
from models.web.main_page import MainPage
from data.user import User

main_page = MainPage()
login_page = LoginPage()
user = User()

incorrect_login = 'incorrect_login@login.com'
incorrect_password = 'password'


@allure.tag('UI')
@allure.label('owner', 'ganastasia')
@allure.feature('Authorization')
@allure.story('Successful authorization')
@allure.severity(Severity.BLOCKER)
@allure.title('User can authorization with correct login and password')
def test_successful_authorization():
    main_page.open()
    login_page.open_from_main_screen()
    login_page.authorization(user.login, user.password)

    with allure.step('Verify user name'):
        browser.element('[data-testid=user-widget-avatar]').element(f'[title={user.name}]')


@allure.tag('UI')
@allure.label('owner', 'ganastasia')
@allure.feature('Authorization')
@allure.story('Authorization with incorrect login and correct password')
@allure.severity(Severity.BLOCKER)
@allure.title("User can't authorization with incorrect login and correct password")
def test_authorization_with_incorrect_login():
    login_page.open_by_link()
    login_page.authorization(incorrect_login, user.password)

    with allure.step('Verify error banner'):
        browser.element('[aria-label^=Error]')
    with allure.step('Check error message'):
        browser.element('[class^=Message]').should(have.exact_text('Incorrect username or password.'))


@allure.tag('UI')
@allure.label('owner', 'ganastasia')
@allure.feature('Authorization')
@allure.story('Authorization with correct login and incorrect password')
@allure.severity(Severity.BLOCKER)
@allure.title("User can't authorization with correct login and incorrect password")
def test_authorization_with_incorrect_password():
    login_page.open_by_link()
    login_page.authorization(user.login, incorrect_password)

    with allure.step('Verify error banner'):
        browser.element('[aria-label^=Error]')
    with allure.step('Check error message'):
        browser.element('[class^=Message]').should(have.exact_text('Incorrect username or password.'))
