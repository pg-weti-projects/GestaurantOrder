import logging
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QRegion

logger = logging.getLogger("app")

class GestureCounterWidget(QWidget):
    """
    Class defining the gesture counter widget, displaying a countdown timer. Emits a signal when the countdown finishes.
    """
    countdown_finished = Signal()
    def __init__(self, widget_width = 100, widget_height = 100, font_size = 60):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.setVisible(False)

        self.label = QLabel("", self)
        self.label.setStyleSheet(f"font-size: {font_size}px; color: white;")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)

        self.time_left = 2
        self.is_timer_finished = False

        self.setStyleSheet("""
            background-color: gray;
            border-radius: 200px;
        """)

        self.setFixedSize(widget_width, widget_height)
        self.setMask(QRegion(self.rect(), QRegion.Ellipse))

    def start_timer(self) -> None:
        """Starts timer counting in seconds."""
        self.time_left = 2
        self.is_timer_finished = False
        self.label.setText(str(self.time_left))
        self.label.setVisible(True)
        self.setVisible(True)
        self.timer.start(1000)
        logger.debug("Timer started counting.")

    def stop_timer(self) -> None:
        """Forces stop timer without emitting countdown_finished signal"""
        logger.debug("Timer forced stopped counting.")
        self.label.setVisible(False)
        self.timer.stop()
        self.is_timer_finished = True

    def update_countdown(self) -> None:
        """
        Updates the countdown every second. Hides the label and emits the countdown_finished signal when
        the timer reaches zero.
        """
        self.time_left -= 1
        if self.time_left >= 1:
            logger.debug(f"Timer set {self.time_left} seconds left.")
            self.label.setText(str(self.time_left))
        else:
            logger.debug("Timer stopped counting.")
            self.label.setVisible(False)
            self.timer.stop()
            self.is_timer_finished = True
            self.countdown_finished.emit()

    @property
    def is_finished(self) -> bool:
        """
        Checks if the countdown timer has finished.

        Returns: True if the timer has finished, otherwise False.
        """
        return self.is_timer_finished
