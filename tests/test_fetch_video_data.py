from big_fiubrother_core.db import (
    VideoChunk,
    Frame,
    Face,
    Database
)
from big_fiubrother_core.messages import (
    AnalyzedVideoChunkMessage
)
from big_fiubrother_interpolator import (
    FetchVideoData
)
from queue import Queue
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

        frame = Frame(offset=0,
                      video_chunk_id=video_chunk.id)

        self.db.add(frame)

        self.bounding_box = [
            [10.0, 10.0],
            [20.0, 20.0]
        ]

        face = Face(
            frame_id=frame.id,
            bounding_box=self.bounding_box
        )

        self.db.add(face)

        self.id = video_chunk.id

    def test_execute(self):
        input_queue = Queue()
        output_queue = Queue()

        task = FetchVideoData(
            configuration=self.configuration,
            input_queue=input_queue,
            output_queue=output_queue)

        with test_helper.start_task(task):
            message = AnalyzedVideoChunkMessage(
                video_chunk_id=self.id)

            input_queue.put(message)
            input_queue.join()

        output_message = output_queue.get(block=False)

        video_chunk = output_message['video_chunk']
        self.assertEqual(video_chunk.camera_id, 'CAMERA_ID')
        self.assertEqual(video_chunk.timestamp, 1.0)
        self.assertEqual(video_chunk.payload, b'asd')

        faces_by_offset = output_message['faces_by_offset']
        self.assertEqual([*faces_by_offset.keys()], [0])

        faces = faces_by_offset[0]
        self.assertEqual(len(faces), 1)
        self.assertEqual(faces[0].bounding_box, self.bounding_box)

    def tearDown(self):
        self.db.close()


if __name__ == '__main__':
    unittest.main()
