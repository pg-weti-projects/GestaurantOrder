from PySide6.QtWidgets import QLabel, QWidget, QSizePolicy
from PySide6.QtCore import Qt


class Widgets:
    def __init__(self, monitor_geometry: dict, main_window):
        self._main_window = main_window
        self._m_width = monitor_geometry['width']
        self._m_height = monitor_geometry['height']
        self._m_center_width = monitor_geometry['width'] / 2
        self._m_center_height = monitor_geometry['height'] / 2

    def create_helper_widget(self) -> QWidget:
        """
        Creates the helper widget which displays the available options in app.

        Returns: Widget object
        """
        helper_widget = QWidget(self._main_window)
        helper_widget.setWindowTitle("Help")
        helper_widget.setGeometry(self._m_center_width - (self._m_width / 4),
                                  self._m_center_height - (self._m_height / 4),
                                  self._m_center_width,
                                  self._m_center_height)
        helper_widget.setVisible(False)

        helper_widget.setStyleSheet("background-color: grey;")

        label_text = """Available functions:\n
        \t1 - Show/Hide camera preview\n
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

    def create_camera_preview_label(self) -> QLabel:
        """
        Creates label for displaying image captured by camera.

        Returns: Label object
        """
        label = QLabel("Camera Preview", self._main_window)
        label.setGeometry(self._m_center_width - (self._m_width / 4),
                          0,
                          self._m_center_width,
                          self._m_center_height)
        label.setVisible(True)
        label.setStyleSheet("border: 2px solid cyan;")

        return label
