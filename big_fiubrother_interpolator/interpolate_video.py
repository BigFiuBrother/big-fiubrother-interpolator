from big_fiubrother_core import QueueTask
from . import InterpolationIterator
import os


class InterpolateVideo(QueueTask):

    def __init__(self, configuration, input_queue, output_queue):
        super().__init__(input_queue)
        self.output_queue = output_queue
        self.configuration = configuration

    def init(self):
        self.db = Database(self.configuration['db'])

    def execute_with(self, message):
        iterator = InterpolationIterator(
            video_path=message['filepath'], 
            faces_by_offset=message['faces_by_offset'])

        for frame, faces in iterator:
            #TODO: process video
            
        os.remove(message['filepath'])
