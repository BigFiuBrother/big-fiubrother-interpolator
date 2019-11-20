import cv2


class VideoBuilder:

    def __init__(self, witdh, height, fps):
        self.frames = []
        self.width = width
        self.height = height
        self.fps = fps

    def add_frame(self, frame):
        self.frames.append(frame)

    def build(self, filename):
        video_writer = cv2.VideoWriter('{}.mp4'.format(filename),
                                       cv2.VideoWriter_fourcc(*'mp4v'),
                                       self.fps,
                                       (self.width, self.height))

        for frame in self.frames:
            video_writer.write(frame)

        video_writer.release()