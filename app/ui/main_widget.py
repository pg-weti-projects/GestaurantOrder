import logging
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QPixmap, QPalette, QBrush

from .ui_utils import Card
from Mongo.mongo_manager import MongoManager

logger = logging.getLogger("app")

class MainWidget(QWidget):
    """
    Class to define main widget to display carousel of the dishes. This widget is one of the main ones and is a part of
    the QStackedWidget.
    """
    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        self.dish_data = []
        self.parent = parent

        self.background_image_path = 'resources/img/main_window_background.png'
        self.set_background(self.background_image_path)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.num_visible_items = 5
        self.current_index = 0

        self.load_dishes_from_db()

        self.carousel_layout = QHBoxLayout()

        for index, dish in enumerate(self.dish_data):
            if index < self.num_visible_items:
                dish_card = Card(dish, index == self.num_visible_items // 2)
                self.carousel_layout.addWidget(dish_card)

        self.carousel_widget = QWidget()
        self.carousel_widget.setLayout(self.carousel_layout)

        layout.addWidget(self.carousel_widget)

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
        return self.dish_data

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

        for i in range(self.num_visible_items):
            current_card_index = (self.current_index + i) % len(self.dish_data)
            is_center = (i == self.num_visible_items // 2)
            dish_card = Card(self.dish_data[current_card_index], is_center)
            self.carousel_layout.addWidget(dish_card)
