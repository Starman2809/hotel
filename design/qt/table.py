from functools import partial

from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout, QWidget, QPushButton

from db.serializers import ClientDataSerializer
from hotel.controller import ClientController
from hotel.models import Client


class QTBaseTable(QMainWindow):
    columns = 9
    window_title = "Table Example"

    def __init__(self, width, rows=100):
        super().__init__()
        self.setWindowTitle(self.window_title)
        self.setGeometry(100, 100, width, 600)

        # Создаем таблицу
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(rows)  # Устанавливаем количество строк
        self.tableWidget.setColumnCount(self.columns)  # Устанавливаем количество столбцов

        # Заполняем таблицу данными
        self.fill_table()

        self.set_header_labels()

        # Применяем стили для заголовков таблицы
        header = self.tableWidget.horizontalHeader()
        header.setStyleSheet("""
            color: #000000; /* Цвет текста */
            border: 1px solid #dee2e6; /* Серый бордюр */
            border-radius: 4px; /* Закругленные углы */
        """)

        # Устанавливаем растягивание столбцов по содержимому
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Создаем вертикальный Layout и добавляем в него таблицу
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)

        # Создаем центральный виджет и устанавливаем в него Layout
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def set_header_labels(self):
        # Устанавливаем горизонтальные заголовки
        self.tableWidget.setHorizontalHeaderLabels([f"Column {col + 1}" for col in range(self.columns)])

    def fill_table(self):
        for row in range(100):
            for col in range(self.columns):
                item = QTableWidgetItem(f"Row {row + 1}, Col {col + 1}")
                self.tableWidget.setItem(row, col, item)


class QTClientsTable(QTBaseTable):
    width = 1000
    window_title = "Список всех клиентов"
    columns = 8
    items_to_draw = ["Фамилия", "Имя", "Отчество", "Дата рождения", "Электронная почта", "Номер телефона",
                     "Номер паспорта", ]

    def __init__(self):
        self.all_clients_data = ClientDataSerializer.prepare_data_to_print(Client.all())
        self.rows = len(self.all_clients_data)
        super().__init__(width=self.width, rows=self.rows)

    def set_header_labels(self):
        # Устанавливаем горизонтальные заголовки
        self.tableWidget.setHorizontalHeaderLabels(self.items_to_draw)

    def fill_table(self):
        for index, row in enumerate(self.all_clients_data):
            self.tableWidget.setItem(index, 0, QTableWidgetItem(f"{row["last_name"]}"))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(f"{row["first_name"]}"))
            self.tableWidget.setItem(index, 2, QTableWidgetItem(f"{row["patronymic"]}"))
            self.tableWidget.setItem(index, 3, QTableWidgetItem(f"{row["birthday_date"]}"))
            self.tableWidget.setItem(index, 4, QTableWidgetItem(f"{row["email"]}"))
            self.tableWidget.setItem(index, 5, QTableWidgetItem(f"{row["phone_number"]}"))
            self.tableWidget.setItem(index, 6, QTableWidgetItem(f"{row["passport_number"]}"))

            button = QPushButton("Удалить")
            button.clicked.connect(partial(self.delete_client, row["id"]))
            self.tableWidget.setCellWidget(index, 7, button)

    def delete_client(self, client_id):
        ClientController.submit_delete(client_id=client_id)
        self.update_table()

    def update_table(self):
        self.all_clients_data = ClientDataSerializer.prepare_data_to_print(Client.all())
        self.tableWidget.clearContents()
        self.fill_table()
