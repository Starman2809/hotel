from functools import partial

from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout, QWidget, QPushButton

from db.serializers import ClientDataSerializer, HotelRoomSerializer, BookingSerializer, PaymentTypeSerializer, \
    EmployeeSerializer, JobPositionSerializer, DepartmentSerializer, WorkScheduleSerializer, RoomTypeSerializer, \
    AdditionalServiceSerializer
from design.qt.style import red_qt_push_button, green_qt_push_button
from hotel.controller import ClientController, BookingController
from hotel.models import Client, HotelRoom, Booking, PaymentType, Employee, JobPosition, Department, WorkSchedule, \
    RoomType, AdditionalServiceType


class QTBaseTable(QMainWindow):
    columns = 9
    window_title = "Table Example"
    items_to_draw = ["col{1}" for i in range(columns)]

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
        self.tableWidget.setHorizontalHeaderLabels(self.items_to_draw)

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


    def fill_table(self):
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


class QTPaymentTypeTable(QTBaseTable):
    width = 1000
    window_title = "Способы оплаты"
    columns = 3
    items_to_draw = ["id Оплаты", "Описание оплаты"]

    def __init__(self):
        self.all_data = PaymentTypeSerializer.prepare_data_to_print(PaymentType.all())
        self.rows = len(self.all_data)
        super().__init__(width=self.width, rows=self.rows)

    def fill_table(self):
        for index, row in enumerate(self.all_data):
            self.tableWidget.setItem(index, 0, QTableWidgetItem(f"{row["id"]}"))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(f"{row["payment_type_description"]}"))

            button = QPushButton("Удалить")
            button.clicked.connect(partial(self.delete_item, row["id"]))
            self.tableWidget.setCellWidget(index, 2, button)

    def delete_item(self, client_id):
        pass
        # ClientController.submit_delete(client_id=client_id)
        # self.update_table()

    def update_table(self):
        pass
        # self.all_clients_data = ClientDataSerializer.prepare_data_to_print(Client.all())
        # self.tableWidget.clearContents()
        # self.fill_table()


class QTEmployeeTable(QTBaseTable):

    width = 1000
    window_title = "Сотрудники"
    items_to_draw = ["Номер", "Фамилия", "Имя", "Отчество", "Дата рождения", "Номер паспорта", "Должность", "Электронная почта", "Номер телефона", "Дата найма", "Зарплата", "Отдел", "График работы", "Статус"]
    columns = len(items_to_draw)+1

    def __init__(self):
        self.all_data = EmployeeSerializer.prepare_data_to_print(Employee.all())
        self.rows = len(self.all_data)
        super().__init__(width=self.width, rows=self.rows)

    def fill_table(self):
        for index, row in enumerate(self.all_data):
            self.tableWidget.setItem(index, 0, QTableWidgetItem(f"{row["id"]}"))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(f"{row["last_name"]}"))
            self.tableWidget.setItem(index, 2, QTableWidgetItem(f"{row["first_name"]}"))
            self.tableWidget.setItem(index, 3, QTableWidgetItem(f"{row["patronymic"]}"))
            self.tableWidget.setItem(index, 4, QTableWidgetItem(f"{row["birthday_date"]}"))
            self.tableWidget.setItem(index, 5, QTableWidgetItem(f"{row["passport_number"]}"))
            self.tableWidget.setItem(index, 6, QTableWidgetItem(f"{row["job_position"]}"))
            self.tableWidget.setItem(index, 7, QTableWidgetItem(f"{row["email"]}"))
            self.tableWidget.setItem(index, 8, QTableWidgetItem(f"{row["phone_number"]}"))
            self.tableWidget.setItem(index, 9, QTableWidgetItem(f"{row["hiring_date"]}"))
            self.tableWidget.setItem(index, 10, QTableWidgetItem(f"{row["salary"]}"))
            self.tableWidget.setItem(index, 11, QTableWidgetItem(f"{row["department"]}"))
            self.tableWidget.setItem(index, 12, QTableWidgetItem(f"{row["work_schedule"]}"))
            self.tableWidget.setItem(index, 13, QTableWidgetItem(f"{row["work_status"]}"))

            button = QPushButton("Удалить")
            button.clicked.connect(partial(self.delete_item, row["id"]))
            self.tableWidget.setCellWidget(index, 14, button)

    def delete_item(self, client_id):
        pass
        # EmployeeController.submit_delete(employee_id=employee_id)
        # self.update_table()

    def update_table(self):
        pass
        # self.all_employees_data = EmployeeSerializer.prepare_data_to_print(Employee.all())
        # self.tableWidget.clearContents()
        # self.fill_table()


class QTJobPositionTable(QTBaseTable):
    width = 1000
    window_title = "Должности"
    items_to_draw = ["Номер", "Название"]
    columns = len(items_to_draw)+1

    def __init__(self):
        self.all_data = JobPositionSerializer.prepare_data_to_print(JobPosition.all())
        self.rows = len(self.all_data)
        super().__init__(width=self.width, rows=self.rows)

    def fill_table(self):
        for index, row in enumerate(self.all_data):
            self.tableWidget.setItem(index, 0, QTableWidgetItem(f"{row["id"]}"))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(f"{row["job_title"]}"))

            button = QPushButton("Удалить")
            button.clicked.connect(partial(self.delete_item, row["id"]))
            self.tableWidget.setCellWidget(index, 2, button)

    def delete_item(self, client_id):
        pass
        # EmployeeController.submit_delete(employee_id=employee_id)
        # self.update_table()

    def update_table(self):
        pass
        # self.all_employees_data = EmployeeSerializer.prepare_data_to_print(Employee.all())
        # self.tableWidget.clearContents()
        # self.fill_table()

class QTDepartmentTable(QTBaseTable):
    width = 1000
    window_title = "Отделы"
    items_to_draw = ["Номер", "Название"]
    columns = len(items_to_draw)+1

    def __init__(self):
        self.all_data = DepartmentSerializer.prepare_data_to_print(Department.all())
        self.rows = len(self.all_data)
        super().__init__(width=self.width, rows=self.rows)

    def fill_table(self):
        for index, row in enumerate(self.all_data):
            self.tableWidget.setItem(index, 0, QTableWidgetItem(f"{row["id"]}"))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(f"{row["department_title"]}"))

            button = QPushButton("Удалить")
            button.clicked.connect(partial(self.delete_item, row["id"]))
            self.tableWidget.setCellWidget(index, 2, button)

    def delete_item(self, client_id):
        pass
        # EmployeeController.submit_delete(employee_id=employee_id)
        # self.update_table()

    def update_table(self):
        pass
        # self.all_employees_data = EmployeeSerializer.prepare_data_to_print(Employee.all())
        # self.tableWidget.clearContents()
        # self.fill_table()


class QTWorkScheduleTable(QTBaseTable):
    width = 1000
    window_title = "График работы"
    items_to_draw = ["Номер", "Название"]
    columns = len(items_to_draw)+1

    def __init__(self):
        self.all_data = WorkScheduleSerializer.prepare_data_to_print(WorkSchedule.all())
        self.rows = len(self.all_data)
        super().__init__(width=self.width, rows=self.rows)

    def fill_table(self):
        for index, row in enumerate(self.all_data):
            self.tableWidget.setItem(index, 0, QTableWidgetItem(f"{row["id"]}"))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(f"{row["work_schedule_title"]}"))

            button = QPushButton("Удалить")
            button.clicked.connect(partial(self.delete_item, row["id"]))
            self.tableWidget.setCellWidget(index, 2, button)

    def delete_item(self, client_id):
        pass
        # EmployeeController.submit_delete(employee_id=employee_id)
        # self.update_table()

    def update_table(self):
        pass
        # self.all_employees_data = EmployeeSerializer.prepare_data_to_print(Employee.all())
        # self.tableWidget.clearContents()
        # self.fill_table()


class QTHotelRoomTable(QTBaseTable):
    width = 1200
    window_title = "Номера"
    items_to_draw = ["Номер", "ФИО сотрудника", "Тип", "Описание", "Цена", "Активна"]
    columns = len(items_to_draw)+1

    def __init__(self):
        self.all_data = HotelRoomSerializer.prepare_data_to_print(HotelRoom.all())
        self.rows = len(self.all_data)
        super().__init__(width=self.width, rows=self.rows)

    def fill_table(self):
        for index, row in enumerate(self.all_data):
            self.tableWidget.setItem(index, 0, QTableWidgetItem(f"{row["id"]}"))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(f"{row["employee_full_name"]}"))
            self.tableWidget.setItem(index, 2, QTableWidgetItem(f"{row["room_type_name"]}"))
            self.tableWidget.setItem(index, 3, QTableWidgetItem(f"{row["room_type_description"]}"))
            self.tableWidget.setItem(index, 4, QTableWidgetItem(f"{row["room_type_price"]}"))
            self.tableWidget.setItem(index, 5, QTableWidgetItem(f"{row["active"]}"))

            if row['active'] == "Да":
                button = QPushButton("Деактивировать")
                button.setStyleSheet(red_qt_push_button)
                button.clicked.connect(partial(self.deactivate_hotel_room, row["id"]))
            else:
                button = QPushButton("Активировать")
                button.setStyleSheet(green_qt_push_button)
                button.clicked.connect(partial(self.activate_hotel_room, row["id"]))

            self.tableWidget.setCellWidget(index, 6, button)

    def deactivate_hotel_room(self, client_id):
        pass
        # HotelRoom.deactivate(room_id)
        # self.update_table()

    def activate_hotel_room(self, client_id):
        pass
        # HotelRoom.activate(room_id)
        # self.update_table()

    def update_table(self):
        pass
        # self.all_employees_data = EmployeeSerializer.prepare_data_to_print(Employee.all())
        # self.tableWidget.clearContents()
        # self.fill_table()

class QTRoomTypeTable(QTBaseTable):
    width = 1000
    window_title = "Типы номеров"
    items_to_draw = ["Номер", "Название", "Описание", "Стоимость"]
    columns = len(items_to_draw)+1

    def __init__(self):
        self.all_data = RoomTypeSerializer.prepare_data_to_print(RoomType.all())
        self.rows = len(self.all_data)
        super().__init__(width=self.width, rows=self.rows)

    def fill_table(self):
        for index, row in enumerate(self.all_data):
            self.tableWidget.setItem(index, 0, QTableWidgetItem(f"{row["id"]}"))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(f"{row["title"]}"))
            self.tableWidget.setItem(index, 2, QTableWidgetItem(f"{row["description"]}"))
            self.tableWidget.setItem(index, 3, QTableWidgetItem(f"{row["price"]}"))

            button = QPushButton("Удалить")
            button.clicked.connect(partial(self.delete_item, row["id"]))
            self.tableWidget.setCellWidget(index, 4, button)

    def delete_item(self, client_id):
        pass
        # EmployeeController.submit_delete(employee_id=employee_id)
        # self.update_table()

    def update_table(self):
        pass
        # self.all_employees_data = EmployeeSerializer.prepare_data_to_print(Employee.all())
        # self.tableWidget.clearContents()
        # self.fill_table()


class QTAdditionalServiceTable(QTBaseTable):
    width = 1000
    window_title = "Дополнительные услуги"
    items_to_draw = ["Номер", "Название", "Описание", "Стоимость"]
    columns = len(items_to_draw)+1

    def __init__(self):
        self.all_data = AdditionalServiceSerializer.prepare_data_to_print(AdditionalServiceType.all())
        self.rows = len(self.all_data)
        super().__init__(width=self.width, rows=self.rows)

    def fill_table(self):
        for index, row in enumerate(self.all_data):
            self.tableWidget.setItem(index, 0, QTableWidgetItem(f"{row["id"]}"))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(f"{row["service_name"]}"))
            self.tableWidget.setItem(index, 2, QTableWidgetItem(f"{row["service_description"]}"))
            self.tableWidget.setItem(index, 3, QTableWidgetItem(f"{row["service_price"]}"))

            button = QPushButton("Удалить")
            button.clicked.connect(partial(self.delete_item, row["id"]))
            self.tableWidget.setCellWidget(index, 4, button)

    def delete_item(self, client_id):
        pass
        # EmployeeController.submit_delete(employee_id=employee_id)
        # self.update_table()

    def update_table(self):
        pass
        # self.all_employees_data = EmployeeSerializer.prepare_data_to_print(Employee.all())
        # self.tableWidget.clearContents()
        # self.fill_table()