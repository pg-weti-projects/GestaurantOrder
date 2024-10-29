import logging
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtGui import QPixmap

from .gesture_counter_widget import GestureCounterWidget

logger = logging.getLogger("app")

class ConfirmationWidget(QWidget):
    """
    Class for confirmation QWidget that displays confirmation window with information about name and
    amount of ordering dish.
    """
    gesture_response = Signal(str)

    def __init__(self, parent, number_to_order: int, dish_name: str, dish_price: int, monitor_geometry: dict):
        super().__init__(parent)
        self._set_window_geometry(monitor_geometry['width'], monitor_geometry['height'])
        self.setVisible(True)
        self.raise_()

        main_layout = QVBoxLayout(self)
        main_widget = QWidget()
        main_widget.setStyleSheet(f"background-color: #a0a0a0; border-radius: 45px;")

        self.gesture_counter = GestureCounterWidget()
        self.gesture_counter.countdown_finished.connect(self.handle_gesture_on_timer_finished)
        self.gesture_counter_works: bool = False

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
        self._add_bottom_images_and_counter()
        layout.addWidget(self.bottom_layout_widget, 1)

        main_layout.addWidget(main_widget)

        self.last_gesture: str | None = None

        self.setLayout(main_layout)

    @Slot(str)
    def handle_gesture(self, gesture: str) -> None:
        """
        Sets last gesture and emits detected gesture detection further.

        Args:
            gesture: Detected gesture name.
        """
        self.last_gesture = gesture
        self.handle_gesture_operation(gesture)
        logger.debug(f"ConfirmationWidget gesture {gesture} set.")

    def handle_gesture_operation(self, gesture: str) -> None:
        """
        Handles operations based on detected gestures.

        Args:
            gesture: The detected gesture, which can be "Thumb_Up" or "Thumb_Down".

        The method performs the following actions:
        - If the gesture counter is not currently active and a valid gesture is detected, it starts the gesture counter
        and connects the countdown finished signal to 'handle_gesture_on_timer_finished'.
        - If the gesture counter is already active and the gesture is not valid, it stops the timer and resets the
        gesture counter status.
        """
        if not self.gesture_counter_works:
            if gesture in ("Thumb_Up", "Thumb_Down"):
                self.gesture_counter_works = True
                self.gesture_counter.start_timer()
        else:
            self.gesture_counter.stop_timer()
            self.gesture_counter_works = False

    def handle_gesture_on_timer_finished(self) -> None:
        """
        Executes actions based on the last recognized gesture when the timer finishes counting.

        The method logs the event and performs the following actions:
        - If the last gesture was "Thumb_Up", it calls the `_confirm_dish_order` method responsible for emitting signal
        about confirmed dish order.
        - If the last gesture was "Thumb_Down", it calls the `_cancel_dish_order` method responsible for emitting signal
        about canceled dish order.
        """
        logger.debug(f"ConfirmationWidget timer stopped counting. Making action assigned to {self.last_gesture}.")
        if self.last_gesture == "Thumb_Up":
            self._confirm_dish_order()
        elif self.last_gesture == "Thumb_Down":
            self._cancel_dish_order()

    def _confirm_dish_order(self) -> None:
        """Emits the confirmation signal to the MainWidget class."""
        logger.debug("ConfirmationWidget: Dish has been confirmed.")
        self.gesture_response.emit("confirmed")

    def _cancel_dish_order(self) -> None:
        """Emits the cancel signal to the MainWidget class."""
        logger.debug("ConfirmationWidget: Dish has been canceled.")
        self.gesture_response.emit("canceled")

    def _add_bottom_images_and_counter(self) -> None:
        """Adds bottom layout with gestures icons."""
        right_corner_layout = QHBoxLayout()
        right_corner_layout.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        right_corner_layout.addWidget(self.gesture_counter)

        image_paths = [
            "resources/img/gesture_img/thumb_down.png",
            "resources/img/gesture_img/thumb_up.png"
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

    def _set_window_geometry(self, m_width: int, m_height: int) -> None:
        """Sets ConfirmationWidget geometry."""
        m_center_width = m_width // 2
        m_center_height = m_height // 2
        window_x_pos = m_width * 0.3
        self.setGeometry(m_center_width - window_x_pos / 2,
                         m_center_height - (m_height * 0.25),
                         window_x_pos,
                         m_height * 0.5)
