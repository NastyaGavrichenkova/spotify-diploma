import os
from typing import Literal

from pydantic_settings import BaseSettings
from appium.options.android import UiAutomator2Options
from utils.helper import abs_path_to_file
from dotenv import load_dotenv
from selenium import webdriver


class Config(BaseSettings):
    app_context: Literal['local_emulator', 'bstack'] = 'bstack'
    web_context: Literal['local', 'remote'] = 'local'

    # App params
    remote_url: str = ''
    app: str = ''
    appWaitActivity: str = ''
    timeout: float = 10.0

    bstack_userName: str = ''
    bstack_accessKey: str = ''
    deviceName: str = ''
    platformVersion: str = ''

    # WEB param
    browser: Literal['chrome', 'firefox'] = 'chrome'

    @property
    def get_selenoid_capabilities(self):
        capabilities = {
            'browserName': 'chrome',
            'browserVersion': '100.0',
            'selenoid:options': {
                'enableVNC': True,
                'enableVideo': True
            }
        }

        return capabilities

    def selenoid_auth_link(self):
        load_dotenv(abs_path_to_file('.env.selenoid_credentials'))
        login = os.getenv('SELENOID_LOGIN')
        password = os.getenv('SELENOID_PASSWORD')
        link = f'https://{login}:{password}@selenoid.autotests.cloud/wd/hub'

        return link

    def to_browser_driver_options(self):
        if self.browser == 'chrome':
            options = webdriver.ChromeOptions()

        elif self.browser == 'firefox':
            options = webdriver.FirefoxOptions()

        return options

    def browser_remote_driver(self):
        if self.web_context == 'remote':
            options = self.to_browser_driver_options()
            selenoid_capabilities = self.get_selenoid_capabilities
            options.capabilities.update(selenoid_capabilities)

            driver = webdriver.Remote(
                command_executor=self.selenoid_auth_link(),
                options=options
            )

        return driver

    def runs_on_bstack(self):
        return self.app.startswith('bs://')

    @property
    def bstack_creds(self):
        load_dotenv(abs_path_to_file('.env.bstack_credentials'))
        self.bstack_userName = os.getenv('bstack_userName')
        self.bstack_accessKey = os.getenv('bstack_accessKey')
        return {
            'userName': self.bstack_userName,
            'accessKey': self.bstack_accessKey
        }

    @property
    def bstack_deviceName_and_platformVersion(self):
        return {
            'deviceName': self.deviceName,
            'platformVersion': self.platformVersion
        }

    def to_driver_options(self):
        options = UiAutomator2Options()
        options.set_capability('app', (
            self.app if (self.app.startswith('/') or self.runs_on_bstack())
            else abs_path_to_file(self.app)
        ))

        if self.appWaitActivity:
            options.set_capability('appWaitActivity', self.appWaitActivity)

        if self.runs_on_bstack():
            options.load_capabilities({
                **self.bstack_deviceName_and_platformVersion,

                'bstack:options': {
                    'projectName': 'First Python project',
                    'buildName': 'browserstack-android-build-1',
                    'sessionName': 'BStack first_android_test',

                    **self.bstack_creds
                }
            })

        return options
