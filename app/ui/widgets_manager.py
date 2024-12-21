from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QLabel, QWidget, QSizePolicy, QVBoxLayout

from .admin_panel_widget import AdminPanel
from .main_widget import MainWidget


class WidgetsManager:
    """
    Class to define additional widgets that are not supported by QStackedWidget ( except temporary test widget ).
    """
    def __init__(self, monitor_geometry: dict, main_window: QMainWindow):
        self._main_window = main_window
        self.monitor_geometry = monitor_geometry
        self._m_width = monitor_geometry['width']
        self._m_height = monitor_geometry['height']
        self._m_center_width = monitor_geometry['width'] / 2
        self._m_center_height = monitor_geometry['height'] / 2

    def create_helper_widget(self, default_visibility: bool) -> QWidget:
        """
        Creates the helper widget which displays the available options in app.

        Args:
            default_visibility: Sets the default setting of the widget visibility.

        Returns: Helper window widget object
        """
        helper_widget = QWidget(self._main_window)
        helper_widget.setWindowTitle("Help")
        helper_widget.setGeometry(self._m_center_width - (self._m_width / 4),
                                  self._m_center_height - (self._m_height / 4),
                                  self._m_center_width,
                                  self._m_center_height)
        helper_widget.setVisible(default_visibility)

        helper_widget.setStyleSheet("background-color: grey;")

        label_text = """Available functions:\n
        \tF1 - Show/Hide main window\n
        \tF2 - Show/Hide admin panel\n
        \tF3 - Show help window\n
        \tF4 - Show/Hide camera preview\n
        \tESC - Exit application
        """

        label_info = QLabel(label_text, helper_widget)
        label_info.setStyleSheet("color: white; font-size: 20px; padding: 5px;")
        label_info.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label_info.setSizePolicy(size_policy)

        label_info.setGeometry(helper_widget.rect())

        return helper_widget

    def create_camera_preview_label(self, default_visibility: bool) -> (QWidget, QLabel):
        """
        Creates widget for displaying label with images captured by camera.

        Args:
            default_visibility: Sets the default setting of the widget visibility.

        Returns: Camera widget object and label object.
        """
        camera_widget = QWidget(self._main_window)
        camera_widget.setGeometry(self._m_center_width - (self._m_width / 4),
                          0,
                          self._m_center_width,
                          self._m_center_height)
        camera_widget.setVisible(default_visibility)

        layout = QVBoxLayout(camera_widget)
        camera_label = QLabel("Camera Preview", camera_widget)
        camera_label.setStyleSheet("border: 2px solid black;")
        layout.addWidget(camera_label)
        camera_widget.setLayout(layout)

        return camera_widget, camera_label

    def create_notification_widget(self, text: str, notification_type: str) -> QWidget:
        """
        Creates notification widget with specified text. Sets notification background based on the specified
        notification_status param. If the param is 'success' the background will be green but if is 'failure' the
        background will be red.

        Args:
            text: Text to be set in notification widget.
            notification_type: Notification type to set proper background color of notification.

        Returns: QWidget with QLabel.
        """
        notification_widget = QWidget(self._main_window)
        notification_widget.setGeometry(
            self._main_window.width() // 3,
            50,
            self._main_window.width() // 3,
            100
        )

        if notification_type == "success":
            bg_color = "#228B22"
        elif notification_type == "failure":
            bg_color = "#800020"
        else:
            bg_color = "#D3D3D3"

        notification_widget.setStyleSheet(f"background-color: {bg_color}; border-radius: 10px;")
        notification_widget.setContentsMargins(5, 5, 5, 5)

        label = QLabel(text, notification_widget)
        label.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(notification_widget)
        layout.addWidget(label)
        notification_widget.setLayout(layout)

        notification_widget.raise_()
        notification_widget.show()

        return notification_widget

    def create_admin_panel_widget(self, default_visibility: bool) -> QWidget:
        """
        Creates widget for testing algorithms and app with 3 clickable squares at the horizontal center of app.

        Args:
            default_visibility: Sets the default setting of the widget visibility.

        Returns: Admin panel widget object
        """
        admin_panel_widget = AdminPanel(self._main_window)
        admin_panel_widget.setVisible(default_visibility)
        return admin_panel_widget

    def create_main_widget(self, default_visibility: bool) -> QWidget:
        """
        Creates widget for with main view.

        Args:
            default_visibility: Sets the default setting of the widget visibility.

        Returns: Main view widget object
        """
        main_widget = MainWidget(self._main_window, self.monitor_geometry)
        main_widget.setVisible(default_visibility)
        return main_widget
