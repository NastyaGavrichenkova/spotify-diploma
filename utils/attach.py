import allure
from allure_commons.types import AttachmentType
import requests


def screenshot(browser):
    allure.attach(
        browser.driver.get_screenshot_as_png(),
        name='screenshot',
        attachment_type=allure.attachment_type.PNG,
        extension='.png'
    )


def logs(browser):
    log = "".join(f'{text}\n' for text in browser.driver.get_log(log_type='browser'))
    allure.attach(
        log,
        name='browser_logs',
        attachment_type=AttachmentType.TEXT,
        extension='.log'
    )


def html(browser):
    allure.attach(
        browser.driver.page_source,
        name='page_source',
        attachment_type=allure.attachment_type.HTML,
        extension='.html'
    )


def video(browser):
    video_url = "https://selenoid.autotests.cloud/video/" + browser.driver.session_id + ".mp4"
    html = "<html><body><video width='100%' height='100%' controls autoplay><source src='" \
           + video_url \
           + "' type='video/mp4'></video></body></html>"
    allure.attach(
        html,
        name='video_' + browser.driver.session_id,
        attachment_type=allure.attachment_type.HTML,
        extension='.html'
    )


def bstack_video(session_id, user_name, access_key):
    bstack_session = requests.get(
        f'https://api.browserstack.com/app-automate/sessions/{session_id}.json',
        auth=(user_name, access_key),
    ).json()
    video_url = bstack_session['automation_session']['video_url']

    allure.attach(
        '<html><body>'
        '<video width="100%" height="100%" controls autoplay>'
        f'<source src="{video_url}" type="video/mp4">'
        '</video>'
        '</body></html>',
        name='video recording',
        attachment_type=allure.attachment_type.HTML,
        extension='.html'
    )


def page_source(browser):
    allure.attach(
        browser.driver.page_source,
        name='screen xml dump',
        attachment_type=allure.attachment_type.XML,
        extension='.xml'
    )
