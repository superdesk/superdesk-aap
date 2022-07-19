import logging
from superdesk.publish.transmitters import FTPPublishService
from superdesk.publish import register_transmitter
from superdesk.errors import PublishFtpError
from superdesk.ftp import ftp_connect
from io import BytesIO
import datetime

errors = [PublishFtpError.ftpError().get_error_description()]
logger = logging.getLogger(__name__)


class notes_transmitter(FTPPublishService):
    def _transmit(self, queue_item, subscriber):
        config = queue_item.get('destination', {}).get('config', {})

        try:
            with ftp_connect(config) as ftp:
                filename = '{0}{1:03}'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M'),
                                              queue_item.get('published_seq_num', 0) % 1000)
                b = BytesIO(queue_item['encoded_item'])
                ftp.storbinary("STOR " + filename, b)
        except PublishFtpError:
            raise
        except Exception as ex:
            raise PublishFtpError.ftpError(ex, config)


register_transmitter('notes ftp', notes_transmitter(), errors)
