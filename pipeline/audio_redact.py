import os
import json
import whisper
import subprocess
from config import SENSITIVE_KEYWORDS, WHISPER_MODEL, OUTPUT_DIR


class AudioRedactor:

    def __init__(self):
        self.model = whisper.load_model(WHISPER_MODEL)
        self.muted_segments = []

    def _has_audio(self, video_path):
        command = [
            "ffprobe", "-v", "quiet",
            "-print_format", "json",
            "-show_streams",
            video_path
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        streams = json.loads(result.stdout).get("streams", [])
        return any(s["codec_type"] == "audio" for s in streams)

    def transcribe(self, video_path):
        result = self.model.transcribe(video_path)
        return result["segments"]

    def find_sensitive_segments(self, segments):
        sensitive_segments = []
        for segment in segments:
            text = segment["text"].lower()
            for keyword in SENSITIVE_KEYWORDS:
                if keyword in text:
                    sensitive_segments.append({
                        "start": segment["start"],
                        "end": segment["end"],
                        "text": segment["text"].strip(),
                        "keyword_matched": keyword
                    })
                    break
        return sensitive_segments

    def mute_segments(self, video_path, sensitive_segments, output_filename):
        if not sensitive_segments:
            return video_path

        filters = []
        for segment in sensitive_segments:
            start = segment["start"]
            end = segment["end"]
            filters.append(f"volume=enable='between(t,{start},{end})':volume=0")

        filter_string = ", ".join(filters)
        output_path = os.path.join(OUTPUT_DIR, f"audio_{output_filename}")

        command = [
            "ffmpeg", "-i", video_path,
            "-af", filter_string,
            "-c:v", "copy",
            output_path,
            "-y"
        ]

        subprocess.run(command, check=True)
        self.muted_segments = sensitive_segments
        return output_path

    def process(self, video_path, output_filename):
        if not self._has_audio(video_path):
            print("No audio stream found, skipping audio redaction.")
            return video_path

        print("Transcribing audio...")
        segments = self.transcribe(video_path)

        print("Finding sensitive segments...")
        sensitive_segments = self.find_sensitive_segments(segments)

        print(f"Found {len(sensitive_segments)} sensitive segments, muting...")
        return self.mute_segments(video_path, sensitive_segments, output_filename)

    def get_stats(self):
        return {
            "total_muted_segments": len(self.muted_segments),
            "muted_segments": self.muted_segments
        }