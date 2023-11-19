import pytest
from selene import browser
from selenium import webdriver
import os
from dotenv import load_dotenv

from utils import attach
from utils.helper import abs_path_to_file

load_dotenv(abs_path_to_file('.env.selenoid_credentials'))


@pytest.fixture(autouse=True)
def setup_browser(request):
    driver_options = webdriver.ChromeOptions()

    browser.config.driver_options = driver_options

    selenoid_capabilities = {
        'browserName': 'chrome',
        'browserVersion': '100.0',
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
    browser.config.base_url = 'https://open.spotify.com'

    yield browser

    attach.screenshot(browser)
    attach.logs(browser)
    attach.html(browser)
    attach.video(browser)

    browser.quit()
