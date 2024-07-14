import logging
from PySide6.QtGui import QGuiApplication


class Utils:
    def __init__(self, logger):
        self.__logger = logger

    def get_monitor_geometry(self) -> dict:
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
    
    
class Logger:
    """
    Class for configuring and obtaining a logger.
    """
    def __init__(self, name: str):
        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.__logger.addHandler(console_handler)

        file_handler = logging.FileHandler("../logs/logs.log")
        file_handler.setFormatter(formatter)
        self.__logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        """
        Returns the logger instance.

        Returns:
            The logger instance.
        """
        return self.__logger
