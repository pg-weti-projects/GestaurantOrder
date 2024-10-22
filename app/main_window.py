import logging
import os
from PySide6.QtCore import Slot, Qt, QTimer
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout, QWidget
from PySide6.QtGui import QPixmap, QImage

from camera.gesture_parser import GestureParser
from engine import Engine
from ui.widgets_manager import WidgetsManager
from utils import Utils
from pynput.keyboard import Key, Controller

keyboard = Controller()

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
        # Track last processed gesture
        self.last_gesture = None

        # Default visibility settings for additional widgets
        self.camera_preview_visible = False
        self.helper_widget_preview_visible = False
        self.test_widget_preview_visible = True

        # Define additional help widgets
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
        layout.setContentsMargins(0,0,0,0)
        main_widget = QWidget(self)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self.engine.frame_ready.connect(self.update_image)
        self.engine.start()
        self.showFullScreen()

        self.filename = os.getenv('CAMERA_FILENAME')
        self.gesture_timer = QTimer(self)
        self.gesture_timer.timeout.connect(self.check_gestures_from_json)
        self.gesture_timer.start(1000)


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
        elif event.key() == Qt.Key_D:
            if self.stacked_widget.currentWidget() == self.main_widgets['main_view_widget']:
                self.main_widgets['main_view_widget'].show_next_items()
        elif event.key() == Qt.Key_A:
            if self.stacked_widget.currentWidget() == self.main_widgets['main_view_widget']:
                self.main_widgets['main_view_widget'].show_previous_items()

    def toggle_main_widgets(self, actual_widget: QWidget) -> None:
        if self.stacked_widget.currentWidget() != actual_widget:
            self.stacked_widget.setCurrentWidget(actual_widget)

    def check_gestures_from_json(self):
        gesture = GestureParser().read_gesture_from_json(self.filename)

        if gesture is not None and gesture != self.last_gesture:
            self.last_gesture = gesture
            self.handle_gesture_action(gesture)

    def handle_gesture_action(self, gesture):
        if gesture == 1:
            self.simulate_key_press(Qt.Key_Right)
        elif gesture == 2:
            self.simulate_key_press(Qt.Key_Left)
        elif gesture == 'Open_Palm':
            self.simulate_key_press(Qt.Key_Right)
        elif gesture == 'Thumb_Down':
            self.simulate_key_press(Qt.Key_Left)

        ## TO DO
        # elif gesture == 'Thumb_Up':
        #     self.simulate_key_press(Qt.Key_Right)
        # elif gesture == 'Pointing_Up':
        #     self.simulate_key_press(Qt.Key_Right)

    @staticmethod
    def simulate_key_press(key):
        if key == Qt.Key_Right:
            keyboard.press(Key.right)
            keyboard.release(Key.right)
        elif key == Qt.Key_Left:
            keyboard.press(Key.left)
            keyboard.release(Key.left)

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
