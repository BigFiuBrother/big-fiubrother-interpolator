from big_fiubrother_core import VideoIterator
from queue import deque


class InterpolationIterator:

    def __init__(self, video_capture, faces_by_offset):
        self.video_iterator = VideoIterator(video_capture)
        self.faces_by_offset = faces_by_offset

    def __iter__(self):
        self.all_faces = deque(faces_by_offset.items())
        self.faces_offset, self.faces = self.all_faces.popleft()
        return self

    def __next__(self):
        offset, frame = self.video_iterator.next()

        if len(self.all_faces) > 0 and offset >= self.faces_offset:
            self.faces_offset, self.faces = self.all_faces.popleft()

        return frame, self.faces
