import logging


class Logger:
    """
    Class for configuring and obtaining a logger.
    """
    def __init__(self, name: str):
        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s (%(lineno)d): %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.__logger.addHandler(console_handler)

    def get_logger(self) -> logging.Logger:
        """
        Returns the logger instance.

        Returns:
            The logger instance.
        """
        return self.__logger
