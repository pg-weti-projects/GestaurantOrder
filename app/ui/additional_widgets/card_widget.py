import logging
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtGui import QPixmap, QFont

logger = logging.getLogger("app")

class CardWidget(QWidget):
    """
    Class defining the dish card QWidget.
    """
    def __init__(self, dish_data: dict, is_center: bool, screen_geometry: dict):
        super().__init__()
        self.dish_data = dish_data
        self.dish_img = dish_data['img_path']
        self.dish_price = dish_data['price']
        self.dish_name = dish_data['name']

        card_layout = QVBoxLayout(self)
        card_frame = QFrame(self)

        if is_center:
            card_frame.setStyleSheet("""
                QFrame {
                    background-color: lightblue;
                    border-radius: 15px;
                }
            """)
        else:
            card_frame.setStyleSheet("""
                QFrame {
                    background-color: lightgray;
                    border-radius: 15px;
                }
            """)

        width, height = self._calculate_size(screen_geometry['width'], screen_geometry['height'], is_center)
        self.setFixedSize(width, height)

        # Dish Image widget
        dish_image = QLabel(self)
        pixmap = QPixmap(self.dish_img)
        dish_image.setPixmap(pixmap.scaled(230, 230, Qt.KeepAspectRatio, Qt.SmoothTransformation) if is_center
                             else pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        dish_image.setAlignment(Qt.AlignCenter)

        # Dish name widget
        dish_label = QLabel(self.dish_name, self)
        dish_label.setAlignment(Qt.AlignCenter)

        dish_font = QFont()
        dish_font.setPointSize(20)
        dish_font.setBold(True)
        dish_label.setFont(dish_font)
        dish_label.setStyleSheet("color: darkslategray;")

        # Dish price widget
        price_label = QLabel(f"{self.dish_price} zł", self)
        price_label.setAlignment(Qt.AlignCenter)

        price_font = QFont()
        price_font.setPointSize(self._set_font_size(screen_geometry['width'], screen_geometry['height']))
        price_font.setBold(True)
        price_label.setFont(price_font)
        price_label.setStyleSheet("color: darkslategray;")

        frame_layout = QVBoxLayout(card_frame)
        frame_layout.addWidget(dish_image)
        frame_layout.addWidget(dish_label)
        frame_layout.addWidget(price_label)

        card_layout.addWidget(card_frame)
        self.setLayout(card_layout)

    @staticmethod
    def _calculate_size(screen_width: int, screen_height: int, is_center: bool) -> tuple:
        """
        Calculate the size of the card based on screen resolution.

        Args:
            screen_width: Width of the screen.
            screen_height: Height of the screen.
            is_center: Boolean indicating if the card is centered.

        Returns: A tuple (width, height).
        """
        if screen_width == 1920 and screen_height == 1080:  # Full HD
            return (220, 360) if is_center else (170, 310)
        elif screen_width == 2560 and screen_height == 1440:  # 2K
            return (270, 410) if is_center else (220, 360)
        elif screen_width == 3840 and screen_height == 2160:  # 4K
            return (320, 460) if is_center else (270, 420)
        else:
            return (220, 360) if is_center else (170, 310)

    @staticmethod
    def _set_font_size(screen_width: int, screen_height: int) -> int:
        """
        Calculate the size of the font for the Card.

        Args:
            screen_width: Width of the screen.
            screen_height: Height of the screen.

        Returns: Size of the font
        """
        if screen_width == 1920 and screen_height == 1080:  # Full HD
            return 15
        elif screen_width == 2560 and screen_height == 1440:  # 2K
            return 20
        elif screen_width == 3840 and screen_height == 2160:  # 4K
            return 22
        else:
            return 15
