import cv2


class VideoBuilder:

    def __init__(self, filename, width, height, fps):
        self.filepath = '{}.mp4'.format(filename)
        self.video_writer = cv2.VideoWriter(self.filepath,
                                            cv2.VideoWriter_fourcc(*'avc1'),
                                            fps,
                                            (width, height))

    def add_frame(self, frame):
        self.video_writer.write(frame)

    def release(self):
        self.video_writer.release()
