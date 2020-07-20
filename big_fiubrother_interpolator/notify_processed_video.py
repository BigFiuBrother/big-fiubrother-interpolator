from big_fiubrother_core import QueueTask
from requests import post


class NotifyProcessedVideo(QueueTask):

    def __init__(self, configuration, input_queue):
        super().__init__(input_queue)
        self.configuration = configuration

    def execute_with(self, video_chunk_id):
        post(self.configuration['web_server_host'],
            json={'video_chunk_id': video_chunk_id})
