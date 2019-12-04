from big_fiubrother_core import QueueTask
from big_fiubrother_core.messages import VideoChunkMessage
import os


class ReadInterpolatedVideo(QueueTask):

    def __init__(self, input_queue, publisher_queue, storage_queue):
        super().__init__(input_queue)
        self.publisher_queue = publisher_queue
        self.storage_queue = storage_queue

    def execute_with(self, message):
        with open(message['filepath'], 'rb') as file:
            interpolated_video_chunk = file.read()

        video_chunk_message = VideoChunkMessage(
            camera_id=message['camera_id'],
            timestamp=message['timestamp'],
            payload=interpolated_video_chunk)

        self.publisher_queue.put(video_chunk_message)

        self.storage_queue.put((
            message['video_chunk_id'],
            interpolated_video_chunk
        ))

        os.remove(message['filepath'])
