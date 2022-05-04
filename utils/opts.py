import argparse


def parse_opt():
    parser = argparse.ArgumentParser(
        description="Server gets Raspberry pi's capture through zmq"
    )
    parser.add_argument("--input", type=str, default=0, help="input video")
    parser.add_argument(
        "--weights", type=str, default="data/yolov4_tiny.weights", help="yolo weights"
    )
    parser.add_argument(
        "--configure", type=str, default="data/yolov4_tiny.cfg", help="yolo configure"
    )
    parser.add_argument(
        "--label", type=str, default="data/coco.names", help="coco class label"
    )
    parser.add_argument(
        "--confidence", type=float, default=0.5, help="minimum confidence"
    )
    parser.add_argument(
        "--threshold", type=float, default=0.3, help="minimum threshold"
    )
    parser.add_argument(
        "--frame", type=int, default=10, help="threshold of frame count"
    )
    args = parser.parse_args()

    return args
