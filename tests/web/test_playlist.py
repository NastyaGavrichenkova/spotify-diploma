import allure
from allure_commons.types import Severity
from selene import browser
from models.web.login_page import LoginPage
from models.web.main_page import MainPage
from data.user import User
from data.tracks_artists import Track
from tests.marks import layer

pytestmark = [
    layer("UI")]

main_page = MainPage()
login_page = LoginPage()
user = User()
track = Track()


@allure.tag('UI')
@allure.label('owner', 'ganastasia')
@allure.feature('Playlists')
@allure.story('Add a new playlist')
@allure.severity(Severity.CRITICAL)
@allure.title('User add an empty playlist')
def test_add_playlist():
    login_page.open_by_link()
    login_page.authorization(user.login, user.password)
    main_page.add_playlist()

    with allure.step('Check the new album in the list'):
        browser.element('[data-testid=playlist-page]').element('[aria-label^="My Playlist"]')

