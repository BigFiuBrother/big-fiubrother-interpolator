from big_fiubrother_core import QueueTask
from queue import deque
import cv2
import os


class InterpolateVideo(QueueTask):

    def __init__(self, configuration, input_queue, output_queue):
        super().__init__(input_queue)
        self.output_queue = output_queue
        self.configuration = configuration

    def init(self):
        self.db = Database(self.configuration['db'])

    def execute_with(self, message):
        cap = cv2.VideoCapture(message['filepath'])

        queue = deque(message['frames_with_faces'].keys())
        offset = 0
        faces = None

        while True:
            if offset == queue.index(0):
                faces = queue.popleft()
                
            ret, frame = cap.read()

            if ret:
                #TODO: Process video
                offset += 1
            else:
                break

        cap.release()

        os.remove(message['filepath'])
