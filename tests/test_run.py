from big_fiubrother_core.db import (
    VideoChunk,
    Frame,
    Face,
    Database
)
from big_fiubrother_core.messages import (
    AnalyzedVideoChunkMessage,
    encode_message
)
from big_fiubrother_core.message_clients.rabbitmq import (
    Publisher
)
from big_fiubrother_core.synchronization import ProcessSynchronizer
from big_fiubrother_core.storage import raw_storage
import test_helper
import unittest


class TestRun(unittest.TestCase):

    def setUp(self):
        self.configuration = test_helper.configuration()
        self.db = Database(self.configuration['db'])
        self.db.truncate_all()

        video_chunk = VideoChunk(camera_id='CAMERA_ID',
                                 timestamp=1.0)

        self.db.add(video_chunk)

        self.storage = raw_storage(self.configuration['storage'])

        self.storage.store_file(video_chunk.id, 'tests/resources/test.h264')

        self.synchronizer = ProcessSynchronizer(self.configuration['synchronization'])

        self.synchronizer.register_video_task(video_chunk.id)
        
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
        publisher = Publisher(self.configuration['publisher'])
        message = AnalyzedVideoChunkMessage(self.video_chunk_id)
        publisher.publish(encode_message(message))

    def tearDown(self):
        self.db.close()
        self.synchronizer.close()


if __name__ == '__main__':
    unittest.main()
