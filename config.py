import os

# Paths
INPUT_DIR = "input"
OUTPUT_DIR = "output"
LOGS_DIR = "logs"

# Face blur settings
FACE_DETECTION_CONFIDENCE = 0.5
BLUR_KERNEL_SIZE = (99, 99)
BLUR_SIGMA = 30

# Text redaction settings
TEXT_DETECTION_CONFIDENCE = 0.5
TEXT_BOX_COLOR = (0, 0, 0)  # Black rectangle

# Audio redaction settings
SENSITIVE_KEYWORDS = [
    "name", "address", "date of birth", "phone",
    "email", "social security", "password"
]
WHISPER_MODEL = "base"  # options: tiny, base, small, medium, large

# Video processing settings
SUPPORTED_FORMATS = [".mp4", ".avi", ".mov", ".mkv"]

# Ensure directories exist
for directory in [INPUT_DIR, OUTPUT_DIR, LOGS_DIR]:
    os.makedirs(directory, exist_ok=True)