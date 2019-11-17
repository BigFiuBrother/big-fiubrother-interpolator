from big_fiubrother_core import QueueTask
from big_fiubrother_core.db import (
    Database,
    VideoChunk,
    Frame,
    Face
)
from collections import defaultdict


class FetchVideoData(QueueTask):

    def __init__(self, configuration, input_queue, output_queue):
        super().__init__(input_queue)
        self.output_queue = output_queue
        self.configuration = configuration

    def init(self):
        self.db = Database(self.configuration['db'])

    def execute_with(self, message):
        video_chunk = (
            self.db.session
            .query(VideoChunk)
            .get(message.video_chunk_id)
        )

        faces_with_offset = (
            self.db.session
            .query(Frame.offset, Face)
            .filter(Frame.video_chunk_id == message.video_chunk_id)
            .filter(Frame.id == Face.frame_id)
            .order_by(Frame.offset)
            .all()
        )

        faces_by_offset = defaultdict(list)

        for offset, face in faces_with_offset:
            faces_by_offset[offset].append(face)

        self.output_queue.put({
            'faces_by_offset': faces_by_offset,
            'video_chunk': video_chunk
        })
