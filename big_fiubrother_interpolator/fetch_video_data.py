from big_fiubrother_core import QueueTask
from big_fiubrother_core.db import (
    Database,
    VideoChunk,
    Frame,
    Face,
    Person
)
from big_fiubrother_core.synchronization import ProcessSynchronizer
from collections import defaultdict
import logging


class FetchVideoData(QueueTask):

    def __init__(self, configuration, input_queue, output_queue):
        super().__init__(input_queue)
        self.output_queue = output_queue
        self.configuration = configuration

    def init(self):
        self.db = Database(self.configuration['db'])
        self.synchronizer = ProcessSynchronizer(self.configuration['synchronization'])

    def execute_with(self, message):
        is_finished, remaining_tasks = self.synchronizer.is_video_task_finished(message.video_chunk_id)

        if not is_finished:
            logging.debug(f"{message.video_chunk_id} has not finished processing. {remaining_tasks} tasks remaining!")
            return

        video_chunk = self.db.session.query(VideoChunk)
            .options(joinedload(VideoChunk.frames)
                .joinedload(Frame.faces)
                .joinedload(Face.person))
            .get(message.video_chunk_id)

        self.output_queue.put(video_chunk)

    def close(self):
        self.db.close()
