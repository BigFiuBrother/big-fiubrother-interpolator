import cv2


class FrameEditor:

    def __init__(self):
        self.label_separation = 10
        self.line_thickness = 5
        self.known_face_color = (36, 255, 12)
        self.unknown_face_color = (255, 36, 12)

    def edit(self, frame, faces):
        for face in faces:
            if face.is_match:
                color = self.known_face_color
                label = '{} ({} %)'.format(
                    face.person.name.upper(),
                    face.probability_classification * 100)
            else:
                color = self.unknown_face_color
                label = 'UNKNOWN'

            top_left, bottom_right = [tuple(point) for point in face.bounding_box]

            frame = cv2.rectangle(frame,
                                  top_left,
                                  bottom_right,
                                  color,
                                  self.line_thickness)

            cv2.putText(img=frame,
                        text=label,
                        org=(top_left[0], top_left[1] - self.label_separation),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1,
                        color=color)

        return frame
