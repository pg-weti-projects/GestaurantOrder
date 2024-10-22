import logging
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtGui import QPixmap, QPalette, QBrush

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

        top_row = QLabel("Górny wiersz", self)
        top_row.setStyleSheet("background-color: lightgray;")
        top_row.setAlignment(Qt.AlignCenter)
        layout.addWidget(top_row, 1)

        # MIDDLE ROW
        self.middle_row = QWidget(self)
        self.middle_row_layout = QHBoxLayout(self.middle_row)
        layout.addWidget(self.middle_row, 3)

        bottom_row = QLabel("Dolny wiersz", self)
        bottom_row.setStyleSheet("background-color: lightgray;")
        bottom_row.setAlignment(Qt.AlignCenter)
        layout.addWidget(bottom_row, 1)


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
        for i in reversed(range(self.middle_row_layout.count())):
            widget_to_remove = self.middle_row_layout.itemAt(i).widget()
            self.middle_row_layout.removeWidget(widget_to_remove)
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
            self.middle_row_layout.addWidget(dish_card)

            if is_center:
                self.main_card = dish_card

        print(self.main_card.dish_data['name'])
