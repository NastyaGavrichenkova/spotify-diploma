import pytest
from selene import browser
from selenium import webdriver

from utils import attach


@pytest.fixture(autouse=True)
def setup_browser():
    driver_options = webdriver.ChromeOptions()
    # driver_options.add_argument('headless')
    browser.config.driver_options = driver_options
    browser.config.base_url = 'https://open.spotify.com'

    yield browser

    attach.screenshot(browser)
    attach.logs(browser)
    attach.html(browser)
    attach.video(browser)

    browser.quit()
