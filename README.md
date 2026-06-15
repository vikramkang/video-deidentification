# Video De-identification Pipeline

A Python pipeline that automatically detects and redacts faces, 
on-screen text, and sensitive audio from video files.

## Tools Used
- MediaPipe — face detection
- EasyOCR — text detection
- Whisper — audio transcription and redaction
- OpenCV — frame processing
- FFmpeg — audio/video merging