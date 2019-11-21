from big_fiubrother_core import QueueTask
from big_fiubrother_core.db import (
    Database,
    AnalyzedVideoChunk
)


class StoreInterpolatedVideoInDB(QueueTask):

    def __init__(self, configuration, input_queue):
        super().__init__(input_queue)
        self.configuration = configuration

    def init(self):
        self.db = Database(self.configuration['db'])

    def execute_with(self, message):
        video_chunk_id, payload = message

        analyzed_video_chunk = AnalyzedVideoChunk(
            video_chunk_id=video_chunk_id,
            payload=payload)

        self.db.add(analyzed_video_chunk)

    def close(self):
        self.db.close()
