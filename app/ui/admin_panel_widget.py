import logging
from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QMessageBox


logger = logging.getLogger("app")


class AdminPanel(QWidget):
    """
    Class responsible for admin GUI operations. This widget is one of the main ones and is a part of the QStackedWidget.
    """
    def __init__(self, parent: QMainWindow):
        super().__init__(parent)

        button = QPushButton("ADMIN PANEL")
        button.clicked.connect(self.temp_function)

        layout = QVBoxLayout()
        layout.addWidget(button)

        self.setLayout(layout)

    def temp_function(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Info")
        msg_box.setText("Clicked panel admin button!")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()