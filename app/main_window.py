import logging
from PySide6.QtCore import Slot, Qt, Signal, QTimer
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout, QWidget
from PySide6.QtGui import QPixmap, QImage

from engine import Engine
from ui.widgets_manager import WidgetsManager
from utils import Utils

logger = logging.getLogger("app")


class MainApp(QMainWindow):
    """
    Class for the main app window which contains all other widgets.
    """
    gesture_detected = Signal(str)

    def __init__(self, mode):
        super().__init__()
        self.setWindowTitle("GestaurantOrder")
        self.utils = Utils()
        self.engine = Engine(mode)
        self.widgets = WidgetsManager(self.utils.get_monitor_geometry(), self)

        # Define main views ( widgets managed by QStackedWidget ) - only one of them can be displayed at a time
        self.default_visible_main_widget_name = "main_widget"
        self.main_widgets = {
            "main_widget": self.widgets.create_main_widget(default_visibility=False),
            "admin_panel": self.widgets.create_admin_panel_widget(default_visibility=False)
        }
        self.stacked_widget = QStackedWidget(self)
        for widget in self.main_widgets.values():
            self.stacked_widget.addWidget(widget)

        self.stacked_widget.setCurrentWidget(self.main_widgets[self.default_visible_main_widget_name])

        # Defined default visibility of the additional widgets for switching their visibility during app execution.
        self.camera_visible: bool = False
        self.helper_widget_visible: bool = False

        # Define additional widgets
        self.helper_widget = self.widgets.create_helper_widget(default_visibility=False)
        self.camera_widget, self.camera_label = self.widgets.create_camera_preview_label(default_visibility=False)

        self.notification_widget = None
        self.main_widgets["main_widget"].success_notification.connect(self.show_success_notification)
        self.main_widgets["main_widget"].failure_notification.connect(self.show_failure_notification)

        # Set up main layout and widget for other widgets
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        layout.setContentsMargins(0,0,0,0)
        main_widget = QWidget(self)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self.last_gesture: str | None = None

        self.engine.frame_ready.connect(self.update_image)
        self.engine.gesture_detected.connect(self.handle_gesture)
        self.gesture_detected.connect(self.main_widgets['main_widget'].handle_gesture)

        # Detects if data have been updated in admin panel and updates carousel in main widget
        self.main_widgets["admin_panel"].db_data_changed.connect(
            self.main_widgets["main_widget"].update_carousel_data)

        self.engine.start()
        self.showFullScreen()

    @Slot(QImage)
    def update_image(self, frame) -> None:
        """Updates image in camera_label widget."""
        pixmap = QPixmap.fromImage(frame)
        self.camera_label.setPixmap(pixmap)
        self.camera_label.setScaledContents(True)

    @Slot(str)
    def handle_gesture(self, gesture: str) -> None:
        """
        Sets last gesture and emits detected gesture detection further.

        Args:
            gesture: Detected gesture name.
        """
        self.last_gesture = gesture
        self.gesture_detected.emit(gesture)
        logger.debug(f"MainApp gesture {gesture} set.")

    @Slot(str)
    def show_success_notification(self, notification_text: str) -> None:
        """Shows notification widget and remove it after few seconds."""
        if not self.notification_widget:
            self.notification_widget = self.widgets.create_notification_widget(notification_text, "success")
            QTimer.singleShot(5000, self.remove_notification_widget)

    @Slot(str)
    def show_failure_notification(self, notification_text: str) -> None:
        """Shows notification widget and remove it after few seconds."""
        if not self.notification_widget:
            self.notification_widget = self.widgets.create_notification_widget(notification_text, "failure")
            QTimer.singleShot(5000, self.remove_notification_widget)

    def remove_notification_widget(self) -> None:
        """Removes notification widget from view and main window."""
        self.notification_widget.setParent(None)
        self.notification_widget.deleteLater()
        self.notification_widget = None

    def keyPressEvent(self, event) -> None:
        """
        Handle keyboard operations.

        Args:
            event: Incoming event from QKeyEvent containing information about the key press.
        """
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_F1:
            self.toggle_main_widgets(self.main_widgets['main_widget'])
        elif event.key() == Qt.Key_F2:
            self.toggle_main_widgets(self.main_widgets['admin_panel'])
        elif event.key() == Qt.Key_F3:
            self.toggle_camera_preview()
        elif event.key() == Qt.Key_F4:
            self.toggle_help_window_preview()
        else:
            logger.debug(f"Unrecognized keyboard key! {event.key()}")

    def toggle_main_widgets(self, actual_widget: QWidget) -> None:
        """Toggle widgets defined in QStackedWidget."""
        if self.stacked_widget.currentWidget() != actual_widget:
            self.stacked_widget.setCurrentWidget(actual_widget)

    def toggle_camera_preview(self) -> None:
        """Toggle camera preview widget."""
        self.camera_visible = not self.camera_visible
        if self.camera_visible:
            self.camera_widget.raise_()  # sets the camera label at the top of all widgets
        self.camera_widget.setVisible(self.camera_visible)

    def toggle_help_window_preview(self) -> None:
        """Toggle help widget preview."""
        self.helper_widget_visible = not self.helper_widget_visible
        if self.helper_widget_visible:
            self.helper_widget.raise_()  # sets the helper widget at the top of all widgets
        self.helper_widget.setVisible(self.helper_widget_visible)

    def closeEvent(self, event):
        """Overwrites closeEvent method"""
        self.engine.stop()
        event.accept()
