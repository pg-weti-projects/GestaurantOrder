from camera.gesture.fingers import FingersDetector
from camera.gesture.hands import GestureDetector
import logging
from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtGui import QImage

logger = logging.getLogger("app")

class Engine(QObject):
    frame_ready = Signal(QImage)
    gesture_detected = Signal(str)

    def __init__(self, mode: str):
        super().__init__()
        self.mode = mode

        # Initialize the appropriate detector based on the mode
        if self.mode == 'fingers':
            self.detector = FingersDetector(mode=self.mode)
        elif self.mode == 'mediapipe':
            self.detector = GestureDetector(mode=self.mode)
        else:
            raise ValueError(f"Unknown mode: {self.mode}")

        self.camera_thread = QThread()
        self.detector.moveToThread(self.camera_thread)
        self.detector.frame_ready.connect(self.process_frame)
        self.detector.gesture_detected.connect(self.handle_gesture)
        self.camera_thread.started.connect(self.detector._capture_image)

    def start(self):
        """Starts camera thread"""
        self.camera_thread.start()

    def stop(self):
        """Stops detection and camera thread"""
        self.detector.stop()
        self.camera_thread.quit()
        self.camera_thread.wait()

    def process_frame(self, frame: QImage) -> None:
        """Emits frame signal ( QImage object )."""
        self.frame_ready.emit(frame)

    @Slot(str)
    def handle_gesture(self, gesture: str) -> None:
        """
        Emits detected gesture detection further.

        Args:
            gesture: Detected gesture name.
        """
        self.gesture_detected.emit(gesture)
