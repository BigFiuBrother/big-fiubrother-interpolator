from big_fiubrother_interpolator import VideoBuilder
import unittest
import cv2


class TestVideoWriter(unittest.TestCase):

    def test(self):
        video_capture = cv2.VideoCapture("tests/resources/test.h264")

        builder = VideoBuilder(filename="tests/resources/output",
            width=1280,
            height=720,
            fps=24)

        ret = True

        while ret:
            ret, frame = video_capture.read()

            builder.add_frame(frame)

        video_capture.release()
        builder.close()


if __name__ == '__main__':
    unittest.main()



