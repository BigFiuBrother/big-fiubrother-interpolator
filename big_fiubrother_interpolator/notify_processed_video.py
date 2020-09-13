from big_fiubrother_core import QueueTask
from requests import post
import logging


class NotifyProcessedVideo(QueueTask):

    def __init__(self, configuration, input_queue):
        super().__init__(input_queue)
        self.configuration = configuration

    def execute_with(self, message):
        try:
            post(self.configuration['web_server_host'],
                json=message)

            logging.info("Sent {} to web server".format(message['video_chunk_id']))
        except e:
            logging.error(e)
