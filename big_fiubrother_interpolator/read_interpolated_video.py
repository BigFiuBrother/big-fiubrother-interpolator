from big_fiubrother_core import QueueTask
from big_fiubrother_core.messages import VideoChunkMessage
import os


class ReadInterpolatedVideo(QueueTask):

    def __init__(self, input_queue, publisher_queue, storage_queue):
        super().__init__(input_queue)
        self.publisher_queue = publisher_queue
        self.storage_queue = storage_queue

    def execute_with(self, message):
        raw_video_chunk, filepath = message

        with open(filepath, 'rb') as file:
            interpolated_video_chunk = file.read()

        video_chunk_message = VideoChunkMessage(
            camera_id=raw_video_chunk.camera_id,
            timestamp=raw_video_chunk.timestamp,
            payload=interpolated_video_chunk)

        self.publisher_queue.put(video_chunk_message)

        self.storage_queue.put((
            video_chunk.id,
            interpolated_video_chunk
        ))

        os.remove(filepath)
