import sys
from pipeline.video_processor import VideoProcessor


def main():
    filename = r"video_sample1.mp4"

    try:
        processor = VideoProcessor(filename)
        output_path = processor.process()
        print(f"Successfully processed: {output_path}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()