from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QMainWindow, QLabel, QWidget, QSizePolicy, QVBoxLayout, QHBoxLayout, QPushButton,
                               QMessageBox)

from .admin_panel_widget import AdminPanel
from .main_widget import MainWidget


class WidgetsManager:
    """
    Class to define additional widgets that are not supported by QStackedWidget ( except temporary test widget ).
    """
    def __init__(self, monitor_geometry: dict, main_window: QMainWindow):
        self._main_window = main_window
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
        \t1 - Show/Hide main window\n
        \t2 - Show/Hide test widget\n
        \t3 - Show/Hide admin panel\n
        \t9 - Show/Hide camera preview\n
        \tH - Show help window\n
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


    def create_test_widget(self, default_visibility: bool) -> QWidget:
        """
        Creates widget for testing algorithms and app with 3 clickable squares at the horizontal center of app.

        Args:
            default_visibility: Sets the default setting of the widget visibility.

        Returns: Test widget object
        """
        test_widget = QWidget(self._main_window)
        layout = QVBoxLayout(test_widget)
        row_layout = QHBoxLayout()

        button_labels = {"CARBONARA": "resources/img/dish_img/carbonara.png",
                         "PIZZA": "resources/img/dish_img/pizza.png",
                         "RAMEN": "resources/img/dish_img/ramen.png"}

        for btn_label, img_path in button_labels.items():
            button = QPushButton("", test_widget)
            button.setFixedSize(300, 300)
            button.setStyleSheet(f"""
                QPushButton {{
                    background-image: url('{img_path}');
                    background-position: center;
                    background-repeat: no-repeat;
                    background-size: contain;
                    border: 1px black;
                }}
                QPushButton:hover {{
                    border: 5px solid lightblue;
                }}
                QPushButton:focus {{
                    border: 6px solid blue;
                    outline: none;
            }}
            """)

            button.clicked.connect(lambda _, label=btn_label: self._show_button_message(label))
            row_layout.addWidget(button)

        layout.addLayout(row_layout)
        test_widget.setLayout(layout)
        test_widget.setVisible(default_visibility)

        return test_widget

    def _show_button_message(self, btn_label: str) -> None:
        """Shows a message box when a button is clicked."""
        QMessageBox.information(self._main_window, "Button Clicked", f"CLICKED {btn_label}!")

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
        main_widget = MainWidget(self._main_window)
        main_widget.setVisible(default_visibility)
        return main_widget
