from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QHBoxLayout


class Widget(QWidget):
    """
    Sample widget class.
    """
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        row_layout1 = QHBoxLayout()
        row_layout2 = QHBoxLayout()

        for i in range(1, 7):
            button = QPushButton(f"Przycisk {i}", self)
            button.setFixedSize(200, 200)
            button.setStyleSheet("""
                        QPushButton:focus {
                            border: 2px solid blue;
                        }
                    """)
            if i <= 3:
                row_layout1.addWidget(button)
            else:
                row_layout2.addWidget(button)

        layout.addLayout(row_layout1)
        layout.addLayout(row_layout2)

        self.setLayout(layout)
