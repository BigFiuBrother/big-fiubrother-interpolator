from big_fiubrother_core import QueueTask
from big_fiubrother_core.storage import raw_storage
from os import path


class FetchVideoChunk(QueueTask):

    def __init__(self, configuration, input_queue, output_queue):
        super().__init__(input_queue)
        self.output_queue = output_queue
        self.configuration = configuration

    def init(self):
        self.storage = raw_storage(self.configuration['storage'])

    def execute_with(self, video_chunk):
        filepath = path.join('tmp', '{}.h264'.format(video_chunk.id))

        self.storage.retrieve_file(video_chunk.id, filepath)

        self.output_queue.put({
            'filepath': filepath,
            'video_chunk': video_chunk
        })
