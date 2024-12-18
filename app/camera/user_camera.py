import logging
import time
from abc import abstractmethod
import cv2
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
        self._cap = cv2.VideoCapture(int(os.getenv('CAMERA_NUMBER')))
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        if not self._cap.isOpened():
            raise ValueError("Could not open video stream from selected camera!")

        self._running = True
        self._mode = mode
        self._last_gesture: str | None = None
        self._last_save_time = 0
        self._save_interval = 1

    def _capture_image(self):
        """
        This method continuously captures frames from the camera feed and processes them based on
        the selected mode ('fingers' or 'mediapipe').
        """
        while self._running:
            ret, frame = self._cap.read()
            if ret:

                gestures, frame = self.process_frame(frame)

                self._emit_gesture_signal(gestures)

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_frame.shape
                q_img = QImage(rgb_frame.data, w, h, w * ch, QImage.Format_RGB888)
                self.frame_ready.emit(q_img)

    def _emit_gesture_signal(self, gestures):
        """
        Emit gesture signal by the 1 second between detected gestures.
        """
        current_time = time.time()
        if gestures != self._last_gesture and current_time - self._last_save_time >= self._save_interval:
            self._last_gesture = gestures
            self.gesture_detected.emit(gestures)
            self._last_save_time = current_time

    @abstractmethod
    def detect_gesture(self, hands):
        pass

    @abstractmethod
    def display_gestures(self, frame, gestures):
        pass

    @abstractmethod
    def process_frame(self, frame):
        pass

    def stop(self):
        self._running = False

    def __del__(self):
        self._cap.release()
