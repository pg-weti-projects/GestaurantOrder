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

        images = ("carbonara.png", "pizza.png", "kebab.png", "burger.png", "sandwich.png", "ramen.png")

        for i in range(0, 6):
            button = QPushButton(images[i], self) # TODO fix background buttons image that will work with blue frame
            button.setFixedSize(250, 250)

            button.setStyleSheet(f"""
                    QPushButton:focus {{
                        border: 5px solid blue;
                    }}
                """)

            if i < 3:
                row_layout1.addWidget(button)
            else:
                row_layout2.addWidget(button)

        layout.addLayout(row_layout1)
        layout.addLayout(row_layout2)

        self.setLayout(layout)
