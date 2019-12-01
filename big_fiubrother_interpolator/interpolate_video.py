from big_fiubrother_core import QueueTask
from . import (
    InterpolationIterator,
    VideoBuilder,
    FrameEditor
)
import os


class InterpolateVideo(QueueTask):

    def __init__(self, configuration, input_queue, output_queue):
        super().__init__(input_queue)
        self.output_queue = output_queue
        self.configuration = configuration

    def init(self):
        self.tmp_path = self.configuration['tmp_path']

    def execute_with(self, message):
        video_capture = cv2.VideoCapture(message['filepath'])

        iterator = InterpolationIterator(
            video_capture=video_capture,
            faces_by_offset=message['faces_by_offset'])

        video_builder = VideoBuilder(
            width=int(video_capture.get(3)),
            height=int(video_capture.get(4)),
            fps=self.configuration['interpolation_fps']
        )

        frame_editor = FrameEditor()

        for frame, faces in iterator:
            new_frame = frame_editor.edit(frame, faces)
            video_builder.add_frame(new_frame)

        os.remove(message['filepath'])

        video_chunk = message['video_chunk']

        filepath = path.join(
            self.tmp_path,
            '{}.mp4'.format(video_chunk.filename()))

        self.output_queue.put((
            video_chunk,
            video_builder.build(filepath)
        ))
