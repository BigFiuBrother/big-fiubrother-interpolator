from big_fiubrother_core import QueueTask
from big_fiubrother_core.db import (
    Database,
    VideoChunk,
    Frame,
    Face
)
from os import path


class FetchVideoData(QueueTask):

    def __init__(self, configuration, input_queue, output_queue):
        super().__init__(input_queue)
        self.output_queue = output_queue
        self.configuration = configuration

    def init(self):
        self.db = Database(self.configuration['db'])

    def execute_with(self, message):
        video_chunk = self.db.session.query(VideoChunk)
                                     .get(message.video_chunk_id)

        frames_with_faces = (
            self.db.session
            .query(Frame, Face)
            .filter(Frame.video_chunk_id == message.video_chunk_id)
            .join(Face)
            .group_by(Frame.offset)
            .order_by(Frame.offset)
            .all()
        )

        self.output_queue({
            'frames_with_faces': frames_with_faces,
            'video_chunk': video_chunk
        })
