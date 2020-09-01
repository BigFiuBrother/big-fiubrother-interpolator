from big_fiubrother_core import QueueTask
from big_fiubrother_core.db import (
    Database,
    VideoChunk,
    Frame,
    Face,
    Person
)
from sqlalchemy.orm import joinedload
import logging


class FetchVideoData(QueueTask):

    def __init__(self, configuration, input_queue, output_queue):
        super().__init__(input_queue)
        self.output_queue = output_queue
        self.configuration = configuration

    def init(self):
        self.db = Database(self.configuration['db'])

    def execute_with(self, message):
        video_chunk_id = message.video_chunk_id

        video_chunk = self.fetch_video_chunk(video_chunk_id)

        self.output_queue.put(video_chunk)

    def fetch_video_chunk(self, id):
        options = joinedload(VideoChunk.frames).joinedload(Frame.faces).joinedload(Face.person)
        return self.db.session.query(VideoChunk).options(options).get(id)

    def close(self):
        self.db.close()
