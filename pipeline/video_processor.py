import cv2
import os
from config import INPUT_DIR, OUTPUT_DIR, SUPPORTED_FORMATS
from pipeline.face_blur import FaceBlur
from pipeline.text_redact import TextRedactor
from pipeline.audio_redact import AudioRedactor
from pipeline.logger import PipelineLogger


class VideoProcessor:

    def __init__(self, filename):
        self.filename = filename
        self.input_path = os.path.join(INPUT_DIR, filename)
        self.output_path = os.path.join(OUTPUT_DIR, filename)
        self.logger = PipelineLogger(filename)

        self._validate_file()

        self.face_blur = FaceBlur()
        self.text_redactor = TextRedactor()
        self.audio_redactor = AudioRedactor()

    def _validate_file(self):
        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"Input file not found: {self.input_path}")

        ext = os.path.splitext(self.filename)[1].lower()
        if ext not in SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported file format: {ext}")

    def _get_video_writer(self, cap):
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return cv2.VideoWriter(self.output_path, fourcc, fps, (width, height))

    def _process_frames(self, cap, writer):
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.logger.set_total_frames(total_frames)
        frame_number = 0

        print(f"Processing {total_frames} frames...")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            try:
                frame = self.face_blur.process_frame(frame)
                frame = self.text_redactor.process_frame(frame, frame_number)
                writer.write(frame)
                self.logger.increment_processed_frames()

                if frame_number % 100 == 0:
                    print(f"Progress: {frame_number}/{total_frames} frames")

            except Exception as e:
                self.logger.log_error(f"Frame {frame_number}: {str(e)}")

            frame_number += 1

    def process(self):
        print(f"Starting pipeline for: {self.filename}")

        cap = cv2.VideoCapture(self.input_path)
        writer = self._get_video_writer(cap)

        try:
            self._process_frames(cap, writer)
        finally:
            cap.release()
            writer.release()
            self.face_blur.close()

        print("Frame processing complete. Starting audio redaction...")
        final_output = self.audio_redactor.process(self.output_path, self.filename)

        self.logger.save(
            face_stats=self.face_blur.get_stats(),
            text_stats=self.text_redactor.get_stats(),
            audio_stats=self.audio_redactor.get_stats()
        )

        print(f"Pipeline complete. Output saved to: {final_output}")
        return final_output