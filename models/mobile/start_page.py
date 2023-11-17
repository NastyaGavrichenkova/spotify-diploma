import time

import allure

from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have, be


class StartPage:
    def authorization(self, login, password):
        with allure.step('Open login page'):
            button = browser.all((AppiumBy.CLASS_NAME, 'android.widget.Button')).element_by(have.text('Log in'))
            button.click()
        with allure.step(f'Enter the login {login}'):
            browser.element((AppiumBy.ID, 'com.spotify.music:id/username_text')).type(login)
        with allure.step('Enter the password'):
            browser.element((AppiumBy.ID, 'com.spotify.music:id/password_text')).type(password)
        with allure.step('Click login button'):
            browser.element((AppiumBy.ID, 'com.spotify.music:id/login_button')).click()
            time.sleep(3)

        if browser.element((AppiumBy.ID, 'com.spotify.music:id/design_bottom_sheet')).matching(be.visible):
            with allure.step('Close bottom sheet'):
                browser.element((AppiumBy.ID, 'com.spotify.music:id/later_button')).click()
