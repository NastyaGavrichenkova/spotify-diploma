import time

import allure

from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have

name = 'This playlist was created through Android app'


class LibraryTab:

    def open_library_tab(self):
        with allure.step('Go to library tab'):
            browser.element((AppiumBy.ID, 'com.spotify.music:id/your_library_tab')).click()

    def add_new_playlist(self):
        with allure.step('Open creating panel'):
            browser.element((AppiumBy.ID, 'com.spotify.music:id/icon_create')).click()
        with allure.step(('Select Create playlist option')):
            browser.element((AppiumBy.ID, 'com.spotify.music:id/create_playlist_row')).click()
        with allure.step('Rename the playlist'):
            browser.element((AppiumBy.ID, 'com.spotify.music:id/edit_text')).type(name)
        with allure.step('Confirm creating'):
            browser.element((AppiumBy.ID, 'com.spotify.music:id/continue_button')).click()
            time.sleep(3)

    def add_first_song_to_playlist(self, value):
        with allure.step('Open add to playlist screen'):
            browser.element((AppiumBy.ID, 'com.spotify.music:id/action_button')).click()
        with allure.step('Open the search screen'):
            browser.element((AppiumBy.ID, 'com.spotify.music:id/search_field_root')).click()
        with allure.step(f'Enter {value} track to the input'):
            browser.element((AppiumBy.ID, 'com.spotify.music:id/query')).type(value)
        with allure.step('Add selected track'):
            browser.all((AppiumBy.ID, 'com.spotify.music:id/quick_action')).first.click()


    def rename_created_playlist(self, value):
        with allure.step('Open playlist context menu'):
            browser.element((AppiumBy.ID, 'com.spotify.music:id/context_menu_button')).click()
        with allure.step('Select edit playlist option'):
            browser.all((AppiumBy.ID, 'com.spotify.music:id/title')).element_by(have.text('Edit playlist')).click()
        with allure.step(f'Enter {value} to the input'):
            input = browser.element((AppiumBy.ID, 'com.spotify.music:id/title_edit_text')).click()
            input.type(value)
        with allure.step('Save changes'):
            browser.all((AppiumBy.CLASS_NAME, 'android.widget.Button')).element_by(have.text('Save')).click()
