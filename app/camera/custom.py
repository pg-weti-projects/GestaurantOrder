from abc import ABC
import cv2
import mediapipe as mp
from PySide6.QtCore import Signal
from cvzone import HandTrackingModule


class Camera(ABC):
    """
    Abstract class for cameras.
    """
    frame_captured = Signal(object)

    def __init__(self, mode='fingers'):
        """
            Initialize the Camera object.

            mode (str): The mode of the camera. Options are 'fingers' for finger detection
                        or 'mediapipe' for gesture detection using MediaPipe. Default is 'fingers'.
        """
        super().__init__()
        self.cap = cv2.VideoCapture(1)
        self.hand = HandTrackingModule.HandDetector()
        self.mode = mode

        if self.mode == 'mediapipe':
            self.mp_hands = mp.solutions.hands.Hands(
                static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
            self.mp_draw = mp.solutions.drawing_utils

        if not self.cap.isOpened():
            raise ValueError("Could not open video stream from selected camera!")

    def capture_image(self):
        """
            Capture image frames for two modes:
            - mediapipe: Gesture detection
            - fingers: Fingers detection
        """
        while self.cap.isOpened():
            ret, frame = self.cap.read()

            if not ret:
                print("Warning: Frame capture failed. Retrying...")
                continue

            hands, frame = self.hand.findHands(frame)

            if ret and self.mode == 'fingers':
                gestures = self.detect_gesture(hands)
                self.display_gestures(frame, gestures)
                cv2.imshow('Web', frame)
            elif ret and self.mode == 'mediapipe':
                gestures = self.detect_gesture(frame)
                self.display_gestures(frame, gestures)
                cv2.imshow('Web', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()

    def detect_gesture(self, hands):
        pass

    def display_gestures(self, frame, gestures):
        pass

    def __del__(self):
        self.cap.release()
