import cv2
from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QImage


class UserCamera(QObject):
    frame_ready = Signal(QImage)

    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.running = True

        if not self.cap.isOpened():
            raise ValueError("Could not open video stream from selected camera!")

    def capture_image(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                flipped_frame = cv2.flip(gray_frame, 1)

                h, w = flipped_frame.shape
                q_img = QImage(flipped_frame.data, w, h, w, QImage.Format_Grayscale8)

                self.frame_ready.emit(q_img)

    def stop(self):
        self.running = False

    def __del__(self):
        self.cap.release()

