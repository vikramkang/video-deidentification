import cv2
import mediapipe as mp
from config import BLUR_KERNEL_SIZE, BLUR_SIGMA


class FaceBlur:

    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=0,
            min_detection_confidence=0.5
        )
        self.faces_detected_count = 0

    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb_frame)

        if results.detections:
            h, w, _ = frame.shape
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                x = max(0, int(bbox.xmin * w))
                y = max(0, int(bbox.ymin * h))
                width = min(int(bbox.width * w), w - x)
                height = min(int(bbox.height * h), h - y)

                face_region = frame[y:y + height, x:x + width]
                blurred = cv2.GaussianBlur(face_region, BLUR_KERNEL_SIZE, BLUR_SIGMA)
                frame[y:y + height, x:x + width] = blurred
                self.faces_detected_count += 1

        return frame

    def get_stats(self):
        return {"total_faces_detected": self.faces_detected_count}

    def close(self):
        self.face_detection.close()