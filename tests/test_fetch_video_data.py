from big_fiubrother_core.db import (
    VideoChunk,
    Frame,
    Face,
    Database
)
import test_helper
import unittest


class TestFetchVideoData(unittest.TestCase):

    def setUp(self):
        self.configuration = test_helper.configuration()
        self.db = Database(self.configuration['db'])
        self.db.truncate_all()

        video_chunk = VideoChunk(camera_id='CAMERA_ID',
                                 timestamp=1.0,
                                 payload=b'asd')

        self.db.add(video_chunk)

        self.id = video_chunk.id

    def test_execute(self):
        video_chunk = self.db.session.query(VideoChunk).get(self.id)

        self.assertEqual(video_chunk.camera_id, 'CAMERA_ID')
        self.assertEqual(video_chunk.timestamp, 1.0)
        self.assertEqual(video_chunk.payload, b'asd')

    def tearDown(self):
        self.db.close()


if __name__ == '__main__':
    unittest.main()
