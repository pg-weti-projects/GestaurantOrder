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

    def __init__(self, parent: QMainWindow, monitor_geometry: dict):
        super().__init__(parent)
        self.parent = parent
        self.monitor_geometry = monitor_geometry

        self.background_image_path = 'resources/img/main_window_background.png'
        self.set_background(self.background_image_path)

        layout = QVBoxLayout(self)
        self.dish_data = []
        self.load_dishes_from_db()

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
        self.gesture_counter = GestureCounterWidget()
        self.gesture_counter_works = False
        # self.gesture_counter.countdown_finished.connect(self.show_confirmation_widget) # TODO ATTACH TO GESTURE RECOGNITION
        self._add_gestures_images_widgets()
        layout.addWidget(self.bottom_layout_widget, 1)

        self.num_visible_items = 5
        self.current_index = 0
        self.selected_card = None
        self.cards_number = len(self.dish_data)

        self.ordering_widget = None
        self.summary_widget = None
        self.ordered_dish_data = None
        self.last_gesture = None

        self.update_carousel()
        self.setLayout(layout)

    def load_dishes_from_db(self):
        """Loads dish data from the MongoDB."""
        mongo_manager = MongoManager()
        dishes = mongo_manager.get_order_list()

        self.dish_data = [{
                "img_path": dish['image_path'],
                "price": f"{dish['price']} zł",
                "name": dish['name']
            }
            for dish in dishes
        ]

    def resizeEvent(self, event):
        """resizeEvent method override to adjust background image to new app sizze"""
        self.set_background(self.background_image_path)
        super().resizeEvent(event)
    @Slot(str)
    def handle_gesture(self, gesture: str) -> None:
        """
        Handle gesture operation. Sets last gesture and emits detected gesture detection further
        Args:
            gesture: Detected gesture name.
        """
        self.last_gesture = gesture
        self.gesture_detected.emit(gesture)
        self.handle_gesture_operation(gesture)
        logger.debug(f"MainWidget gesture {gesture} set.")

    def on_timer_finished(self) -> None:
        """
        Executes actions based on the last recognized gesture when the timer finishes counting.

        The method logs the event and performs the following actions:
        - If the last gesture was "Thumb_Up", it calls the `select_dish` method responsible for displaying ordering
        widget.
        - If the last gesture was "Open_Palm", it calls the `show_next_items` method responsible for moving carousel
        to the next item.
        - If the last gesture was "Closed_Fist", it calls the `show_previous_items` method responsible for moving
        carousel to the previous item.
        """
        logger.debug(f"MainWidget timer stopped counting. Making action assigned to {self.last_gesture}.")
        if self.last_gesture == "Thumb_Up":
            self.select_dish()
        elif self.last_gesture == "Open_Palm":
            self.show_next_items()
        elif self.last_gesture == "Closed_Fist":
            self.show_previous_items()

    def handle_gesture_operation(self, gesture: str) -> None:
        """
        Handles operations based on detected gestures.

        Args:
            gesture (str): The detected gesture, which can be "Thumb_Up", "Open_Palm", or "Closed_Fist".

        The method performs the following actions:
        - If the gesture counter is not currently active and a valid gesture is detected, it starts the gesture counter
        and connects the countdown finished signal to `on_timer_finished`.
        - If the gesture counter is already active, it stops the timer, disconnects the signal, and resets the gesture
        counter status.
        """
        if not self.gesture_counter_works:
            if gesture in ("Thumb_Up", "Open_Palm", "Closed_Fist"):
                self.gesture_counter_works = True
                self.gesture_counter.start_timer()
                self.gesture_counter.countdown_finished.connect(self.on_timer_finished)
        else:
            self.gesture_counter.stop_timer()
            self.gesture_counter.countdown_finished.disconnect(self.on_timer_finished)
            self.gesture_counter_works = False

    def select_dish(self) -> None:
        """
        Creates Ordering Widget when the dish is selected.
        """
        if self.selected_card and not self.ordering_widget:
            print("SELECTED AND OPENED ORDERING WINDOW: ", self.selected_card.dish_name) # TODO REMOVE AFTER TESTING
            self.ordering_widget = OrderingWidget(self.parent, self.monitor_geometry, self.selected_card.dish_data)
            self.gesture_detected.connect(self.ordering_widget.handle_gesture)
            self.ordering_widget.raise_()

    def set_dish_number_in_ordering_widget(self, number: int) -> None:
        """
        Sets the number of dishes in the ordering widget.

        Args:
            number (int): The quantity of dishes to be set in the ordering widget.

        If the ordering widget exists, it updates the dish number by calling the 'set_dish_number' method on the widget.
        """
        if self.ordering_widget:
            self.ordering_widget.set_dish_number(number)

    def close_ordering_widget(self) -> None:
        """
        Closes and cleans up the ordering widget.

        If the ordering widget exists, this method disconnects the gesture detection signal from the widget's handling
        method, deletes the widget, and sets its reference to None, ensuring proper resource management.
        """
        if self.ordering_widget:
            self.gesture_detected.disconnect(self.ordering_widget.handle_gesture)
            self.ordering_widget.deleteLater()
            self.ordering_widget = None

    def show_next_items(self) -> None:
        """Moves the cards visible on the screen forward one item."""
        self.current_index = (self.current_index + 1) % len(self.dish_data)
        self.update_carousel()

    def show_previous_items(self) -> None:
        """Moves the cards visible on the screen back one item."""
        self.current_index = (self.current_index - 1) % len(self.dish_data)
        self.update_carousel()

    def update_carousel(self) -> None:
        """
        Removes the Card objects currently visible on the screen and then generates next cards to be displayed.
        """
        if not self.ordering_widget:
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

    def _add_gestures_images_widgets(self) -> None:
        """
        Adds bottom layout with gestures icons.
        """
        right_corner_layout = QHBoxLayout()
        right_corner_layout.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        right_corner_layout.addWidget(self.gesture_counter)

        image_paths = [
            'resources/img/gesture_img/closed_fist.png',
            'resources/img/gesture_img/open_hand.png',
            'resources/img/gesture_img/thumb_up.png'
        ]
        labels = ["MOVE LEFT", "MOVE RIGHT", "CHOOSE DISH"]
        for image_path, label_text in zip(image_paths, labels):
            widget = QWidget()
            layout = QVBoxLayout(widget)

            image_label = QLabel()
            pixmap = QPixmap(image_path)
            image_label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))

            text_label = QLabel(label_text)
            text_label.setStyleSheet("font-weight: bold;")

            layout.addWidget(image_label, alignment=Qt.AlignCenter)
            layout.addWidget(text_label, alignment=Qt.AlignCenter)

            widget.setFixedSize(120, 150)
            right_corner_layout.addWidget(widget)

        self.bottom_layout.addLayout(right_corner_layout)

    def _add_logo_and_title(self) -> None:
        """
        Adds top layout with app logo and name.
        """
        left_corner_layout = QHBoxLayout()
        left_corner_layout.setAlignment(Qt.AlignLeft | Qt.AlignCenter)

        widget = QWidget()
        layout = QHBoxLayout(widget)

        logo_label = QLabel()
        logo_pixmap = QPixmap('resources/img/gesture_img/thumb_down.png')
        logo_label.setPixmap(logo_pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))

        title_label = QLabel("GestaurantOrder")
        title_label.setStyleSheet("font-weight: bold;")
        title_label.setFont(QFont("Comic Sans MS", 60))
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        layout.addWidget(logo_label, alignment=Qt.AlignLeft)
        layout.addWidget(title_label, alignment=Qt.AlignLeft)

        layout.setSpacing(40)

        left_corner_layout.addWidget(widget)
        self.top_layout.addLayout(left_corner_layout)

    def resizeEvent(self, event):
        """resizeEvent method override to adjust background image to new app size"""
        self.set_background(self.background_image_path)
        super().resizeEvent(event)

    def set_background(self, image_path) -> None:
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

    def create_summary_widget(self): # TODO TEMP FOR TESTING
        """
        TEMP FUNCTION FOR SummaryOrderWidget TESTS.
        """
        self.dish_data = [
            {"img_path": "resources/img/dish_img/burger.png", "price": 40, "name": "Burger"},
            {"img_path": "resources/img/dish_img/carbonara.png", "price": 26, "name": "Carbonara"},
            {"img_path": "resources/img/dish_img/kebab.png", "price": 33, "name": "Kebab"},
            {"img_path": "resources/img/dish_img/ramen.png", "price": 25, "name": "Ramen"},
            {"img_path": "resources/img/dish_img/sandwich.png", "price": 58, "name": "Sandwich"},
            {"img_path": "resources/img/dish_img/pizza.png", "price": 21, "name": "Pizza"}
        ]

        temp = [
            {"amount": 2, "dish_data": self.dish_data[0]},
            {"amount": 2, "dish_data": self.dish_data[0]},
            {"amount": 3, "dish_data": self.dish_data[2]},
            {"amount": 2, "dish_data": self.dish_data[3]},
            {"amount": 6, "dish_data": self.dish_data[3]}
        ]
        self.summary_widget = SummaryOrderWidget(self.parent, self.monitor_geometry, temp)
        self.summary_widget.setVisible(True)
