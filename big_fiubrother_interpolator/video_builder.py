from vidgear.gears import WriteGear


class VideoBuilder:

    def __init__(self, filename, width, height, fps):
        self.filepath = '{}.mp4'.format(filename)
        
        output_parameters = {
            "-vcodec":"libx264",
            "-movflags": "+dash",
            "-input_framerate": fps,
            "-output_dimensions": (width, height)
        }

        self.writer = WriteGear(output_filename=self.filepath,
                                **output_parameters)

    def add_frame(self, frame):
        self.writer.write(frame)

    def close(self):
        self.writer.close()
