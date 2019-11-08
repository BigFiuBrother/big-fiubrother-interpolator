from big_fiubrother_core import QueueTask
from big_fiubrother_core.db import (
    Database,
    VideoChunk
)
from os import path


class FetchVideoChunk(QueueTask):

    def __init__(self, configuration, input_queue, output_queue):
        super().__init__(input_queue)
        self.output_queue = output_queue
        self.configuration = configuration

    def init(self):
        self.tmp_path = self.configuration['tmp_path']
        self.db = Database(self.configuration['db'])

    def execute_with(self, message):
        video_chunk = (
            self.db.session
            .query(VideoChunk)
            .filter_by(id=message.video_chunk_id)
        )

        filepath = path.join(self.tmp_path, video_chunk.filename)

        with open(filepath, 'wb') as file:
            file.write(video_chunk.payload)

        self.output_queue({
            'path': filepath,
            'frame_ids': message.frame_ids,
            'camera_id': video_chunk.camera_id,
            'timestamp': video_chunk.timestamp 
        })
