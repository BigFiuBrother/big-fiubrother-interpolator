from big_fiubrother_core import QueueTask
from big_fiubrother_core.db import (
    Database
)
from os import path


class StoreVideoInFileSystem(QueueTask):

    def __init__(self, configuration, input_queue, output_queue):
        super().__init__(input_queue)
        self.output_queue = output_queue
        self.configuration = configuration

    def init(self):
        self.tmp_path = self.configuration['tmp_path']

    def execute_with(self, message):
        video_chunk = message['video_chunk']
        filepath = path.join(self.tmp_path, video_chunk.filename)

        with open(filepath, 'wb') as file:
            file.write(video_chunk.payload)

        message['filepath'] = filepath

        self.output_queue.put(message)
