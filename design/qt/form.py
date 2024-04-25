from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QRect, QLocale
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QSpacerItem, QSizePolicy,
                             QPushButton, QCalendarWidget)

from design.qt.table import QTClientsTable, QTAvailableRoomsTable


class QTBaseForm(QWidget):
    window_title = "Table Example"
    window_geometry = QRect(0, 0, 800, 600)

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.window_title)
        self.setGeometry(self.window_geometry)
        self.setStyleSheet("font-family: Arial, sans-serif;")

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
        for i in range(5):
            label = QLabel(f"Поле {i + 1}:")
            label.setStyleSheet("color: #333; font-size: 16px;")
            edit = QLineEdit()
            edit.setStyleSheet("padding: 6px; border: 1px solid #ccc; border-radius: 4px; font-size: 16px;"
                               "background-color: #fff;")
            edit.setObjectName(f"edit_{i}")  # Добавляем objectName для дальнейшей настройки стилей через CSS
            form_layout.addWidget(label, i, 0)
            form_layout.addWidget(edit, i, 1)

        calendar = QCalendarWidget()

        calendar.setStyleSheet(
            "QCalendarWidget QAbstractItemView { color: black; }"
            "QCalendarWidget QToolButton { color: black; }"
        )

        form_layout.addWidget(calendar, 5, 1, 5, 1)  # Размещаем календарь в столбце 1 и ряду 0, занимая 5 рядов

        # Добавляем сеточный макет с полями в вертикальный макет
        main_layout.addLayout(form_layout)

        # Создаем горизонтальный пространственный элемент перед кнопкой
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        main_layout.addItem(spacer_bottom)

        # Создаем кнопку "Отправить"
        self.submit_button = QPushButton("Отправить")
        self.submit_button.setStyleSheet(
            "QPushButton { background-color: #007bff; color: #fff; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; }"
            "QPushButton:hover { background-color: #0056b3; }"
            "QPushButton:pressed { background-color: #28a745; }")  # Изменяем цвет при нажатии
        self.submit_button.clicked.connect(self.on_submit_button_clicked)
        main_layout.addWidget(self.submit_button,
                              alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)

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


class QTBookingSearchForm(QTBaseForm):
    window_title = "Поиск доступных номеров"
    window_geometry = QRect(100, 100, 1200, 600)

    def __init__(self):
        russian_locale = QLocale(QLocale.Language.Russian, QLocale.Country.Russia)
        calendar_style = """
                    QAbstractItemView { border: 2px solid black; }
                """

        self.calendar_date_from = QCalendarWidget()
        self.calendar_date_to = QCalendarWidget()

        self.calendar_date_from.setLocale(russian_locale)
        self.calendar_date_from.setStyleSheet(calendar_style)
        self.calendar_date_from.setMinimumHeight(180)
        self.calendar_date_from.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)

        self.calendar_date_to.setLocale(russian_locale)
        self.calendar_date_to.setStyleSheet(calendar_style)
        self.calendar_date_to.setMinimumHeight(180)
        self.calendar_date_to.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)

        super().__init__()

    def add_objects_to_form(self, main_layout):
        # Создаем сеточный макет для полей формы
        form_layout = QGridLayout()

        form_layout.addWidget(self.calendar_date_from, 0, 0, 5, 1)
        form_layout.addWidget(self.calendar_date_to, 0, 1, 5, 1)

        # Добавляем сеточный макет с полями в вертикальный макет
        main_layout.addLayout(form_layout)

        # Создаем горизонтальный пространственный элемент перед кнопкой
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        main_layout.addItem(spacer_bottom)

        # Создаем кнопку "Отправить"
        self.submit_button = QPushButton("Отправить")
        self.submit_button.setStyleSheet(
            "QPushButton { background-color: #007bff; color: #fff; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; }"
            "QPushButton:hover { background-color: #0056b3; }"
            "QPushButton:pressed { background-color: #28a745; }")  # Изменяем цвет при нажатии
        self.submit_button.clicked.connect(self.on_submit_button_clicked)
        main_layout.addWidget(self.submit_button,
                              alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)

        # Устанавливаем вертикальный макет для главного окна
        self.setLayout(main_layout)

    def on_submit_button_clicked(self):
        date_from = self.calendar_date_from.selectedDate()
        print("Выбранная дата в календаре 1:", date_from.toString())

        date_to = self.calendar_date_to.selectedDate()
        print("Выбранная дата в календаре 2:", date_to.toString())

        available_rooms = QTAvailableRoomsTable(date_from.toPyDate(), date_to.toPyDate())
        available_rooms.show()
