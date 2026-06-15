import cv2
from config import BLUR_KERNEL_SIZE, BLUR_SIGMA

class FaceBlur:

    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.faces_detected_count = 0

    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        for (x, y, w, h) in faces:
            face_region = frame[y:y+h, x:x+w]
            blurred = cv2.GaussianBlur(face_region, BLUR_KERNEL_SIZE, BLUR_SIGMA)
            frame[y:y+h, x:x+w] = blurred
            self.faces_detected_count += 1

        return frame

    def get_stats(self):
        return {"total_faces_detected": self.faces_detected_count}

    def close(self):
        pass