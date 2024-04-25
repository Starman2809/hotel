from PyQt6 import QtCore
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QCalendarWidget, QSpacerItem, \
    QSizePolicy, QPushButton

from design.qt.button import SimpleButton


class QTAllActionsWindow(QWidget):
    window_title = "All actions window"
    window_geometry = QRect(0, 0, 1200, 600)

    def __init__(self, items_to_draw):

        super().__init__()
        self.setWindowTitle(self.window_title)
        self.setGeometry(self.window_geometry)
        self.setStyleSheet("font-family: Arial, sans-serif;")
        self.items_to_draw = items_to_draw
        self.init_ui()

    def init_ui(self):
        # Создаем вертикальный макет для главного окна
        main_layout = QVBoxLayout()

        # Создаем заголовок
        title_label = QLabel(self.window_title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        title_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; margin-bottom: 20px; color: black; background-color: #ddd;")
        main_layout.addWidget(title_label)

        self.add_objects_to_form(main_layout)

    def add_objects_to_form(self, main_layout):
        # Создаем сеточный макет для полей формы
        form_layout = QGridLayout()

        # Создаем и добавляем названия полей и поля для ввода
        for index, (field_name, field_callback) in enumerate(self.items_to_draw.items()):
            label = QLabel(f"{field_name}:")
            label.setStyleSheet("color: #333; font-size: 16px;")

            create_button = SimpleButton("Создать", field_callback["create"])
            read_button = SimpleButton("Читать", field_callback["read"])
            update_button = SimpleButton("Редактировать", field_callback["update"])
            delete_button = SimpleButton("Удалить", field_callback["delete"])

            form_layout.addWidget(label, index, 0)
            form_layout.addWidget(create_button, index, 1)
            form_layout.addWidget(read_button, index, 2)
            form_layout.addWidget(update_button, index, 3)
            form_layout.addWidget(delete_button, index, 4)

        # Добавляем сеточный макет с полями в вертикальный макет
        main_layout.addLayout(form_layout)

        # Создаем горизонтальный пространственный элемент перед кнопкой
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        main_layout.addItem(spacer_bottom)

        # Устанавливаем вертикальный макет для главного окна
        self.setLayout(main_layout)

    def on_submit_button_clicked(self):
        print(123132123)
