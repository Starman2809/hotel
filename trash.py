import sys

from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt

from hotel.view import ClientView


class MainForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Название формы")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f0f0f0; font-family: Arial, sans-serif;")

        self.init_ui()

    def init_ui(self):
        # Создаем вертикальный макет для главного окна
        main_layout = QVBoxLayout()

        # Создаем заголовок
        title_label = QLabel("Название формы")
        title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px; color: black; background-color: #ddd;")
        main_layout.addWidget(title_label)

        # Создаем сеточный макет для полей формы
        form_layout = QGridLayout()

        # Создаем и добавляем названия полей и поля для ввода
        for i in range(5):
            label = QLabel(f"Поле {i + 1}:")
            label.setStyleSheet("color: #333; font-size: 16px;")
            edit = QLineEdit()
            edit.setStyleSheet("padding: 6px; border: 1px solid #ccc; border-radius: 4px; font-size: 16px;"
                               "background-color: #fff;")
            edit.setObjectName(f"edit_{i}")  # Добавляем objectName для дальнейшей настройки стилей через CSS
            form_layout.addWidget(label, i, 0)
            form_layout.addWidget(edit, i, 1)

        # Добавляем сеточный макет с полями в вертикальный макет
        main_layout.addLayout(form_layout)

        # Создаем горизонтальный пространственный элемент перед кнопкой
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        main_layout.addItem(spacer_bottom)

        # Создаем кнопку "Отправить"
        self.submit_button = QPushButton("Отправить")
        self.submit_button.setStyleSheet("QPushButton { background-color: #007bff; color: #fff; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; }"
                                         "QPushButton:hover { background-color: #0056b3; }"
                                         "QPushButton:pressed { background-color: #28a745; }")  # Изменяем цвет при нажатии
        self.submit_button.clicked.connect(self.on_submit_button_clicked)
        main_layout.addWidget(self.submit_button, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)

        # Устанавливаем вертикальный макет для главного окна
        self.setLayout(main_layout)

        # Привязываем события наведения курсора на поля ввода
        for i in range(5):
            edit_widget = self.findChild(QLineEdit, f"edit_{i}")
            if edit_widget:
                edit_widget.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.Enter:
            if isinstance(obj, QLineEdit):
                obj.setStyleSheet("padding: 6px; border: 1px solid #007bff; border-radius: 4px; font-size: 16px;"
                                   "background-color: #fff;")
        elif event.type() == QtCore.QEvent.Type.Leave:
            if isinstance(obj, QLineEdit):
                obj.setStyleSheet("padding: 6px; border: 1px solid #ccc; border-radius: 4px; font-size: 16px;"
                                   "background-color: #fff;")
        return super().eventFilter(obj, event)

    def on_submit_button_clicked(self):
        pass


def main():
    print(123)
    client_view = ClientView()
    # client_view.create_new_view_window()
    client_view.read_all()
    # client_id = 5
    # client_view.update_view_window(client_id)
    pass
    # app = QApplication(sys.argv)
    # form = MainForm()
    # form.show()
    # sys.exit(app.exec())


if __name__ == "__main__":
    main()