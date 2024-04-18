from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QGuiApplication

from .widget import Widget


class MainWindow(QMainWindow):
    """
    Main window class for the GUI
    """
    def __init__(self, logger):
        super().__init__()
        self.__logger = logger
        self.__monitor_size = self.__get_monitor_geometry()
        self.setWindowTitle("Gestaurant Order")
        self.resize(self.__monitor_size['width'], self.__monitor_size['height'])

        # Sample widget
        self.widget = Widget()
        self.setCentralWidget(self.widget)

    def __get_monitor_geometry(self) -> dict:
        """
        Gets primary monitor geometry ( width and height )

        Returns:
            Monitor width and height
        """
        monitor = QGuiApplication.primaryScreen().geometry()
        m_width = monitor.width()
        m_height = monitor.height()
        self.__logger.info(f"Size of your primary monitor: {m_width}x{m_height}")

        return {"width": m_width, "height": m_height}
