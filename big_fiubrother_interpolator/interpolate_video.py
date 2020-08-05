from big_fiubrother_core import QueueTask
from . import (
    InterpolationIterator,
    VideoBuilder,
    FrameEditor
)
from uuid import uuid4 as uuid
import cv2
import os


class InterpolateVideo(QueueTask):

    def __init__(self, configuration, input_queue, output_queue):
        super().__init__(input_queue)
        self.output_queue = output_queue
        self.configuration = configuration

    def execute_with(self, message):
        video_capture = cv2.VideoCapture(message['filepath'])

        iterator = InterpolationIterator(
            video_capture=video_capture,
            frames=message['video_chunk'].frames)

        video_builder = VideoBuilder(
            filename=os.path.join('tmp', str(uuid())),
            width=int(video_capture.get(3)),
            height=int(video_capture.get(4)),
            fps=self.configuration['interpolation_fps']
        )

        frame_editor = FrameEditor()

        for frame, faces in iterator:
            new_frame = frame_editor.edit(frame, faces)
            video_builder.add_frame(new_frame)

        video_builder.close()

        os.remove(message['filepath'])
        
        message['filepath'] = video_builder.filepath

        self.output_queue.put(message)
