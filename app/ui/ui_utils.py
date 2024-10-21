import logging
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtGui import QPixmap, QFont

logger = logging.getLogger("app")


class Card(QWidget):
    """
    Class defining the dish card QWidget.
    """
    def __init__(self, dish_data: dict, is_center: bool):
        super().__init__()
        self.dish_data = dish_data

        card_layout = QVBoxLayout(self)
        card_frame = QFrame(self)

        if is_center:
            card_frame.setStyleSheet("""
                QFrame {
                    background-color: lightblue;
                    border-radius: 15px;
                }
            """)
            self.setFixedSize(270, 410)
        else:
            card_frame.setStyleSheet("""
                QFrame {
                    background-color: lightgray;
                    border-radius: 15px;
                }
            """)
            self.setFixedSize(220, 360)

        # Dish Image widget
        dish_image = QLabel(self)
        pixmap = QPixmap(self.dish_data['img_path'])
        dish_image.setPixmap(pixmap.scaled(230, 230, Qt.KeepAspectRatio, Qt.SmoothTransformation) if is_center
                             else pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        dish_image.setAlignment(Qt.AlignCenter)

        # Dish name widget
        dish_label = QLabel(self.dish_data['name'], self)
        dish_label.setAlignment(Qt.AlignCenter)

        dish_font = QFont()
        dish_font.setPointSize(20)
        dish_font.setBold(True)
        dish_label.setFont(dish_font)
        dish_label.setStyleSheet("color: darkslategray;")

        # Dish price widget
        price_label = QLabel(self.dish_data['price'], self)
        price_label.setAlignment(Qt.AlignCenter)

        price_font = QFont()
        price_font.setPointSize(20)
        price_font.setBold(True)
        price_label.setFont(price_font)
        price_label.setStyleSheet("color: darkslategray;")

        frame_layout = QVBoxLayout(card_frame)
        frame_layout.addWidget(dish_image)
        frame_layout.addWidget(dish_label)
        frame_layout.addWidget(price_label)

        card_layout.addWidget(card_frame)
        self.setLayout(card_layout)
