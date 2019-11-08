from big_fiubrother_core import QueueTask
from big_fiubrother_core.db import (
    Database
)
from os import path


class FetchBoundingBoxes(QueueTask):

    def __init__(self, configuration, input_queue, output_queue):
        super().__init__(input_queue)
        self.output_queue = output_queue
        self.configuration = configuration

    def init(self):
        self.db = Database(self.configuration['db'])

    def execute_with(self, message):
