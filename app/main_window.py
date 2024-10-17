import logging
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout, QWidget, QLabel
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Slot, Qt

from engine import Engine
from ui.widgets_manager import WidgetsManager
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
        self.widgets = WidgetsManager(self.utils.get_monitor_geometry(), self)

        # Define main views ( widgets managed by QStackedWidget ) - only one of them can be displayed at a time
        self.default_visible_main_widget_name = "main_view_widget"
        self.main_widgets = {
            "main_view_widget": self.widgets.create_main_widget(default_visibility=False),
            "test_widget": self.widgets.create_test_widget(default_visibility=False),
            "admin_panel": self.widgets.create_admin_panel_widget(default_visibility=False)
        }
        self.stacked_widget = QStackedWidget(self)
        for widget in self.main_widgets.values():
            self.stacked_widget.addWidget(widget)

        self.stacked_widget.setCurrentWidget(self.main_widgets[self.default_visible_main_widget_name])

        # Default visibility settings for additional widgets ( which do not belong to stacked widgets )
        self.camera_default_visible = False
        self.helper_widget_default_visible = False

        # Define additional widgets
        self.helper_widget = self.widgets.create_helper_widget(default_visibility=False)
        self.camera_widget, self.camera_label = self.widgets.create_camera_preview_label(default_visibility=False)

        # Set up main layout and widget for other widgets
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
        elif event.key() == Qt.Key_1:
            self.toggle_main_widgets(self.main_widgets['main_view_widget'])
        elif event.key() == Qt.Key_2:
            self.toggle_main_widgets(self.main_widgets['test_widget'])
        elif event.key() == Qt.Key_3:
            self.toggle_main_widgets(self.main_widgets['admin_panel'])
        elif event.key() == Qt.Key_H:
            self.toggle_help_window_preview()
        elif event.key() == Qt.Key_9:
            self.toggle_camera_preview()

    def toggle_main_widgets(self, actual_widget: QWidget) -> None:
        if self.stacked_widget.currentWidget() != actual_widget:
            self.stacked_widget.setCurrentWidget(actual_widget)

    def toggle_camera_preview(self):
        self.camera_default_visible = not self.camera_default_visible
        if self.camera_default_visible:
            self.camera_widget.raise_()  # sets the camera label at the top of all widgets
        self.camera_widget.setVisible(self.camera_default_visible)

    def toggle_help_window_preview(self):
        self.helper_widget_default_visible = not self.helper_widget_default_visible
        if self.helper_widget_default_visible:
            self.helper_widget.raise_()  # sets the helper widget at the top of all widgets
        self.helper_widget.setVisible(self.helper_widget_default_visible)

    def closeEvent(self, event):
        self.engine.stop()
        event.accept()
