import os
import json
from datetime import datetime
from config import LOGS_DIR


class PipelineLogger:

    def __init__(self, video_filename):
        self.video_filename = video_filename
        self.start_time = datetime.now()
        self.end_time = None
        self.total_frames = 0
        self.processed_frames = 0
        self.errors = []

    def set_total_frames(self, total_frames):
        self.total_frames = total_frames

    def increment_processed_frames(self):
        self.processed_frames += 1

    def log_error(self, error_message):
        self.errors.append({
            "timestamp": datetime.now().isoformat(),
            "error": error_message
        })

    def build_report(self, face_stats, text_stats, audio_stats):
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()

        report = {
            "video_filename": self.video_filename,
            "processed_at": self.start_time.isoformat(),
            "processing_duration_seconds": round(duration, 2),
            "total_frames": self.total_frames,
            "processed_frames": self.processed_frames,
            "face_blur": face_stats,
            "text_redaction": text_stats,
            "audio_redaction": audio_stats,
            "errors": self.errors,
            "requires_human_review": len(text_stats.get("flagged_frames", [])) > 0
        }

        return report

    def save(self, face_stats, text_stats, audio_stats):
        report = self.build_report(face_stats, text_stats, audio_stats)

        log_filename = f"{os.path.splitext(self.video_filename)[0]}_{self.start_time.strftime('%Y%m%d_%H%M%S')}.json"
        log_path = os.path.join(LOGS_DIR, log_filename)

        with open(log_path, "w") as f:
            json.dump(report, f, indent=4)

        print(f"Log saved to {log_path}")
        return log_path