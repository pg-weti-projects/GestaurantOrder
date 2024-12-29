import logging
from Mongo.mongo_manager import MongoManager

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QFont, QDoubleValidator
from PySide6.QtWidgets import (QMainWindow, QWidget, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel,
                               QFileDialog, QApplication, QHBoxLayout, QAbstractItemView, QLineEdit)
from bson import ObjectId

logger = logging.getLogger("app")

class AdminPanel(QWidget):
    """
    Class responsible for admin GUI operations. This widget is one of the main ones and is a part of the QStackedWidget.
    """
    db_data_changed = Signal()

    def __init__(self, parent: QMainWindow):
        super().__init__(parent)

        # Database
        self.mongo_manager = MongoManager()

        self.image_paths = {}
        # Monitor geometry
        monitor = QApplication.primaryScreen().geometry()
        m_width = monitor.width()
        m_height = monitor.height()
        table_width = int(m_width * 0.75)
        table_height = int(m_height * 0.75)

        # Buttons
        self.add_dish_button = QPushButton("Add new meal")
        self.add_dish_button.setFixedSize(int(m_width * 0.10), int(m_width * 0.05))
        self.add_dish_button.clicked.connect(self.add_dish)

        self.delete_dish_button = QPushButton("Delete selected meal")
        self.delete_dish_button.setFixedSize(int(m_width * 0.10), int(m_width * 0.05))
        self.delete_dish_button.clicked.connect(self.delete_dish)

        # Table
        self.dish_table = QTableWidget()
        self.dish_table.setColumnCount(4)
        self.dish_table.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.dish_table.setHorizontalHeaderLabels(["ID", "Name", "Price", "Image"])
        self.dish_table.cellChanged.connect(self.edit_dish)

        self.dish_table.setColumnWidth(0, int(table_width * 0.2))  # ID
        self.dish_table.setColumnWidth(1, int(table_width * 0.4))  # Name
        self.dish_table.setColumnWidth(2, int(table_width * 0.2))  # Price
        self.dish_table.setColumnWidth(3, int(table_width * 0.2))  # Image
        self.dish_table.setFixedSize(table_width, table_height)

        header = self.dish_table.horizontalHeader()
        header.setStretchLastSection(True)

        # Layouts
        button_layout = QVBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.add_dish_button)
        button_layout.setSpacing(40)
        button_layout.addWidget(self.delete_dish_button)

        admin_label = QLabel("Admin Panel")
        admin_label.setAlignment(Qt.AlignCenter)

        font = QFont()
        font.setPointSize(24)
        admin_label.setFont(font)

        main_layout = QVBoxLayout()
        main_layout.addWidget(admin_label)
        main_layout.addSpacing(40)

        table_button_layout = QHBoxLayout()
        table_button_layout.addWidget(self.dish_table)
        table_button_layout.addLayout(button_layout)

        button_layout.addStretch()
        main_layout.addLayout(table_button_layout)

        self.setLayout(main_layout)

        self.update_dish_list()
        self.dish_table.cellDoubleClicked.connect(self.price_validator)

    def load_dishes_from_db(self):
        """
        Loud and set all dishes from the database.
        """
        return self.mongo_manager.get_order_list()

    def update_dish_list(self):
        """
        Update dishes from the database.
        """
        self.dish_table.setRowCount(0)
        dishes = self.load_dishes_from_db()

        for dish in dishes:
            row_position = self.dish_table.rowCount()
            self.dish_table.insertRow(row_position)

            id_item = QTableWidgetItem(str(dish['_id']))
            id_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.dish_table.setItem(row_position, 0, id_item)

            self.dish_table.setItem(row_position, 1, QTableWidgetItem(dish['name']))
            self.dish_table.setItem(row_position, 2, QTableWidgetItem(str(dish['price'])))

            if 'image_path' in dish and dish['image_path'] != "":
                pixmap = QPixmap(dish['image_path']).scaled(50, 50)
                label = QLabel()
                label.setPixmap(pixmap)
                self.dish_table.setCellWidget(row_position, 3, label)
            else:
                add_image_button = QPushButton("Add Image")
                add_image_button.setFixedSize(80, 30)
                add_image_button.clicked.connect(lambda _, row=row_position: self.add_image(row))
                self.dish_table.setCellWidget(row_position, 3, add_image_button)

    def add_dish(self):
        """
        Add new dish with price and img to the table.
        """
        row_position = self.dish_table.rowCount()
        self.dish_table.insertRow(row_position)

        self.dish_table.setItem(row_position, 0, QTableWidgetItem(""))
        self.dish_table.setItem(row_position, 1, QTableWidgetItem("New Dish"))
        self.dish_table.setItem(row_position, 2, QTableWidgetItem("0.0"))

        add_image_button = QPushButton("Add Image")
        add_image_button.setFixedSize(80, 30)
        add_image_button.clicked.connect(lambda: self.add_image(row_position))
        self.dish_table.setCellWidget(row_position, 3, add_image_button)

    def delete_dish(self):
        """
        Delete selected dish from the database and view.
        """
        current_row = self.dish_table.currentRow()
        if current_row != -1:
            dish_id = self.dish_table.item(current_row, 0).text()
            if dish_id:
                success = self.mongo_manager.delete_record(dish_id)
                if success:
                    self.dish_table.removeRow(current_row)
                    logger.info(f"Successfully deleted dish with ID: {dish_id}")
                    self.db_data_changed.emit()
                else:
                    logger.error(f"Failed to delete dish with ID: {dish_id} from database.")


    def edit_dish(self, row, column):
        """
        Select row to edit dish and update it on database.
        """
        if column in [1, 2]:
            dish_id = self.dish_table.item(row, 0).text()
            name = self.dish_table.item(row, 1).text()
            price_item = self.dish_table.item(row, 2)
            price = float(price_item.text()) if price_item and price_item.text() else 0.0

            if not dish_id:
                new_dish = {"name": name, "price": price, "image_path": ""}
                new_dish_id = self.mongo_manager.add_record(new_dish)
                self.dish_table.setItem(row, 0, QTableWidgetItem(str(new_dish_id)))
            else:
                updated_dish = {"_id": dish_id, "name": name, "price": price}

                if dish_id in self.image_paths:
                    updated_dish['image_path'] = self.image_paths[dish_id]
                else:
                    if dish_id not in self.image_paths:
                        existing_dish = self.mongo_manager.get_dish_by_id(dish_id)
                        if existing_dish and 'image_path' in existing_dish:
                            updated_dish['image_path'] = existing_dish['image_path']


                self.mongo_manager.update_record(updated_dish)
            self.db_data_changed.emit()

        if column == 3:
            self.add_image(row)

    def price_validator(self, row, column):
        """
        Apply a Validator to the price column editor on cell edit.
        """
        if column == 2:
            price_editor = QLineEdit(self.dish_table)
            price_validator = QDoubleValidator(0.0, 9999.99, 2)
            price_validator.setNotation(QDoubleValidator.StandardNotation)
            price_editor.setValidator(price_validator)
            price_editor.setAlignment(Qt.AlignRight)

            price_editor.editingFinished.connect(lambda: self.finish_editing_price(row, column, price_editor))

            self.dish_table.setCellWidget(row, column, price_editor)
            price_editor.setFocus()

    def finish_editing_price(self, row, column, editor):
        """
        Replace the QLineEdit editor in the cell with a QTableWidgetItem after editing.
        """
        new_price_text = editor.text()

        self.dish_table.removeCellWidget(row, column)
        self.dish_table.setItem(row, column, QTableWidgetItem(new_price_text))

    @staticmethod
    def get_image_path_from_label(label):
        return label.pixmap().data() if hasattr(label.pixmap(), 'data') else ""

    def add_image(self, row):
        """
        Add image to the dish table and set image path from your local path.
        """
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(self, "Choose Image", "",
                                                    "Images (*.png *.jpg *.bmp)")
        if image_path:
            self.image_paths[row] = image_path
            pixmap = QPixmap(image_path).scaled(50, 50)
            label = QLabel()
            label.setPixmap(pixmap)
            self.dish_table.setCellWidget(row, 3, label)

            dish_id = self.dish_table.item(row, 0).text()
            name = self.dish_table.item(row, 1).text()
            price = float(self.dish_table.item(row, 2).text())

            if dish_id:
                self.image_paths[dish_id] = image_path

                updated_dish = {"_id": dish_id, "name": name, "price": price, "image_path": image_path}
                self.mongo_manager.update_record(updated_dish)

            if not dish_id:
                new_dish = {"name": name, "price": price, "image_path": image_path}
                new_dish_id = self.mongo_manager.add_record(new_dish)
                self.dish_table.setItem(row, 0, QTableWidgetItem(str(new_dish_id)))
            else:
                updated_dish = {"_id": dish_id, "name": name, "price": price, "image_path": image_path}
                self.mongo_manager.update_record(updated_dish)
            self.db_data_changed.emit()
