import allure
from allure_commons.types import Severity
import jsonschema
from data.tracks_artists import Track
from data.user import User
from utils.helper import CustomSession, load_schema

spotify_session = CustomSession('https://api.spotify.com/v1')
track = Track()
user = User()


@allure.tag('API')
@allure.label('owner', 'ganastasia')
@allure.feature('User Info')
@allure.story('Current user')
@allure.severity(Severity.CRITICAL)
@allure.title('Validate schema of user information')
def test_get_current_user_information(get_access_token):
    token = get_access_token
    headers = spotify_session.auth_header(token)
    schema = load_schema('user_info.json')

    with allure.step('Get user information'):
        response = spotify_session.request(
            'get',
            url='/me',
            headers=headers
        )

    assert response.status_code == 200
    with allure.step('Validate schema'):
        jsonschema.validate(response.json(), schema)


@allure.tag('API')
@allure.label('owner', 'ganastasia')
@allure.feature('Library')
@allure.story('Current user')
@allure.severity(Severity.CRITICAL)
@allure.title('Add track to the library')
def test_add_track(get_access_token):
    token = get_access_token
    headers = spotify_session.auth_and_content_type_header(token)

    json = {
        'ids': [
            track.id
        ]
    }

    with allure.step('Add track'):
        response = spotify_session.request(
            'put',
            url='/me/tracks',
            headers=headers,
            json=json
        )

    with allure.step('Check response status code'):
        assert response.status_code == 200


@allure.tag('API')
@allure.label('owner', 'ganastasia')
@allure.feature('Library')
@allure.story('Current user')
@allure.severity(Severity.CRITICAL)
@allure.title('Create new playlist')
def test_create_playlist(get_access_token):
    token = get_access_token
    user_id = user.id
    headers = spotify_session.auth_and_content_type_header(token)

    json = {
        "name": "This playlist was created through API",
        "description": "New playlist description",
        "public": False
    }

    with allure.step('Create a new playlist'):
        response = spotify_session.request(
            'post',
            url=f'/users/{user_id}/playlists',
            headers=headers,
            json=json
        )

    with allure.step('Check response status code'):
        assert response.status_code == 201
