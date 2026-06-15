import cv2
import easyocr
from config import TEXT_DETECTION_CONFIDENCE, TEXT_BOX_COLOR

import torch

class TextRedactor:
    def __init__(self):
        gpu_available = torch.cuda.is_available()
        self.reader = easyocr.Reader(['en'], gpu=gpu_available)
        print(f"EasyOCR using GPU: {gpu_available}")
        self.text_regions_redacted_count = 0
        self.flagged_frames = []

    def process_frame(self, frame, frame_number=None):
        results = self.reader.readtext(frame)

        for (bbox, text, confidence) in results:
            if confidence >= TEXT_DETECTION_CONFIDENCE:
                points = [list(map(int, point)) for point in bbox]
                x_coords = [p[0] for p in points]
                y_coords = [p[1] for p in points]
                x_min, x_max = max(0, min(x_coords)), max(x_coords)
                y_min, y_max = max(0, min(y_coords)), max(y_coords)

                cv2.rectangle(
                    frame,
                    (x_min, y_min),
                    (x_max, y_max),
                    TEXT_BOX_COLOR,
                    thickness=-1
                )
                self.text_regions_redacted_count += 1

                if frame_number is not None:
                    self.flagged_frames.append({
                        "frame": frame_number,
                        "text_detected": text,
                        "confidence": round(confidence, 2)
                    })

        return frame

    def get_stats(self):
        return {
            "total_text_regions_redacted": self.text_regions_redacted_count,
            "flagged_frames": self.flagged_frames
        }