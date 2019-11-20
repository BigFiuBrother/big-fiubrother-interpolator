import cv2


class FrameEditor:

    def __init__(self):
        self.label_separation = 10
        self.line_thickness = 5
        self.known_face_color = (36, 255, 12)
        self.unknown_face_color = (255, 36, 12)

    def edit(frame, faces):
        for face in faces:
            if face.is_match:
                color = self.known_face_color
                label = 'CONOCIDO({} %)'.format(
                    face.probability_classification * 100)
            else:
                color = self.unknown_face_color
                label = 'DESCONOCIDO'

            top_left, bottom_right = [tuple(point)
                                      for point in face.bounding_box]

            frame = cv2.rectangle(frame,
                                  top_left,
                                  bottom_right,
                                  color,
                                  self.line_thickness)

            cv2.putText(frame,
                        label,
                        (top_left[0], top_left[1] - self.label_separation),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        self.color)

        return frame
