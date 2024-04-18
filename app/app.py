from PySide6.QtWidgets import QApplication
import sys
import tomllib

from logger import Logger
from widgets.main_window import MainWindow


def create_app(logger) -> None:
    """
    Creates app instance.

    Returns:
        App instance
    """
    app = QApplication(sys.argv)

    main_window = MainWindow(logger)
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    logger = Logger("LOGGER").get_logger()

    try:
        with open("config.toml", "rb") as cfg_file:
            cfg = tomllib.load(cfg_file)
    except FileNotFoundError:
        logger.error("Could not find config.toml file!")
        sys.exit(1)

    logger.info("Application starting")
    create_app(logger)
