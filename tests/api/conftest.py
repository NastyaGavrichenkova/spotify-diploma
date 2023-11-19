import base64
import time

from selene import browser, be, command
import pytest
from spotipy.oauth2 import SpotifyOAuth
import requests
from data.user import User
from config import Config
from utils import attach

user = User()
config = Config()


@pytest.fixture(scope='session', autouse=True)
def browser_management(request):
    browser.config.driver = config.to_browser_driver_options

    if config.web_context == 'remote':
        browser.config.driver = config.browser_remote_driver()

    browser.config.base_url = 'https://open.spotify.com'

    yield

    attach.screenshot(browser)
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
