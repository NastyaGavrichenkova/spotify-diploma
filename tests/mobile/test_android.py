import allure
from allure_commons.types import Severity
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have
from data.user import User
from data.tracks_artists import Artist, Track
from models.mobile.search_tab import SearchTab
from models.mobile.start_page import StartPage
from models.mobile.library_tab import LibraryTab
from tests.marks import layer

pytestmark = [
    layer("Android")]

start_page = StartPage()
search_tab = SearchTab()
library_tab = LibraryTab()
user = User()
artist = Artist()
track = Track()
playlist_name = 'This playlist was renamed'


@allure.tag('Android')
@allure.label('owner', 'ganastasia')
@allure.feature('Search')
@allure.story('Search top results')
@allure.severity(Severity.CRITICAL)
@allure.title(f'User can find the arist {artist.name}')
def test_search():
    start_page.authorization(user.login, user.password)
    search_tab.search(artist.name)

    with allure.step('Verify the first result'):
        results = browser.all((AppiumBy.ID, 'com.spotify.music:id/title'))
        results.first.should(have.text(artist.name))


@allure.tag('Android')
@allure.label('owner', 'ganastasia')
@allure.feature('Playlist')
@allure.story('Add track to playlist')
@allure.severity(Severity.CRITICAL)
@allure.title(f'User can add the first track to a new playlist')
def test_add_first_track_to_playlist():
    start_page.authorization(user.login, user.password)
    library_tab.open_library_tab()
    library_tab.add_new_playlist()
    library_tab.add_first_song_to_playlist(track.name)

    with allure.step('Return to playlist screen'):
        browser.element((AppiumBy.ID, 'com.spotify.music:id/toolbar_up_button')).click()

    with allure.step('Verify added track'):
        browser.element((AppiumBy.ID, 'com.spotify.music:id/track_cloud')).should(have.text(track.name))


@allure.tag('Android')
@allure.label('owner', 'ganastasia')
@allure.feature('Playlist')
@allure.story('Rename a playlist')
@allure.severity(Severity.NORMAL)
@allure.title(f'User can rename created playlist')
def test_rename_created_playlist():
    start_page.authorization(user.login, user.password)
    library_tab.open_library_tab()
    library_tab.add_new_playlist()
    library_tab.rename_created_playlist(playlist_name)

    with allure.step('Verify new name'):
        browser.element((AppiumBy.ID, 'com.spotify.music:id/title')).should(have.exact_text(playlist_name))