from abc import ABC
import cv2
from PySide6.QtCore import Signal
from cvzone import HandTrackingModule


class Camera(ABC):
    """
    Abstract class for cameras.
    """
    frame_captured = Signal(object)

    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(1)
        self.hand = HandTrackingModule.HandDetector()

        if not self.cap.isOpened():
            raise ValueError("Could not open video stream from selected camera!")

    def capture_image(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            hands, frame = self.hand.findHands(frame)
            if not ret:
                print("Warning: Frame capture failed. Retrying...")
                continue
            if ret:
                gestures = self.detect_gesture(hands)
                self.display_gestures(frame, gestures)
                cv2.imshow('Web', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                raise ValueError("Failed to capture image from camera!")
        self.cap.release()
        cv2.destroyAllWindows()

    def detect_gesture(self, hands):
        pass

    def display_gestures(self, frame, gestures):
        pass

    def __del__(self):
        self.cap.release()
