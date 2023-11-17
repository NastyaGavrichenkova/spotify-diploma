import os
from typing import Literal

from pydantic_settings import BaseSettings
from appium.options.android import UiAutomator2Options
from utils.helper import abs_path_to_file
from dotenv import load_dotenv


class AppConfig(BaseSettings):
    context: Literal['local_emulator', 'bstack'] = 'local_emulator'

    remote_url: str = ''
    app: str = ''
    appWaitActivity: str = ''
    timeout: float = 10.0

    bstack_userName: str = ''
    bstack_accessKey: str = ''
    deviceName: str = ''
    platformVersion: str = ''

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
