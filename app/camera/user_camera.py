import logging
import time
from abc import abstractmethod
import cv2
from cvzone import HandTrackingModule
import mediapipe as mp
import os
from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QImage

logger = logging.getLogger("app")

class UserCamera(QObject):
    frame_ready = Signal(QImage)
    gesture_detected = Signal(str)

    def __init__(self, mode):
        """
        Initialize the Camera object.

        mode (str): The mode of the camera. Options are 'fingers' for finger detection
                    or 'mediapipe' for gesture detection using MediaPipe. Default is 'fingers'.
        """
        super().__init__()
        self.cap = cv2.VideoCapture(int(os.getenv('CAMERA_NUMBER')))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.running = True

        self.hand = HandTrackingModule.HandDetector()
        self.mode = mode
        self.last_gesture: str | None = None
        self.last_save_time = 0
        self.save_interval = 1


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
        while self.running:
            ret, frame = self.cap.read()
            if ret:

                if ret and self.mode == 'fingers':
                    # Process finger detection
                    hands, frame = self.hand.findHands(frame)
                    gestures = self.detect_gesture(hands)
                    gestures = self.display_gestures(frame, gestures)

                elif ret and self.mode == 'mediapipe':
                    # Process gesture detection with MediaPipe
                    gestures = self.detect_gesture(frame)
                    gestures = self.display_gestures(frame, gestures)

                current_time = time.time()
                if gestures != self.last_gesture and current_time - self.last_save_time >= self.save_interval:
                    self.last_gesture = gestures
                    self.gesture_detected.emit(self.last_gesture)
                    self.last_save_time = current_time

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Get image dimensions
                h, w, ch = rgb_frame.shape

                # Create a QImage from the RGB frame
                q_img = QImage(rgb_frame.data, w, h, w * ch, QImage.Format_RGB888)

                self.frame_ready.emit(q_img)

    @abstractmethod
    def detect_gesture(self, hands):
        pass

    @abstractmethod
    def display_gestures(self, frame, gestures):
        pass

    def stop(self):
        self.running = False

    def __del__(self):
        self.cap.release()
