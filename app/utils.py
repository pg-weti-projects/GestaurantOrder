import logging
from PySide6.QtGui import QGuiApplication
import subprocess
import sys

from Mongo.mongo_manager import MongoManager

class Utils:
    """
    Class for all other functions that cannot be classified.
    """
    def __init__(self):
        self._logger = logging.getLogger("app")

    def get_monitor_geometry(self) -> dict:
        """
        Gets primary monitor geometry ( width and height )

        Returns:
            Monitor width and height
        """
        monitor = QGuiApplication.primaryScreen().geometry()
        m_width = monitor.width()
        m_height = monitor.height()
        self._logger.info(f"Size of your primary monitor: {m_width}x{m_height}")

        return {"width": m_width, "height": m_height}

class LoggerManager:
    """
    Class for configuring global logger.
    """
    def __init__(self, name: str, debug_mode_enabled: bool):
        self._logger = logging.getLogger(name)

        logging_level = logging.DEBUG if debug_mode_enabled else logging.INFO
        self._logger.setLevel(logging_level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)

        if debug_mode_enabled:
            log_dir = "logs/logs.log"
            self._logger.info(f"Debug mode is enabled. Logs will be saved to file: {log_dir}")
            file_handler = logging.FileHandler(log_dir)
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)

class DockerManager:
    """
    Class for managing docker containers from Python level execution.
    """

    def __init__(self):
        self._logger = logging.getLogger("app")

    def run_docker_services(self, docker_file_path: str) -> None:
        """
        Runs docker compose file with MongoDB and mongo-express docker containers.
        Args:
            docker_file_path: Docker compose file path.
        """
        try:
            subprocess.Popen(["docker-compose", "-f", docker_file_path, "up"])
            self._logger.debug("Containers mongodb and mongoui started successfully")
        except subprocess.CalledProcessError as e:
            self._logger.exception(f"Failed to start containers! Error: {e}")
            sys.exit(1)

    def stop_docker_services(self, docker_file_path: str) -> None:
        """
        Stops docker compose file with MongoDB and mongo-express docker containers.
        Args:
            docker_file_path: Docker compose file path.
        """
        try:
            subprocess.run(["docker-compose", "-f", docker_file_path, "down"])
            self._logger.debug("Stopped and removed mongodb and mongoui containers.")
        except subprocess.CalledProcessError as e:
            self._logger.exception(f"Failed to stop containers! Error: {e}")

    def wait_for_mongo_container_start(self) -> None:
        """
        Waits for the MongoDB container to be fully up and running.
        """
        mongo_manager = MongoManager()
        attempt = 0
        max_attempts = 18
        while attempt != max_attempts:  # Wait 180 seconds for MongoDB container run
            mongo_connection = mongo_manager.check_mongo_connection()
            if mongo_connection:
                self._logger.debug(f"MongoDB container is READY!")
                return
            else:
                self._logger.debug(f"Waiting for MongoDB container. Attempt {attempt}/{max_attempts}")
                attempt += 1
        else:
            self._logger.error("MongoDB container not working! Check the container and run app again.")
            sys.exit(1)
