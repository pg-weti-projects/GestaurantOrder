from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtGui import QImage

from camera.user_camera import UserCamera


class Engine(QObject):
    frame_ready = Signal(QImage)

    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        self.camera = UserCamera(self.logger)

        self.camera_thread = QThread()
        self.camera.moveToThread(self.camera_thread)
        self.camera.frame_ready.connect(self.process_frame)
        self.camera_thread.started.connect(self.camera.capture_image)

    def start(self):
        self.camera_thread.start()

    def stop(self):
        self.camera.stop()
        self.camera_thread.quit()
        self.camera_thread.wait()

    def process_frame(self, frame):
        self.frame_ready.emit(frame)
