from PySide6.QtWidgets import QApplication
import sys

from utils import Logger
from main_window import MainApp


def create_app(logger) -> None:
    """
    Creates app instance.
    """
    app = QApplication(sys.argv)
    main_window = MainApp(logger)
    logger.info("Application starting")
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    logger = Logger("LOGGER").get_logger()

    # TODO at the moment we don't use config file
    # try:
    #     with open("config.toml", "rb") as cfg_file:
    #         cfg = tomllib.load(cfg_file)
    # except FileNotFoundError:
    #     logger.error("Could not find config.toml file!")
    #     sys.exit(1)

    create_app(logger)
