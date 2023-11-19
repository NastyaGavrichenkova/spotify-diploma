import pytest
from selene import browser

from utils import attach
from config import Config

config = Config()


@pytest.fixture(autouse=True)
def setup_browser(request):
    browser.config.driver = config.to_browser_driver_options

    if config.web_context == 'remote':
        browser.config.driver = config.browser_remote_driver()

    browser.config.base_url = 'https://open.spotify.com'

    yield browser

    attach.screenshot(browser)
    attach.logs(browser)
    attach.html(browser)
    attach.video(browser)

    browser.quit()
