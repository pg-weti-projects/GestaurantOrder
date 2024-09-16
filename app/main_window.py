from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QThread
from engine import Engine
from ui.widget import Widget
from utils import Utils
from camera.gesture.fingers import FingersDetector
from camera.gesture.hand import GestureDetector
import cv2


class MainApp(QMainWindow):
    """
    Main window class for the GUI
    """
    def __init__(self, logger, mode):
        super().__init__()
        self.logger = logger
        self.utils = Utils(logger)
        self.engine = Engine(logger)
        self.engine_thread = None
        self.mode = mode
        self.__init_engine_thread()
        self.set_main_window_params()

        # Sample widget
        self.widget = Widget()
        self.setCentralWidget(self.widget)
        self.show_video_capture()

    def __init_engine_thread(self):
        self.engine_thread = QThread()
        self.engine.moveToThread(self.engine_thread)
        self.engine_thread.start()

    def show_video_capture(self):
        try:
            if self.mode == 'fingers':
                gesture_detector = FingersDetector(mode=self.mode)  # Initialize the gesture detector
                gesture_detector.capture_image()  # Start capturing and detecting
            else:
                gesture_detector = GestureDetector(mode=self.mode)  # Initialize the gesture detector
                gesture_detector.capture_image()  # Start capturing and detecting
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            cv2.destroyAllWindows()

    def set_main_window_params(self) -> None:
        """
        Set main window parameters
        """
        self.setWindowTitle("Gestaurant Order")
        monitor_size = self.utils.get_monitor_geometry()
        self.resize(monitor_size['width'], monitor_size['height'])
