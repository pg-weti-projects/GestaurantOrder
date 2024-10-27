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
    Class for ordering widget that displays ordered dish.
    """
    gesture_detected = Signal(str)

    def __init__(self, parent: QWidget | QMainWindow, monitor_geometry: dict, selected_dish_data: dict):
        super().__init__(parent)
        self.parent = parent
        self.selected_dish_data = selected_dish_data
        self.monitor_geometry = monitor_geometry
        self._set_window_geometry(monitor_geometry['width'], monitor_geometry['height'])
        self.setVisible(True)

        main_widget = QWidget()
        main_widget.setStyleSheet("background-color: #a0a0a0; border-radius: 45px;")
        layout = QVBoxLayout(main_widget)
        # main_widget.setContentsMargins(20,0,20,0)

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
        self._add_card_to_layout(self.selected_dish_data, is_center=False)
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
        self.gesture_counter = GestureCounterWidget()
        self.gesture_counter.countdown_finished.connect(self.show_confirmation_widget)
        self._add_bottom_images_and_counter()
        layout.addWidget(self.bottom_layout_widget, 1)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(main_widget)
        self.setLayout(main_layout)

        self.number_to_order = 0
        self.confirm_widget_obj = None
        self.ordered_dish = []

        self.last_gesture = None
        # self.gesture_counter.start_timer() # TODO REMOVE AFTER TESTING

    @Slot(str)
    def handle_gesture(self, gesture: str) -> None:
        """
        Handle gesture operation. Sets last gesture and emits detected gesture detection further
        Args:
            gesture: Detected gesture name.
        """
        self.last_gesture = gesture
        self.gesture_detected.emit(gesture)
        logger.debug(f"OrderingWidget gesture {gesture} handled.")


    def set_dish_number(self, value: int) -> None: # TODO ATTACH TO FINGERS GESTURE RECOGNIZING
        """
        Sets dish number to order in QLabel.

        Args:
            value: Dish number to set.
        """
        self.counter_label.setText(str(value))
        self.number_to_order = value

    def _set_window_geometry(self, m_width: int, m_height: int) -> None:
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

    def _add_card_to_layout(self, selected_dish_data: dict, is_center: bool = False) -> None:
        card = CardWidget(selected_dish_data, is_center, self.monitor_geometry)
        self.card_layout.addWidget(card)

    def _add_top_layout_widget(self) -> None:
        """
        Adds a header label widget to the top layout of the interface. This label prompts the user to specify the
        quantity of the product they wish to order.
        """
        header_label = QLabel("How many pieces of the product do you want to order?", self)
        header_label.setAlignment(Qt.AlignCenter)
        header_font = QFont()
        header_font.setPointSize(16)
        header_font.setBold(True)
        header_label.setFont(header_font)
        header_label.setStyleSheet("color: black;")
        self.top_layout.addWidget(header_label)

    def _add_bottom_images_and_counter(self) -> None:
        """
        Adds bottom layout with gestures icons and counter widget.
        """
        right_corner_layout = QHBoxLayout()
        right_corner_layout.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        right_corner_layout.addWidget(self.gesture_counter)

        image_paths = [
            'resources/img/gesture_img/fingers.png'
        ]
        labels = ["SHOW AMOUNT"]
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

    def show_confirmation_widget(self) -> None:
        """
        Creates and shows confirmation widget of ordered dish.
        """
        self.confirm_widget_obj = ConfirmationWidget(
            self.parent,
            self.number_to_order,
            self.selected_dish_data['name'],
            self.selected_dish_data['price'],
            self.monitor_geometry
        )
        # self.confirm_widget_obj.confirmed.connect(self.handle_confirmation_ordering) # TODO ATTACH IT WHILE THE USER CONFIRMED SELECTING PRODUCT
        self.confirm_widget_obj.show()

    def handle_confirmation_ordering(self) -> None:
        """
        Handles the confirmation of an order. This method performs the following actions:

        1. If a confirmation widget object exists, it deletes the widget and sets the reference to None.
        2. Logs an informational message confirming the order, including the quantity and name of the selected dish.
        3. Appends the ordered dish details, including the amount and dish data, to the ordered_dish list.
        """
        if self.confirm_widget_obj:
            self.confirm_widget_obj.deleteLater()
            self.confirm_widget_obj = None
        logger.info(f"Confirmed order for {self.number_to_order} of {self.selected_dish_data['name']}.")
        self.ordered_dish.append({"amount": self.number_to_order, "dish_data": self.selected_dish_data })
