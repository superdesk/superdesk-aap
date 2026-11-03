import json
import logging
from urllib.parse import urlparse, urlunparse
import requests

from superdesk.metadata.item import GUID_FIELD
from superdesk.publish.formatters import NINJSFormatter
from superdesk.text_utils import get_text
from superdesk.errors import FormatterError
from superdesk.utils import json_serialize_datetime_objectId

logger = logging.getLogger(__name__)


class GenderAgentFormatter(NINJSFormatter):
    type = "aap gender"
    name = "AAP Gender Agent"

    user_id = "user_sd"
    session_id = "session_sd"
    app_name = "gender"

    def __init__(self):
        super().__init__()
        self.can_preview = True
        self.can_export = False
        self.format_type = "aap gender"

    def can_format(self, format_type, article):
        return format_type.lower() == "aap gender" and article.get("type") == "text"

    def _verify_session(self, subscriber):
        resource_url = None
        destinations = subscriber.get("destinations", [])
        for dest in destinations:
            if dest.get("delivery_type") == "http_push":
                resource_url = dest.get("config", {}).get("resource_url")
                # Hack token is used to nominate the application name
                self.app_name = dest.get("config", {}).get(
                    "secret_token", self.app_name
                )
                break

        if resource_url:
            request_headers = {"Accept": "application/json"}
            parsed_url = urlparse(resource_url)
            test_url_components = (
                parsed_url.scheme,
                parsed_url.netloc,
                f"/apps/{self.app_name}/users/{self.user_id}/sessions/{self.session_id}",
                "",
                "",
                "",
            )
            test_url = urlunparse(test_url_components)
            response = requests.get(test_url, headers=request_headers)
            if response.status_code == 404:
                logger.warning("Non existing session")
                response = requests.post(test_url, headers=request_headers)
                if response.status_code == 200:
                    logger.info("Session Started")
                    return
            elif response.status_code == 200:
                logger.info("Session found")
                return
            try:
                response.raise_for_status()
            except Exception as ex:
                logger.exception(ex)
                raise FormatterError.NINJSFormatterError(ex, subscriber)
        else:
            logger.warning("No push transmitter found")

    def _transform_to_ninjs(self, article, subscriber, recursive=False):
        self._verify_session(subscriber)
        body_lines = [
            line.strip().replace("'", " ")
            for line in get_text(article["body_html"], lf_on_block=True).split("\n")
            if line.strip()
        ]
        body = {
            "item_id": article.get(GUID_FIELD, article.get("uri")),
            "title": get_text(article.get("headline")).replace("'", " "),
            "byline": article.get("byline"),
            "category": article.get("anpa_category"),
            "subjects": article.get("subject"),
            "body": " ".join(body_lines),
        }

        message = {
            "app_name": self.app_name,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "new_message": {
                "role": "user",
                "parts": [
                    {"text": json.dumps(body, default=json_serialize_datetime_objectId)}
                ],
            },
        }
        return message
