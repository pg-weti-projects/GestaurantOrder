import logging
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtGui import QPixmap, QPalette, QBrush, QFont

from .additional_widgets.card_widget import CardWidget
from .additional_widgets.ordering_widget import OrderingWidget
from .additional_widgets.gesture_counter_widget import GestureCounterWidget
from .summary_order_widget import SummaryOrderWidget
from Mongo.mongo_manager import MongoManager

logger = logging.getLogger("app")

class MainWidget(QWidget):
    """
    Class to define main widget to display carousel of the dishes. This widget is one of the main ones and is a part of
    the QStackedWidget.
    """
    gesture_detected = Signal(str)
    success_notification = Signal(str)
    failure_notification = Signal(str)

    def __init__(self, parent: QMainWindow, monitor_geometry: dict):
        super().__init__(parent)
        self.parent = parent
        self.monitor_geometry = monitor_geometry

        self.background_image_path = 'resources/img/main_window_background.png'
        self._set_background(self.background_image_path)

        layout = QVBoxLayout(self)

        self.gesture_counter = GestureCounterWidget()
        self.gesture_counter.countdown_finished.connect(self.handle_gesture_on_timer_finished)
        self.gesture_counter_works: bool = False

        self.dish_data: list = []
        self.dish_data_exists: bool = self._load_dishes_from_db()

        # Top layout
        self.top_layout = QHBoxLayout()
        self.top_layout_widget = QWidget()
        self.top_layout_widget.setLayout(self.top_layout)
        self._add_logo_and_title()
        layout.addWidget(self.top_layout_widget, 1)

        # Carousel layout
        self.carousel_layout = QHBoxLayout(self)
        self.carousel_widget = QWidget()
        self.carousel_widget.setLayout(self.carousel_layout)
        layout.addWidget(self.carousel_widget, 3)

        # Bottom layout
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout_widget = QWidget()
        self.bottom_layout_widget.setLayout(self.bottom_layout)
        self._add_gestures_images_widgets()
        layout.addWidget(self.bottom_layout_widget, 1)

        self.num_visible_items: int = 5
        self.current_index: int = 0
        self.selected_card: CardWidget | None = None
        self.cards_number: int = len(self.dish_data)

        self.ordering_widget = None
        self.summary_order_widget = None
        self.ordered_dish_data: list = []

        self.last_gesture: str | None = None

        if self.dish_data_exists:
            self.update_carousel()

        self.setLayout(layout)

    def _load_dishes_from_db(self) -> bool:
        """
        Loads dish data from the MongoDB.

        Returns: True if the dish data exists or False if not
        """
        mongo_manager = MongoManager()
        dishes = mongo_manager.get_order_list()

        self.dish_data = [{
                "img_path": dish['image_path'],
                "price": dish['price'],
                "name": dish['name']
            }
            for dish in dishes
        ]
        if self.dish_data:
            return True
        else:
            return False

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
        logger.debug(f"MainWidget gesture {gesture} set.")

    def handle_gesture_operation(self, gesture: str) -> None:
        """
        Handles operations based on detected gestures.

        Args:
            gesture: The detected gesture, which can be "Thumb_Up", "Thumb_Down, "Open_Palm", or "Closed_Fist".

        The method performs the following actions:
        - If the ordering_widget and summary_order_widget do not exist, the gesture counter is not currently active
        and a valid gesture is detected, it starts the gesture counter and connects the countdown finished
        signal to 'handle_gesture_on_timer_finished'.
        - If the gesture counter is already active and the gesture is not valid, it stops the timer and resets the
        gesture counter status.
        """
        if not self.ordering_widget and not self.summary_order_widget:
            if not self.gesture_counter_works:
                if gesture in ("Thumb_Up", "Thumb_Down", "Open_Palm", "Closed_Fist"):
                    self.gesture_counter_works = True
                    self.gesture_counter.start_timer()
            else:
                self.gesture_counter.stop_timer()
                self.gesture_counter_works = False

    def handle_gesture_on_timer_finished(self) -> None:
        """
        Executes actions based on the last recognized gesture when the timer finishes counting.

        The method logs the event and performs the following actions:
        - If the last gesture was "Thumb_Up", it calls the `_select_dish` method responsible for displaying ordering
        widget.
        - If the last gesture was "Thumb_Down", it calls the `_create_and_show_summary_order_widget` method responsible
        for creating and displaying summary order widget
        - If the last gesture was "Open_Palm", it calls the `_show_next_items` method responsible for moving carousel
        to the next item.
        - If the last gesture was "Closed_Fist", it calls the `_show_previous_items` method responsible for moving
        carousel to the previous item.
        """
        logger.debug(f"MainWidget timer stopped counting. Making action assigned to {self.last_gesture}.")
        if self.last_gesture == "Thumb_Up":
            self._select_dish()
        elif self.last_gesture == "Thumb_Down":
            self._create_and_show_summary_order_widget()
        elif self.last_gesture == "Open_Palm":
            self._show_next_items()
        elif self.last_gesture == "Closed_Fist":
            self._show_previous_items()

    def _select_dish(self) -> None:
        """Creates Ordering Widget when the dish is selected and ordering_widget not exist."""
        if self.selected_card and not self.ordering_widget:
            self.ordering_widget = OrderingWidget(self.parent, self.monitor_geometry, self.selected_card.dish_data)
            self.gesture_detected.connect(self.ordering_widget.handle_gesture)
            self.ordering_widget.ordered_dish.connect(self.add_ordered_dish_and_close_ordering_widget)
            self.ordering_widget.success_order.connect(self.emit_show_success_notification)
            self.ordering_widget.failure_order.connect(self.emit_show_failure_notification)
            self.ordering_widget.raise_()

    @Slot(str)
    def emit_show_success_notification(self, notification_text: str) -> None:
        """Emits success notification signal to the MainApp class for displaying notification with specified text"""
        self.success_notification.emit(notification_text)

    @Slot(str)
    def emit_show_failure_notification(self, notification_text: str) -> None:
        """Emits failure notification signal to the MainApp class for displaying notification with specified text"""
        self.failure_notification.emit(notification_text)

    @Slot(dict)
    def add_ordered_dish_and_close_ordering_widget(self, ordered_dish: dict) -> None:
        """
        If the user confirmed ordering selected dish, the ordered dish data will be added to ordered_dish_data list.
        At the end OrderingWidget is removed.

        Args:
            ordered_dish: Ordered dish data contains information about amount of the ordered dish and
            other dish data like name, price for one dish, and img_path.
        """
        if ordered_dish:
            self.ordered_dish_data.append(ordered_dish)
            logger.debug(f"Confirmed order for {ordered_dish['amount']} of {ordered_dish['dish_data']['name']}.")
        else:
            logger.debug("Ordering dish has been canceled!")

        if self.ordering_widget:
            self.ordering_widget.setParent(None)
            self.gesture_detected.disconnect(self.ordering_widget.handle_gesture)
            self.ordering_widget.ordered_dish.disconnect(self.add_ordered_dish_and_close_ordering_widget)
            self.ordering_widget.success_order.disconnect(self.emit_show_success_notification)
            self.ordering_widget.failure_order.disconnect(self.emit_show_failure_notification)
            self.ordering_widget.deleteLater()
            self.ordering_widget = None

    def _create_and_show_summary_order_widget(self) -> None:
        """
        Creates and shows SummaryOrderWidget with ordered dish if ordered dish have been added by user.
        If not only notification will be displayed.
        """
        if self.ordered_dish_data:
            self.summary_order_widget = SummaryOrderWidget(self.parent, self.monitor_geometry, self.ordered_dish_data)
            self.summary_order_widget.setVisible(True)
            self.gesture_detected.connect(self.summary_order_widget.handle_gesture)
            self.summary_order_widget.gesture_response.connect(self.handle_summary_order_widget_operation_and_close_widget)
        else:
            logger.debug("There are no any data to display in SummaryOrderWidget! Skipping creating this widget.")
            self.failure_notification.emit(f"There are no any ordered dish! Please order something first.")

    @Slot(str)
    def handle_summary_order_widget_operation_and_close_widget(self, user_operation: str) -> None:
        """
        Handle operation from emitted from SummaryOrderWidget when the user confirmed or canceled order. If the order
        is confirmed it displays the confirmation notification and cancel notification if the order is canceled.

        Args:
            user_operation: Selected operation by user ( confirmed or canceled order ).
        """
        order_number = 6
        if user_operation == "confirmed":
            self.success_notification.emit(f"Your order has been confirmed! Your order number is {order_number}.")
        elif user_operation == "canceled":
            self.failure_notification.emit(f"Your order has been canceled!")
        else:
            logger.error("Incorrect user operation from SummaryOrderWidget!")

        if self.summary_order_widget:
            self.summary_order_widget.setParent(None)
            self.gesture_detected.disconnect(self.summary_order_widget.handle_gesture)
            self.summary_order_widget.gesture_response.disconnect(self.handle_summary_order_widget_operation_and_close_widget)
            self.summary_order_widget.deleteLater()
            self.summary_order_widget = None
            self.ordered_dish_data = []

    def update_carousel(self) -> None:
        """
        Removes the Card objects currently visible on the screen and then generates next cards to be displayed if the
        OrderingWidget and SummaryOrderWidget not exist ( if the widget exist the carousel must be blocked ).
        """
        if not self.ordering_widget and not self.summary_order_widget:
            for i in reversed(range(self.carousel_layout.count())):
                widget_to_remove = self.carousel_layout.itemAt(i).widget()
                self.carousel_layout.removeWidget(widget_to_remove)
                widget_to_remove.setParent(None)

            if self.cards_number == 1:
                num_visible = 1
                center_index = 0
            elif self.cards_number <= 3:
                num_visible = 3
                center_index = 1
            else:
                num_visible = 5
                center_index = 2

            for i in range(num_visible):
                current_card_index = (self.current_index + i - center_index) % self.cards_number
                is_center = (i == center_index)
                dish_card = CardWidget(self.dish_data[current_card_index], is_center, self.monitor_geometry)
                self.carousel_layout.addWidget(dish_card)

                if is_center:
                    self.selected_card = CardWidget(self.dish_data[current_card_index], is_center, self.monitor_geometry)

    def _show_next_items(self) -> None:
        """Moves the cards visible on the screen forward one item."""
        if self.dish_data_exists:
            self.current_index = (self.current_index + 1) % len(self.dish_data)
            self.update_carousel()

    def _show_previous_items(self) -> None:
        """Moves the cards visible on the screen back one item."""
        if self.dish_data_exists:
            self.current_index = (self.current_index - 1) % len(self.dish_data)
            self.update_carousel()

    def _add_gestures_images_widgets(self) -> None:
        """Adds bottom layout with gestures icons."""
        right_corner_layout = QHBoxLayout()
        right_corner_layout.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        right_corner_layout.addWidget(self.gesture_counter)

        image_paths = [
            "resources/img/gesture_img/closed_fist.png",
            "resources/img/gesture_img/open_hand.png",
            "resources/img/gesture_img/thumb_up.png",
            "resources/img/gesture_img/thumb_down.png"
        ]
        labels = ["MOVE LEFT", "MOVE RIGHT", "CHOOSE DISH", "SUMMARY"]
        for image_path, label_text in zip(image_paths, labels):
            widget = QWidget()
            layout = QVBoxLayout(widget)

            image_label = QLabel()
            pixmap = QPixmap(image_path)
            image_label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))

            text_label = QLabel(label_text)
            text_label.setStyleSheet("font-weight: bold; color: white;")

            layout.addWidget(image_label, alignment=Qt.AlignCenter)
            layout.addWidget(text_label, alignment=Qt.AlignCenter)

            widget.setFixedSize(120, 150)
            right_corner_layout.addWidget(widget)

        self.bottom_layout.addLayout(right_corner_layout)

    def _add_logo_and_title(self) -> None:
        """Adds top layout with app logo and name."""
        left_corner_layout = QHBoxLayout()
        left_corner_layout.setAlignment(Qt.AlignLeft | Qt.AlignCenter)

        widget = QWidget()
        layout = QHBoxLayout(widget)

        logo_label = QLabel()
        logo_pixmap = QPixmap('resources/img/gesture_img/thumb_down.png')
        logo_label.setPixmap(logo_pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))

        title_label = QLabel("GestaurantOrder")
        title_label.setStyleSheet("font-weight: bold; color: white;")
        title_label.setFont(QFont("Comic Sans MS", 60))
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        layout.addWidget(logo_label, alignment=Qt.AlignLeft)
        layout.addWidget(title_label, alignment=Qt.AlignLeft)

        layout.setSpacing(40)

        left_corner_layout.addWidget(widget)
        self.top_layout.addLayout(left_corner_layout)

    def resizeEvent(self, event):
        """Overwrite resizeEvent method to adjust background image to new app size"""
        self._set_background(self.background_image_path)
        super().resizeEvent(event)

    def _set_background(self, image_path) -> None:
        """
        Sets an image as the widget's background, adapting it to the window size.

        Args:
            image_path: Path to the image to be set as the background.
        """
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
