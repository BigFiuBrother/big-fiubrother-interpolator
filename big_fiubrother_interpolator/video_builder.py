from vidgear.gears import WriteGear


class VideoBuilder:

    def __init__(self, filename, width, height, fps):
        self.closed = False
        self.filepath = '{}.mp4'.format(filename)
        
        output_parameters = {
            "-vcodec":"libx264",
            "-movflags": "+dash",
            "-input_framerate": fps,
            "-output_dimensions": (width, height)
        }

        self._writer = WriteGear(output_filename=self.filepath,
                                **output_parameters)

        self._frame_count = 0
        self.fps = fps

    def add_frame(self, frame):
        assert not self.closed, "Can't add frame to closed VideoBuilder!"

        self._writer.write(frame)
        self._frame_count += 1

    def duration(self):
        return round(self._frame_count / self.fps, 3)

    def close(self):
        self.closed = True
        self._writer.close()

