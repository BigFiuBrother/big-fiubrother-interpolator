from big_fiubrother_core import QueueTask
from os import path


class InterpolateVideo(QueueTask):

    def __init__(self, configuration, input_queue, output_queue):
        super().__init__(input_queue)
        self.output_queue = output_queue
        self.configuration = configuration

    def init(self):
        self.db = Database(self.configuration['db'])

    def execute_with(self, message):
