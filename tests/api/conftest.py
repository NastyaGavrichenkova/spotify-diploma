import base64
import time

from selene import browser, be, command
from selenium import webdriver
import pytest
from spotipy.oauth2 import SpotifyOAuth
import requests
from dotenv import load_dotenv
from data.user import User
from utils.helper import abs_path_to_file
import os

user = User()
load_dotenv(abs_path_to_file('.env.selenoid_credentials'))


DEFAULT_BROWSER_VERSION = '100.0'


def pytest_addoption(parser):
    parser.addoption(
        '--browser_version',
        default=DEFAULT_BROWSER_VERSION
    )


@pytest.fixture(scope='session', autouse=True)
def browser_management(request):

    browser_version = request.config.getoption('--browser_version')
    browser_version = browser_version if browser_version != '' else DEFAULT_BROWSER_VERSION
    driver_options = webdriver.ChromeOptions()

    browser.config.driver_options = driver_options

    selenoid_capabilities = {
        'browserName': 'chrome',
        'browserVersion': browser_version,
        'selenoid:options': {
            'enableVNC': True,
            'enableVideo': True
        }
    }
    driver_options.capabilities.update(selenoid_capabilities)

    login = os.getenv('SELENOID_LOGIN')
    password = os.getenv('SELENOID_PASSWORD')

    browser.config.driver = webdriver.Remote(
        command_executor=f'https://{login}:{password}@selenoid.autotests.cloud/wd/hub',
        options=driver_options
    )

    yield

    browser.quit()


@pytest.fixture(scope='session')
def get_access_token(browser_management):
    redirect_uri = 'https://open.spotify.com'
    scope = 'user-read-private user-library-modify playlist-modify-private user-read-email'

    url = SpotifyOAuth(client_id=user.client_id,
                       client_secret=user.client_secret,
                       redirect_uri=redirect_uri,
                       scope=scope
                       ).get_authorize_url()

    browser.open(url)

    browser.element('#login-username').type(user.login)
    browser.element('#login-password').type(user.password).press_enter()
    time.sleep(5)
    if browser.element("[data-testid='auth-accept']").matching(be.visible):
        browser.element("[data-testid='auth-accept']").perform(command.js.scroll_into_view).click()
    browser.switch_to_next_tab()
    time.sleep(5)
    current_url = browser.driver.current_url
    print(current_url)
    part = current_url.split('=')[1]

    encoded_credentials = base64.b64encode(user.client_id.encode() + b':' + user.client_secret.encode()).decode('utf-8')

    token_headers = {
        'Authorization': 'Basic ' + encoded_credentials,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    token_data = {
        'grant_type': 'authorization_code',
        'code': part,
        'redirect_uri': redirect_uri
    }

    r = requests.post('https://accounts.spotify.com/api/token', data=token_data, headers=token_headers)
    print(r)
    access_token = r.json()['access_token']

    return access_token
