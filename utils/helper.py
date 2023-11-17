from pathlib import Path
import utils
import json
import allure
from curlify import to_curl
from allure_commons.types import AttachmentType
from requests import Session, Response
import json_schemas


def abs_path_to_file(relative_path: str):
    return (
        Path(utils.__file__)
        .parent.parent.joinpath(relative_path)
        .absolute()
        .__str__()
    )


def load_schema(name):
    path = str(Path(json_schemas.__file__).parent.joinpath(f'{name}').absolute())
    with open(path) as file:
        json_schema = json.loads(file.read())
    return json_schema


class CustomSession(Session):
    def __init__(self, base_url):
        self.base_url = base_url
        super().__init__()

    def request(self, method, url, *args, **kwargs) -> Response:
        request_url = self.base_url+url
        response = super(CustomSession, self).request(method=method, url=request_url, *args, **kwargs)
        message = to_curl(response.request)
        allure.attach(body=message.encode("utf8"),
                      name="Curl",
                      attachment_type=AttachmentType.TEXT,
                      extension='txt')
        try:
            allure.attach(body=json.dumps(response.json(), indent=4).encode("utf8"),
                          name="Response Json",
                          attachment_type=AttachmentType.JSON,
                          extension='json')
        except:
            allure.attach(body=response.content,
                          name="Response text",
                          attachment_type=AttachmentType.TEXT,
                          extension='txt')

        return response

    def auth_header(self, token):
        return {
            'Authorization': f'Bearer {token}'
        }

    def auth_and_content_type_header(self, token):
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }
