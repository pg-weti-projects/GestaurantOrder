from abc import ABC
import cv2


class Camera(ABC):
    """
    Abstract class for cameras.
    """
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            raise ValueError("Could not open video stream from selected camera!")

    def capture_image(self):
        pass

    def __del__(self):
        self.cap.release()
