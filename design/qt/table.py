from functools import partial

from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout, QWidget, QPushButton

from db.serializers import ClientDataSerializer, HotelRoomSerializer, BookingSerializer
from hotel.controller import ClientController, BookingController
from hotel.models import Client, HotelRoom, Booking


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
        self.tableWidget.resizeColumnsToContents()

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


class QTBookingsTable(QTBaseTable):
    width = 1000
    window_title = "Список всех бронирований"
    columns = 9
    items_to_draw = ["id Номера", "ФИО сотрудника", "Дата приезда", "Дата отъезда", "Дата бронирования", "Форма оплаты", "Клиент",
                     "Статус оплаты", "Итоговая стоимость"]

    def __init__(self):
        self.all_bookings_data = BookingSerializer.prepare_data_to_print(Booking.all())
        self.rows = len(self.all_bookings_data)
        super().__init__(width=self.width, rows=self.rows)

    def set_header_labels(self):
        # Устанавливаем горизонтальные заголовки
        self.tableWidget.setHorizontalHeaderLabels(self.items_to_draw)

    def fill_table(self):
        for index, row in enumerate(self.all_bookings_data):
            self.tableWidget.setItem(index, 0, QTableWidgetItem(f"{row["room_id"]}"))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(f"{row["employee_full_name"]}"))
            self.tableWidget.setItem(index, 2, QTableWidgetItem(f"{row["date_from"]}"))
            self.tableWidget.setItem(index, 3, QTableWidgetItem(f"{row["date_to"]}"))
            self.tableWidget.setItem(index, 4, QTableWidgetItem(f"{row["creation_date"]}"))
            self.tableWidget.setItem(index, 5, QTableWidgetItem(f"{row["payment_type"]}"))
            self.tableWidget.setItem(index, 6, QTableWidgetItem(f"{row["client"]}"))
            self.tableWidget.setItem(index, 7, QTableWidgetItem(f"{row["payment_status"]}"))
            self.tableWidget.setItem(index, 8, QTableWidgetItem(f"{row["final_price"]}"))


class QTAvailableRoomsTable(QTBaseTable):
    width = 1000
    window_title = "Список доступных комнат"
    columns = 6
    items_to_draw = ["id Номера", "Сотрудник", "Категория", "Описание", "Стоимость"]

    def __init__(self, date_from, date_to):
        self.available_rooms_data = HotelRoomSerializer.prepare_data_to_print(HotelRoom.get_available_rooms(date_from, date_to))
        self.rows = len(self.available_rooms_data)
        super().__init__(width=self.width, rows=self.rows)

    def set_header_labels(self):
        # Устанавливаем горизонтальные заголовки
        self.tableWidget.setHorizontalHeaderLabels(self.items_to_draw)

    def fill_table(self):
        # hotel_room_info_dict = {
        #                 "id": row[0],
        #                 "employee_full_name": f"{row[1]} {row[2]} {row[3]}",
        #                 "room_type_name": row[4],
        #                 "room_type_description": insert_new_lines(row[5], 40),
        #                 "room_type_price": row[6],
        #                 "active": convert_number_to_status(row[7]),
        #             }
        for index, row in enumerate(self.available_rooms_data):
            self.tableWidget.setItem(index, 0, QTableWidgetItem(f"{row["id"]}"))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(f"{row["employee_full_name"]}"))
            self.tableWidget.setItem(index, 2, QTableWidgetItem(f"{row["room_type_name"]}"))
            self.tableWidget.setItem(index, 3, QTableWidgetItem(f"{row["room_type_description"]}"))
            self.tableWidget.setItem(index, 4, QTableWidgetItem(f"{row["room_type_price"]}"))

            button = QPushButton("Забронировать")
            button.clicked.connect(partial(self.book_room, row["id"]))
            self.tableWidget.setCellWidget(index, 5, button)

    def book_room(self, room_id):
        print(room_id)
        # BookingController.submit_create(room_id=room_id)
        # self.update_table()

    def update_table(self):
        pass
        # self.available_rooms_data = ClientDataSerializer.prepare_data_to_print(HotelRoom.all())
        # self.tableWidget.clearContents()
        # self.fill_table()
