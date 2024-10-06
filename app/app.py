from dotenv import load_dotenv
import logging
import os
from PySide6.QtWidgets import QApplication
import sys

from main_window import MainApp
from utils import DockerManager, LoggerManager

load_dotenv()
APP_DEBUG_MODE_ENABLED = os.getenv('APP_DEBUG_MODE') == "true"

LoggerManager("app", APP_DEBUG_MODE_ENABLED)
logger = logging.getLogger("app")


def create_and_run_app() -> None:
    """
    Creates app instance.
    """
    app = QApplication(sys.argv)
    main_window = MainApp(get_user_detection_mode())
    logger.info("App starting")
    main_window.show()
    app.exec()
    logger.info("App stopped.")


def get_user_detection_mode() -> str:
    env_detection_mode = os.getenv('APP_DETECTION_MODE', 'fingers')
    if env_detection_mode not in ['fingers', 'mediapipe']:
        print("Invalid mode in environment!")
        return "fingers"
    return env_detection_mode


if __name__ == "__main__":
    if APP_DEBUG_MODE_ENABLED:
        logger.info("APP DEBUG MODE IS ENABLED!")
    docker_compose_path = "docker-compose.yml"
    containers_start_parallel = os.getenv('CONTAINERS_START_PARALLEL') == "true"
    dm = DockerManager()

    try:
        if containers_start_parallel:
            dm.run_docker_services(docker_compose_path)
            dm.wait_for_mongo_container_start()

        create_and_run_app()
    except Exception as e:
        logger.error(f"An unexpected error occurred! Error: {e}")
    finally:
        if containers_start_parallel:
            dm.stop_docker_services(docker_compose_path)
