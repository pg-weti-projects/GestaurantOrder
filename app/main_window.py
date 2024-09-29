import logging
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout, QWidget
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Slot, Qt

from engine import Engine
from ui.widgets import WidgetsManager
from utils import Utils

logger = logging.getLogger("app")


class MainApp(QMainWindow):
    """
    Main window class for the GUI
    """
    def __init__(self, mode):
        super().__init__()
        self.setWindowTitle("GestaurantOrder")
        self.utils = Utils()
        self.engine = Engine(mode)

        # Default visibility settings for widgets
        self.camera_preview_visible = False
        self.helper_widget_preview_visible = False
        self.test_widget_preview_visible = True

        # Define additional help widgets
        self.widgets = WidgetsManager(self.utils.get_monitor_geometry(), self)
        self.helper_widget = self.widgets.create_helper_widget(self.helper_widget_preview_visible)
        self.camera_widget, self.camera_label = self.widgets.create_camera_preview_label(self.camera_preview_visible)

        # Stacked widget for 'main' widgets that shouldn't be displayed at the same time
        self.stacked_widget = QStackedWidget(self)
        self.test_widget = self.widgets.create_test_widget(self.test_widget_preview_visible)
        self.stacked_widget.addWidget(self.test_widget)

        # Set up main layout with main widget
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        main_widget = QWidget(self)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self.engine.frame_ready.connect(self.update_image)
        self.engine.start()
        self.showFullScreen()


    @Slot(QImage)
    def update_image(self, frame):
        pixmap = QPixmap.fromImage(frame)
        self.camera_label.setPixmap(pixmap)
        self.camera_label.setScaledContents(True)

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
        elif event.key() == Qt.Key_2:
            self.toggle_test_widget_preview()

    def toggle_camera_preview(self):
        self.camera_preview_visible = not self.camera_preview_visible
        if self.camera_preview_visible:
            self.camera_widget.raise_()  # sets the camera label at the top of all widgets
        self.camera_widget.setVisible(self.camera_preview_visible)

    def toggle_help_window_preview(self):
        self.helper_widget_preview_visible = not self.helper_widget_preview_visible
        if self.helper_widget_preview_visible:
            self.helper_widget.raise_()  # sets the helper widget at the top of all widgets
        self.helper_widget.setVisible(self.helper_widget_preview_visible)

    def toggle_test_widget_preview(self):
        self.test_widget_preview_visible = not self.test_widget_preview_visible
        self.test_widget.setVisible(self.test_widget_preview_visible)

    def closeEvent(self, event):
        self.engine.stop()
        event.accept()
