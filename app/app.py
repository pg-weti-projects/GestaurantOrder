from PySide6.QtWidgets import QApplication
import sys
from utils import Logger
from main_window import MainApp


def create_app(logger, mode) -> None:
    """
    Creates app instance.
    """
    app = QApplication(sys.argv)
    main_window = MainApp(logger, mode)
    logger.info("Application starting")
    main_window.show()
    sys.exit(app.exec())

def get_user_mode():
    print("Chose mode:")
    print("1 - fingers")
    print("2 - mediapipe")
    choice = input("Enter your choice 1 or 2: ")
    if choice == "1":
        return "fingers"
    elif choice == "2":
        return "mediapipe"
    else:
        print("Invalid choice!")
        print("Default choice 1 - fingers")
        return "fingers"

if __name__ == "__main__":
    logger = Logger("LOGGER").get_logger()
    mode = get_user_mode()
    # TODO at the moment we don't use config file
    # try:
    #     with open("config.toml", "rb") as cfg_file:
    #         cfg = tomllib.load(cfg_file)
    # except FileNotFoundError:
    #     logger.error("Could not find config.toml file!")
    #     sys.exit(1)

    create_app(logger, mode)
