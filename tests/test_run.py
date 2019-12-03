from big_fiubrother_core.db import (
    VideoChunk,
    Frame,
    Face,
    Database
)
from big_fiubrother_core.messages import (
    AnalyzedVideoChunkMessage
)
from big_fiubrother_core.message_clients.rabbitmq import (
    Publisher
)
import test_helper
import unittest


class TestRun(unittest.TestCase):

    def setUp(self):
        self.configuration = test_helper.configuration()
        self.db = Database(self.configuration['db'])
        self.db.truncate_all()

        with open('resources/test.h264', 'rb') as file:
            payload = file.read()

        video_chunk = VideoChunk(camera_id='CAMERA_ID',
                                 timestamp=1.0,
                                 payload=payload)

        self.db.add(video_chunk)
        
        bounding_boxes = [
            [[602, 380], [289, 286]],
            [[604, 378], [296, 287]],
            [[604, 363], [316, 297]],
            [[633, 364], [310, 320]]
        ]

        for i, bounding_box in enumerate(bounding_boxes):
            frame = Frame(offset=i*6,
                          video_chunk_id=video_chunk.id)

            self.db.add(frame)

            face = Face(
                frame_id=frame.id,
                bounding_box=bounding_box
            )

            self.db.add(face)

        self.video_chunk_id = video_chunk.id

    def test_execute(self):
        publisher = Publisher(self.configuration['input_publisher'])
        message = AnalyzedVideoChunkMessage(self.video_chunk_id)
        publisher.publish(message)

    def tearDown(self):
        self.db.close()


if __name__ == '__main__':
    unittest.main()
