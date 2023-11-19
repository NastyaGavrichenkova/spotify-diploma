import allure
import pytest
from appium import webdriver
from selene import browser, support
import allure_commons
from utils.helper import abs_path_to_file
from utils import attach
from config import Config

app_config = Config(_env_file=abs_path_to_file(f'.env.{Config().app_context}'))


@pytest.fixture(scope='function', autouse=True)
def mobile_management():
    with allure.step('Init app session'):
        browser.config.driver = webdriver.Remote(
            app_config.remote_url,
            options=app_config.to_driver_options()
        )

    browser.config.timeout = app_config.timeout

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    yield

    attach.screenshot(browser)

    attach.page_source(browser)

    session_id = browser.driver.session_id

    browser.quit()

    if app_config.runs_on_bstack():
        attach.bstack_video(session_id, app_config.bstack_userName, app_config.bstack_accessKey)
