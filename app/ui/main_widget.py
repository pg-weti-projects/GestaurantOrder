import logging
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtGui import QPixmap, QPalette, QBrush, QFont

from .ui_utils import Card

logger = logging.getLogger("app")

class MainWidget(QWidget):
    """
    Class to define main widget to display carousel of the dishes. This widget is one of the main ones and is a part of
    the QStackedWidget.
    """
    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        self.parent = parent

        self.background_image_path = 'resources/img/main_window_background.png'
        self.set_background(self.background_image_path)

        layout = QVBoxLayout(self)

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

        # Here we need to add dish data downloaded from Mongo
        self.dish_data = [
            {"img_path": "resources/img/dish_img/burger.png", "price": "40 zł", "name": "Burger"},
            {"img_path": "resources/img/dish_img/carbonara.png", "price": "26 zł", "name": "Carbonara"},
            {"img_path": "resources/img/dish_img/kebab.png", "price": "33 zł", "name": "Kebab"},
            {"img_path": "resources/img/dish_img/ramen.png", "price": "25 zł", "name": "Ramen"},
            {"img_path": "resources/img/dish_img/sandwich.png", "price": "58 zł", "name": "Sandwich"},
            {"img_path": "resources/img/dish_img/pizza.png", "price": "21 zł", "name": "Pizza"}
        ]

        self.num_visible_items = 5
        self.current_index = 0
        self.main_card = None
        self.cards_number = len(self.dish_data)

        self.update_carousel()
        self.setLayout(layout)

    def resizeEvent(self, event):
        """resizeEvent method override to adjust background image to new app sizze"""
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

    def show_next_items(self) -> None:
        """Moves the cards visible on the screen forward one item with animation."""
        self.current_index = (self.current_index + 1) % len(self.dish_data)
        self.update_carousel()

    def show_previous_items(self) -> None:
        """Moves the cards visible on the screen back one item with animation."""
        self.current_index = (self.current_index - 1) % len(self.dish_data)
        self.update_carousel()

    def update_carousel(self) -> None:
        """
        Removes the Card objects currently visible on the screen and then generates additional cards to be displayed.
        """
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
            dish_card = Card(self.dish_data[current_card_index], is_center)
            self.carousel_layout.addWidget(dish_card)

            if is_center:
                self.main_card = dish_card

    def _add_gestures_images_widgets(self) -> None:
        """
        Adds bottom layout with gestures icons.
        """
        right_corner_layout = QHBoxLayout()
        right_corner_layout.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        image_paths = [
            'resources/img/gesture_img/closed_hand.png',
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
