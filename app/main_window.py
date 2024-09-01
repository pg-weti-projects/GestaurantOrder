from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Slot, Qt

from engine import Engine
from ui.widgets import Widgets
from utils import Utils


class MainApp(QMainWindow):
    """
    Main window class for the GUI
    """
    def __init__(self, logger):
        super().__init__()
        self.setWindowTitle("Gestaurant Order")
        self.logger = logger
        self.utils = Utils(logger)
        self.engine = Engine(logger)

        self.widgets = Widgets(self.utils.get_monitor_geometry(), self)
        self.helper_widget = self.widgets.create_helper_widget()
        self.camera_preview_label = self.widgets.create_camera_preview_label()

        self.showFullScreen()

        self.engine.frame_ready.connect(self.update_image)
        self.engine.start()

        self.camera_preview_visible = True
        self.helper_widget_preview_visible = False

    @Slot(QImage)
    def update_image(self, frame):
        pixmap = QPixmap.fromImage(frame)
        self.camera_preview_label.setPixmap(pixmap)
        self.camera_preview_label.setScaledContents(True)

    def keyPressEvent(self, event) -> None:
        """
        Handle keyboard operations.

        Args:
            event: Incoming event from QKeyEvent containing information about the key press.
        """
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_H:
            self.toggle_help_window_preview()
        elif event.key() == Qt.Key_1:
            self.toggle_camera_preview()

    def toggle_camera_preview(self):
        self.camera_preview_visible = not self.camera_preview_visible
        self.camera_preview_label.setVisible(self.camera_preview_visible)

    def toggle_help_window_preview(self):
        self.helper_widget_preview_visible = not self.helper_widget_preview_visible
        self.helper_widget.setVisible(self.helper_widget_preview_visible)

    def closeEvent(self, event):
        self.engine.stop()
        event.accept()
