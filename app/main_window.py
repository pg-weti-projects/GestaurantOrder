from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QThread
from camera.custom import Camera
from engine import Engine
from ui.widget import Widget
from utils import Utils


class MainApp(QMainWindow):
    """
    Main window class for the GUI
    """
    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        self.utils = Utils(logger)
        self.engine = Engine(logger)
        self.engine_thread = None
        self.__init_engine_thread()
        self.set_main_window_params()

        # Sample widget
        self.widget = Widget()
        self.setCentralWidget(self.widget)

        self.camera = Camera()
        self.camera.capture_image()

    def __init_engine_thread(self):
        self.engine_thread = QThread()
        self.engine.moveToThread(self.engine_thread)
        self.engine_thread.start()

    def set_main_window_params(self) -> None:
        """
        Set main window parameters
        """
        self.setWindowTitle("Gestaurant Order")
        monitor_size = self.utils.get_monitor_geometry()
        self.resize(monitor_size['width'], monitor_size['height'])
