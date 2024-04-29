from PySide6.QtCore import QObject
import time


class Engine(QObject):
    def __init__(self, logger):
        super().__init__()
        self.logger = logger

    def run_process(self):
        while True:
            self.logger.info("Processing frame etc.")
            time.sleep(3)
            # TODO: Here we define gathering and processing for each frame ( actually every operations that must be
            #  used on other thread. We also define all processes related to each frame and each 'program round'.
            #  We can use PyQt Signals to connect most elements. You can define here frame gathering.
