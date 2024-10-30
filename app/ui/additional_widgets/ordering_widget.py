import logging
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMainWindow, QHBoxLayout
from PySide6.QtGui import QPixmap, QFont

from .card_widget import CardWidget
from .gesture_counter_widget import GestureCounterWidget
from .confirmation_widget import ConfirmationWidget


logger = logging.getLogger("app")

class OrderingWidget(QWidget):
    """
    Class for ordering widget that displays ordered dish and gives user possibility to choice number of
    the dish to order.
    """
    gesture_detected = Signal(str)
    ordered_dish = Signal(dict)
    success_order = Signal(str)
    failure_order = Signal(str)

    def __init__(self, parent: QWidget | QMainWindow, monitor_geometry: dict, selected_dish_data: dict):
        super().__init__(parent)
        self.parent = parent
        self.selected_dish_data: dict = selected_dish_data
        self.monitor_geometry: dict = monitor_geometry
        self._set_window_geometry(monitor_geometry['width'], monitor_geometry['height'])
        image_size, widget_size = self._scaled_sizes(monitor_geometry['width'], monitor_geometry['height'])
        self.setVisible(True)

        main_widget = QWidget()
        main_widget.setStyleSheet("background-color: #a0a0a0; border-radius: 45px;")
        layout = QVBoxLayout(main_widget)

        self.gesture_counter = GestureCounterWidget()
        self.gesture_counter.countdown_finished.connect(self.handle_gesture_on_timer_finished)
        self.gesture_counter_works: bool = False

        # Top Layout
        self.top_layout = QVBoxLayout()
        self.top_layout_widget = QWidget()
        self.top_layout_widget.setStyleSheet(f"background-color: rgba(255, 255, 255, 0); border-radius: 45px;")
        self.top_layout_widget.setLayout(self.top_layout)
        self._add_top_layout_widget()
        layout.addWidget(self.top_layout_widget, 1)

        # Mid layout
        self.card_layout = QHBoxLayout()
        self.card_widget = QWidget()
        self.card_widget.setLayout(self.card_layout)
        self._add_card_widget(self.selected_dish_data, is_center=False)
        layout.addWidget(self.card_widget, 4)

        # Counter dish layout
        self.counter_layout = QHBoxLayout()
        self.counter_widget = QWidget()
        self.counter_widget.setLayout(self.counter_layout)
        self.counter_label = QLabel("0", self)
        self.counter_label.setAlignment(Qt.AlignCenter)
        self.counter_label.setStyleSheet(f"font-size: 48px; color: black;")
        self.counter_layout.addWidget(self.counter_label)
        layout.addWidget(self.counter_widget, 2)

        # Bottom layout
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout_widget = QWidget()
        self.bottom_layout_widget.setLayout(self.bottom_layout)
        self._add_bottom_images_and_counter(image_size, widget_size)
        layout.addWidget(self.bottom_layout_widget, 1)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(main_widget)

        self.number_to_order: int = 0
        self.confirm_widget: ConfirmationWidget | None = None

        self.last_gesture: str | None = None

        self.setLayout(main_layout)

    @Slot(str)
    def handle_gesture(self, gesture: str) -> None:
        """
        Sets last gesture, emits detected gesture detection further and handles gesture operation.

        Args:
            gesture: Detected gesture name.
        """
        self.last_gesture = gesture
        self.gesture_detected.emit(gesture)
        self.handle_gesture_operation(gesture)
        logger.debug(f"OrderingWidget gesture {gesture} set.")

    def handle_gesture_operation(self, gesture: str) -> None:
        """
        Handles operations based on detected gestures.

        Args:
            gesture: The detected gesture, which can be the number of fingers (0-10).

        The method performs the following actions:
        - If the gesture counter is not currently active and a valid gesture is detected, it sets the counter_label
        text on the specific value, starts the gesture counter and connects the countdown finished
        signal to 'handle_gesture_on_timer_finished'.
        - If the gesture counter is already active and the gesture is not valid, it stops the timer and resets the
        gesture counter status.
        """
        if not self.confirm_widget:
            if not self.gesture_counter_works:
            # TODO ATTACH FINGERS MODEL HERE
                if gesture in ("Open_Palm"): # ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10") TODO
                    self.gesture_counter_works = True
                    if gesture == "0":
                        self.counter_label.setText("CANCELING")
                    else:
                        self.counter_label.setText("6") # TODO change to 'gesture'
                    self.gesture_counter.start_timer()
                else:
                    self.counter_label.setText("UNKNOWN GESTURE")
            else:
                self.gesture_counter.stop_timer()
                self.gesture_counter_works = False

    def handle_gesture_on_timer_finished(self) -> None:
        """
        Executes actions based on the last recognized gesture when the timer finishes counting.

        The method logs the event and performs the following actions:
        - If the last gesture was the number from 1-10, it calls the `_create_and_show_confirmation_widget` method
        responsible for creating and displaying confirmation widget.
        - If the last gesture was "0", it emits the signal to the MainWidget with canceling the ordering process
        of selected dish.
        """
        logger.debug(f"OrderingWidget timer stopped counting. Making action assigned to {self.last_gesture}.")
        if self.last_gesture == ("Open_Palm"):  # TODO CHANGE Open_Palm to tuple ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
            self.number_to_order = int("6") # TODO change to int(self.last_gesture)
            self._create_and_show_confirmation_widget()
        elif self.last_gesture == "0":
            self.failure_order.emit(f"You have canceled ordering {self.selected_dish_data['name']}.")
            self.ordered_dish.emit({})

    def _create_and_show_confirmation_widget(self) -> None:
        """Creates and shows confirmation widget of ordered dish."""
        if not self.confirm_widget:
            self.confirm_widget = ConfirmationWidget(
                self.parent,
                self.number_to_order,
                self.selected_dish_data['name'],
                self.selected_dish_data['price'],
                self.monitor_geometry
            )
            self.gesture_detected.connect(self.confirm_widget.handle_gesture)
            self.confirm_widget.gesture_response.connect(self.handle_confirmation_ordering)
            self.confirm_widget.show()

    @Slot(str)
    def handle_confirmation_ordering(self, user_operation: str) -> None:
        """
        Handles the confirmation of an order. If the user_operation is confirmed then success_order and ordered_dish
        signals are emitted for display appropriate confirm notification and add the dish to the SummaryOrderWidget,
        but if the user_operation is canceled, only failure_order signal is emitted for display appropriate cancel
        notification. After the emitting signals, the confirm_widget will be removed. It also sets counter_label to '0'
        for resetting the dish number counter.

        Args:
            user_operation: Emitted operation selected by user ( confirmed or canceled ).
        """
        if user_operation == "confirmed":
            self.success_order.emit(f"You have successfully ordered {self.selected_dish_data['name']}.")
            self.ordered_dish.emit({"amount": self.number_to_order, "dish_data": self.selected_dish_data})
        elif user_operation == "canceled":
            self.failure_order.emit(f"You have canceled ordering {self.selected_dish_data['name']}.")
        else:
            logger.error("Incorrect user operation from ConfirmationWidget!")

        self.counter_label.setText("0")

        if self.confirm_widget:
            self.confirm_widget.setParent(None)
            self.gesture_detected.disconnect(self.confirm_widget.handle_gesture)
            self.confirm_widget.gesture_response.disconnect(self.handle_confirmation_ordering)
            self.confirm_widget.deleteLater()
            self.confirm_widget = None

    def _add_card_widget(self, selected_dish_data: dict, is_center: bool = False) -> None:
        """Adds CardWidget with selected dish data to OrderingWidget."""
        card = CardWidget(selected_dish_data, is_center, self.monitor_geometry)
        self.card_layout.addWidget(card)

    def _add_top_layout_widget(self) -> None:
        """Adds a header label widget to the top layout of the interface."""
        header_label = QLabel("How many pieces of the product do you want to order?", self)
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setWordWrap(True)
        header_font = QFont()
        header_font.setPointSize(16)
        header_font.setBold(True)
        header_label.setFont(header_font)
        header_label.setStyleSheet("color: black;")
        self.top_layout.addWidget(header_label)

    def _add_bottom_images_and_counter(self, image_size: int, widget_size: int) -> None:
        """Adds bottom layout with gestures icons and counter widget."""
        right_corner_layout = QHBoxLayout()
        right_corner_layout.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        right_corner_layout.addWidget(self.gesture_counter)

        image_paths = [
            "resources/img/gesture_img/fingers.png"
        ]
        labels = ["SHOW AMOUNT"]
        for image_path, label_text in zip(image_paths, labels):
            widget = QWidget()
            layout = QVBoxLayout(widget)

            image_label = QLabel()
            pixmap = QPixmap(image_path)
            image_label.setPixmap(pixmap.scaled(image_size, image_size, Qt.AspectRatioMode.KeepAspectRatio))

            text_label = QLabel(label_text)
            text_label.setStyleSheet("font-weight: bold; color: black;")

            layout.addWidget(image_label, alignment=Qt.AlignCenter)
            layout.addWidget(text_label, alignment=Qt.AlignCenter)

            widget.setFixedSize(widget_size, widget_size)
            right_corner_layout.addWidget(widget)

        self.bottom_layout.addLayout(right_corner_layout)

    def _set_window_geometry(self, m_width: int, m_height: int) -> None:
        """
        Sets self object geometry.
        """
        if m_width == 1512 and m_height == 982:  # MacBook 4K
            height_ratio = 0.7
            y_offset_ratio = 0.4
        elif m_width == 1920 and m_height == 1080:  # Full HD
            height_ratio = 0.5
            y_offset_ratio = 0.25
        elif m_width == 2560 and m_height == 1440:  # 2K
            height_ratio = 0.5
            y_offset_ratio = 0.25
        elif m_width == 3840 and m_height == 2160:  # 4K
            height_ratio = 0.7
            y_offset_ratio = 0.3
        else:
            height_ratio = 0.7
            y_offset_ratio = 0.3

        m_center_width = m_width // 2
        m_center_height = m_height // 2
        window_x_pos = m_width * 0.3
        self.setGeometry(m_center_width - window_x_pos // 2,
                         m_center_height - (m_height * y_offset_ratio),
                         window_x_pos,
                         m_height * height_ratio)

    @staticmethod
    def _scaled_sizes(screen_width: int, screen_height: int) -> tuple:
        """
        Calculate the value of the scaled size.

        Args:
            screen_width: Width of the screen.
            screen_height: Height of the screen.

        Returns:
            Tuple image_size, widget_size.
        """
        if screen_width == 1512 and screen_height == 982:  # MacBook 4K
            return 40, 130
        elif screen_width == 1920 and screen_height == 1080:  # Full HD
            return 50, 110
        elif screen_width == 2560 and screen_height == 1440:  # 2K
            return 50, 110
        elif screen_width == 3840 and screen_height == 2160:  # 4K
            return 50, 110
        else:
            return 50, 110
