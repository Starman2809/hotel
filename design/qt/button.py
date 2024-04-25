from PyQt6.QtWidgets import QPushButton


class SimpleButton(QPushButton):
    button_css = "QPushButton { background-color: #007bff; color: #fff; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; } QPushButton:hover { background-color: #0056b3; } QPushButton:pressed { background-color: #28a745; }"

    def __init__(self, button_title, callback):
        super().__init__(button_title)
        self.setStyleSheet(self.button_css)
        self.clicked.connect(callback)
