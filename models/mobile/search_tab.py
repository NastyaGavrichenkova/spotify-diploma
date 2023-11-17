import allure

from appium.webdriver.common.appiumby import AppiumBy
from selene import browser


class SearchTab:

    def search(self, value):
        with allure.step('Go to search tab'):
            browser.element((AppiumBy.ID, 'com.spotify.music:id/search_tab')).click()
        with allure.step('Open the search screen'):
            browser.element((AppiumBy.ID, 'com.spotify.music:id/find_search_field_text')).click()
        with allure.step(f'Enter {value} to the search input'):
            browser.element((AppiumBy.ID, 'com.spotify.music:id/query')).send_keys(value)