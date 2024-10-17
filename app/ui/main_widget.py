import logging
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel


logger = logging.getLogger("app")


class MainWidget(QWidget):
    """
    Class to define main widget to display carousel of the dishes. This widget is one of the main ones and is a part of
    the QStackedWidget.
    """
    def __init__(self, parent: QMainWindow):
        super().__init__(parent)

        self.welcome_label = QLabel("WELCOME", self)
        self.welcome_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.welcome_label)

        self.setLayout(layout)