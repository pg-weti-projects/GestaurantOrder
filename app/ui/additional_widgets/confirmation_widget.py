import logging
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtGui import QPixmap

from .gesture_counter_widget import GestureCounterWidget

logger = logging.getLogger("app")

WIDGET_COLOR = "#a0a0a0"

class ConfirmationWidget(QWidget):
    """
    Class for confirmation QWidget.
    """
    gesture_detected = Signal(str)

    def __init__(self, parent, number_to_order: int, dish_name: str, dish_price: int, monitor_geometry: dict):
        super().__init__(parent)
        self.set_window_geometry(monitor_geometry['width'], monitor_geometry['height'])
        self.setVisible(True)
        self.raise_()

        main_layout = QVBoxLayout(self)
        main_widget = QWidget()
        main_widget.setStyleSheet(f"background-color: {WIDGET_COLOR}; border-radius: 45px;")

        layout = QVBoxLayout(main_widget)

        message_layout = QVBoxLayout()
        full_price = dish_price * number_to_order
        message_label = QLabel(f"Do you want to order {number_to_order} {dish_name} for {full_price} zł?", self)
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setStyleSheet("font-weight: bold; color: black; font-size: 32px")
        message_layout.addWidget(message_label)
        layout.addLayout(message_layout, 2)

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout_widget = QWidget()
        self.bottom_layout_widget.setLayout(self.bottom_layout)
        self.gesture_counter = GestureCounterWidget()
        self._add_bottom_images_and_counter()
        layout.addWidget(self.bottom_layout_widget, 1)

        main_layout.addWidget(main_widget)
        self.setLayout(main_layout)

        self.last_gesture = None
        # self.gesture_counter.start_timer() # TODO REMOVE AFTER TESTING

    def _add_bottom_images_and_counter(self) -> None:
        """
        Adds bottom layout with gestures icons.
        """
        right_corner_layout = QHBoxLayout()
        right_corner_layout.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        right_corner_layout.addWidget(self.gesture_counter)

        image_paths = [
            'resources/img/gesture_img/thumb_down.png',
            'resources/img/gesture_img/thumb_up.png'
        ]
        labels = ["CANCEL", "ACCEPT"]
        for image_path, label_text in zip(image_paths, labels):
            widget = QWidget()
            layout = QVBoxLayout(widget)

            image_label = QLabel()
            pixmap = QPixmap(image_path)
            image_label.setPixmap(pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio))

            text_label = QLabel(label_text)
            text_label.setStyleSheet("font-weight: bold; color: black;")

            layout.addWidget(image_label, alignment=Qt.AlignCenter)
            layout.addWidget(text_label, alignment=Qt.AlignCenter)

            widget.setFixedSize(110, 110)
            right_corner_layout.addWidget(widget)

        self.bottom_layout.addLayout(right_corner_layout)

    def set_window_geometry(self, m_width: int, m_height: int) -> None:
        """
        Sets self object geometry.
        """
        m_center_width = m_width // 2
        m_center_height = m_height // 2
        window_x_pos = m_width * 0.3
        self.setGeometry(m_center_width - window_x_pos / 2,
                         m_center_height - (m_height * 0.25),
                         window_x_pos,
                         m_height * 0.5)
