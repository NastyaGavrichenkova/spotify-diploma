import allure
from allure_commons.types import Severity
from selene import browser, have
from models.web.login_page import LoginPage
from models.web.main_page import MainPage
from data.tracks_artists import Track, Artist
from tests.marks import layer

pytestmark = [
    layer("UI")]


main_page = MainPage()
login_page = LoginPage()
track = Track()
artist = Artist()


@allure.tag('UI')
@allure.label('owner', 'ganastasia')
@allure.feature('Search')
@allure.story('Search on the main screen')
@allure.severity(Severity.CRITICAL)
@allure.title(f'User can find the arist {artist.name}')
def test_search():
    main_page.open()
    main_page.search(artist.name)

    with allure.step('Verify the first result'):
        browser.all('[data-testid=top-result-card]').element(f'[title={artist.name}]')


@allure.tag('UI')
@allure.label('owner', 'ganastasia')
@allure.feature('Search')
@allure.story('Search on the main screen')
@allure.severity(Severity.CRITICAL)
@allure.title(f"User can't find nonexistent track {track.wrong_name}")
def test_no_result_search():
    main_page.open()
    main_page.search(track.wrong_name)

    with allure.step("Verify there're no results"):
        browser.element('div#searchPage').should(have.text(f'No results found for "{track.wrong_name}"'))
