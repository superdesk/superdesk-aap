import logging
from superdesk.upload import bp, generate_response_for_file
from flask import current_app as app
from superdesk.errors import SuperdeskApiError

logger = logging.getLogger(__name__)

AAP_DOWNLOAD_PATH = 'aap-download'

PATH = f"/{AAP_DOWNLOAD_PATH}/<path:media_id>"


@bp.route(PATH, methods=["GET"])
def aap_download(media_id):
    """
    Endpoint that allows access to stored files without requiring authentication
    :param media_id:
    :return:
    """
    media_file = app.media.get_by_filename(media_id)
    if media_file:
        return generate_response_for_file(media_file)

    raise SuperdeskApiError.notFoundError("File not found on media storage.")
