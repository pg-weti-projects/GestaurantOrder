from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QFrame
from PySide6.QtGui import QPixmap, QPalette, QBrush

from .additional_widgets.gesture_counter_widget import GestureCounterWidget


class SummaryOrderWidget(QWidget):
    """
    Class for summary order widget.
    """
    def __init__(self, parent: QMainWindow, monitor_geometry: dict, ordered_dish_data: list):
        super().__init__(parent)
        self.monitor_geometry = monitor_geometry
        self.ordered_dish_data = ordered_dish_data
        self.setGeometry(0, 0, monitor_geometry['width'], monitor_geometry['height'])
        self.setVisible(True)
        self.background_image_path: str = 'resources/img/summary_background.jpg'
        self.set_background(self.background_image_path)

        self.summary_dish_data: dict = {}
        self.total_price: int = 0
        self.generate_summary_dish_data()

        main_layout = QHBoxLayout(self)

        # Top layout
        self.top_layout = QVBoxLayout()
        self.top_layout_widget = QWidget()
        self.top_layout_widget.setLayout(self.top_layout)
        main_layout.addWidget(self.top_layout_widget, 4)

        # Carousel layout
        self.mid_layout = QVBoxLayout(self)
        self.mid_layout.setContentsMargins(0,80,0,80)
        self.mid_layout_widget = QWidget()
        self.mid_layout_widget.setLayout(self.mid_layout)
        self.create_centered_rectangle()
        main_layout.addWidget(self.mid_layout_widget, 3)

        # Bottom layout
        self.bottom_layout = QVBoxLayout()
        self.bottom_layout_widget = QWidget()
        self.bottom_layout_widget.setLayout(self.bottom_layout)
        self.gesture_counter = GestureCounterWidget()
        self._add_bottom_images_and_counter()
        main_layout.addWidget(self.bottom_layout_widget, 4)

        self.setLayout(main_layout)

    def generate_summary_dish_data(self):
        """
        Generate summary dict data for each dish where the key is the name of the dish and the value is the dict with
        amount of the dish, price for single dish and image path to the dish.
        """
        for dish in self.ordered_dish_data:
            dish_name = dish['dish_data']['name']
            dish_price = dish['dish_data']['price']
            amount = dish['amount']
            img_path = dish['dish_data']['img_path']
            if dish_name not in self.summary_dish_data:
                self.summary_dish_data[dish_name] = {"amount": amount, "price": dish_price, "img_path": img_path}
            else:
                self.summary_dish_data[dish_name]["amount"] += amount

            self.total_price += amount * dish_price

    def create_centered_rectangle(self):
        """
        Creates a centered rectangle in the middle layout containing a header, a scrollable area for items, and a
        total price summary.

        The rectangle has a semi-transparent white background with rounded corners. It displays item details
        such as name, amount, price, and total, along with a light gray scroll area and a custom-styled scrollbar.
        """
        rectangle_widget = QWidget(self)
        rectangle_widget.setObjectName("centeredRectangle")
        rectangle_widget.setStyleSheet("""
            QWidget#centeredRectangle {
                background-color: #f0f0f0;
                border-radius: 45px;
            }
        """)

        rectangle_layout = QVBoxLayout(rectangle_widget)

        # Top label
        header_label = QLabel("SUMMARY RECEIPT")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        rectangle_layout.addWidget(header_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
                QScrollArea {
                    background-color: #f0f0f0;
                }
                QScrollBar:vertical {
                    border: none;
                    background: #f0f0f0;
                    width: 10px;
                    margin: 0px 0px 0px 0px;
                }
                QScrollBar::handle:vertical {
                    background: #a0a0a0;
                    border-radius: 5px;
                    min-height: 30px;
                }
                QScrollBar::handle:vertical:hover {
                    background: #888888;
                }
                QScrollBar::add-line:vertical,
                QScrollBar::sub-line:vertical {
                    background: none;
                }
                QScrollBar::add-page:vertical,
                QScrollBar::sub-page:vertical {
                    background: none;
                }
            """)
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: #f0f0f0;")
        scroll_layout = QVBoxLayout(scroll_content)

        scroll_content_height = 0
        for dish_name, data in self.summary_dish_data.items():
            item_widget_height = 70
            amount = data['amount']
            price = data['price']
            img_path = data['img_path']
            total_dish_price = amount * price

            item_widget = QWidget()
            item_widget.setFixedHeight(item_widget_height)
            item_layout = QHBoxLayout(item_widget)

            img_label = QLabel()
            pixmap = QPixmap(img_path).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            img_label.setPixmap(pixmap)
            item_layout.addWidget(img_label)

            dish_label = QLabel(f"{dish_name} ({price} PLN) x{amount} - {total_dish_price} PLN")
            dish_label.setStyleSheet("font-size: 18px; color: black;")
            item_layout.addWidget(dish_label)

            scroll_layout.addWidget(item_widget, alignment=Qt.AlignLeft)
            scroll_content_height += item_widget_height

        scroll_content.setLayout(scroll_layout)
        scroll_content.setMaximumHeight(scroll_content_height)

        scroll_area.setWidget(scroll_content)
        rectangle_layout.addWidget(scroll_area)

        # Bottom price summary label
        bottom_summary_layout = QHBoxLayout()
        total_label = QLabel(f"TOTAL: {self.total_price} PLN")
        total_label.setStyleSheet("font-size: 18px; font-weight: bold; color: black;")
        total_label.setAlignment(Qt.AlignCenter)
        bottom_summary_layout.addWidget(total_label)
        rectangle_layout.addLayout(bottom_summary_layout)

        self.mid_layout.addWidget(rectangle_widget)

    def _add_bottom_images_and_counter(self) -> None:
        """
        Adds bottom layout with gestures icons and counter widget.
        """
        right_corner_layout = QHBoxLayout()
        right_corner_layout.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        right_corner_layout.addWidget(self.gesture_counter)

        image_paths = [
            'resources/img/gesture_img/thumb_up.png'
        ]
        labels = ["CLOSE"]

        for image_path, label_text in zip(image_paths, labels):
            widget = QWidget()
            layout = QVBoxLayout(widget)

            image_label = QLabel()
            pixmap = QPixmap(image_path)
            image_label.setPixmap(pixmap.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio))

            text_label = QLabel(label_text)
            text_label.setStyleSheet("font-weight: bold; color: white;")

            layout.addWidget(image_label, alignment=Qt.AlignCenter)
            layout.addWidget(text_label, alignment=Qt.AlignCenter)

            widget.setFixedSize(110, 110)
            right_corner_layout.addWidget(widget)

        self.bottom_layout.addLayout(right_corner_layout)

    def confirm_order(self):
        pass

    def cancel_order(self):
        pass

    def resizeEvent(self, event):
        """resizeEvent method override to adjust background image to new app size"""
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
