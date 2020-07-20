from big_fiubrother_core import QueueTask
from big_fiubrother_core.db import Database
from big_fiubrother_core.storage import processed_storage


class StoreProcessedVideo(QueueTask):

    def __init__(self, configuration, input_queue, output_queue):
        super().__init__(input_queue)
        self.configuration = configuration
        self.output_queue = output_queue

    def init(self):
        self.db = Database(self.configuration['db'])
        self.storage = processed_storage(self.configuration['storage'])

    def execute_with(self, message):
        video_chunk = message['video_chunk']

        self.storage.store_file(video_chunk.id, message['filepath'])

        video_chunk.processed = True
        self.db.update()

        self.output_queue.put(video_chunk.id)

    def close(self):
        self.db.close()
