from big_fiubrother_core import VideoIterator
from queue import deque


class InterpolationIterator:

    def __init__(self, video_capture, frames_metadata):
        self.video_iterator = VideoIterator(video_capture)
        self.frames_metadata = frames_metadata

    def __iter__(self):
        self.frames_metadata_queue = deque(frames)
        self.current_frame_metadata = None
        return self

    def __next__(self):
        offset, frame = next(self.video_iterator)

        if len(self.frames_metadata_queue) > 0 and self.frames_metadata_queue[0].offset == offset:
            self.current_frame_metadata = self.frames_metadata_queue.popleft()

        faces = []

        if self.current_frame_metadata is not None:
            faces = self.current_frame_metadata.faces

        return frame, faces