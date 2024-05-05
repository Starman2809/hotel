from functools import partial

from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QLineEdit, \
    QComboBox, QGridLayout

from db.serializers import (ClientDataSerializer, HotelRoomSerializer, BookingSerializer, PaymentTypeSerializer,
                            EmployeeSerializer, JobPositionSerializer, DepartmentSerializer, WorkScheduleSerializer,
                            RoomTypeSerializer)
from design.button import SimpleButton
from design.calendar import RussianCalendar

from design.style import red_qt_push_button, green_qt_push_button, table_header_style, input_edit_style
from hotel.controller import (ClientController, BookingController, PaymentTypeController, EmployeeController,
                              JobPositionController, DepartmentController, WorkScheduleController, HotelRoomController,
                              RoomTypeController)
from hotel.models import (Client, HotelRoom, Booking, PaymentType, Employee, JobPosition, Department, WorkSchedule,
                          RoomType)


class QTBaseTable(QMainWindow):
    window_title = "Table Example"
    items_to_draw = ["col{1}" for i in range(10)]

    def __init__(self, width, rows=100):
        super().__init__()
        self.columns = len(self.items_to_draw) + 2
        self.setWindowTitle(self.window_title)
        self.setGeometry(100, 100, width, 600)
        self._fill_content(rows)

    def _fill_content(self, rows):
        # Создаем таблицу
        self.tableWidget = self.create_table(rows=rows)

        # Заполняем таблицу данными
        self.fill_table()

        self.set_header_labels()

        # Применяем стили для заголовков таблицы
        header = self.tableWidget.horizontalHeader()
        header.setStyleSheet(table_header_style)

        # Устанавливаем растягивание столбцов по содержимому
        self.tableWidget.resizeColumnsToContents()

        # Создаем вертикальный Layout и добавляем в него таблицу
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)

        # Создаем центральный виджет и устанавливаем в него Layout
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def create_table(self, rows):
        tableWidget = QTableWidget()
        tableWidget.setRowCount(rows)  # Устанавливаем количество строк
        tableWidget.setColumnCount(self.columns)  # Устанавливаем количество столбцов
        return tableWidget

    def set_header_labels(self):
        # Устанавливаем горизонтальные заголовки
        self.tableWidget.setHorizontalHeaderLabels(self.items_to_draw)

    def fill_table(self):
        for row in range(100):
            for col in range(self.columns):
                item = QTableWidgetItem(f"Row {row + 1}, Col {col + 1}")
                self.tableWidget.setItem(row, col, item)

    def update_data(self):
        pass

    def show(self):
        self.update_data()
        super().show()


class QTClientsTable(QTBaseTable):
    width = 1000
    window_title = "Список всех клиентов"
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

            button_edit = QPushButton("Редактировать")
            button_edit.clicked.connect(partial(self.create_edit_form, row["id"]))
            self.tableWidget.setCellWidget(index, 7, button_edit)

            button_delete = QPushButton("Удалить")
            button_delete.clicked.connect(partial(self.delete_client, row["id"]))
            self.tableWidget.setCellWidget(index, 8, button_delete)

    def create_edit_form(self, object_id):
        from design.form import QTClientForm
        self.edit_form = QTClientForm(object_id)
        self.edit_form.show()

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
    items_to_draw = ["id Номера", "ФИО сотрудника", "Дата приезда", "Дата отъезда", "Дата создания бронирования",
                     "Форма оплаты", "Клиент", "Статус оплаты", "Итоговая стоимость"]

    def __init__(self):
        self.all_data = BookingSerializer.prepare_data_to_print(Booking.all())
        self.rows = len(self.all_data)
        super().__init__(width=self.width, rows=self.rows)

    def _fill_content(self, rows):
        self.input_data = {}
        self.line_edit_date = RussianCalendar()
        self.line_edit_date.setFixedSize(400, 300)
        self.toggle_button = QPushButton('Enable/Disable Calendar', self)
        self.toggle_button.clicked.connect(self.toggle_calendar)
        self.use_selected_date = True


        self.line_edit_client = QLineEdit()
        self.line_edit_client.setStyleSheet(input_edit_style)
        self.room_type_combo_box = QComboBox()

        room_type_list = RoomType.all_as_dict()
        self.room_type_combo_box.addItem("", "")
        for item_id, text in room_type_list.items():
            self.room_type_combo_box.addItem(text, item_id)

        self.input_data["date"] = self.line_edit_date
        self.input_data["use_selected_date"] = self.use_selected_date
        self.input_data["client"] = self.line_edit_client
        self.input_data["room_type"] = self.room_type_combo_box

        self.search_button = SimpleButton("Поиск", self.search_booking)

        # Создаем таблицу
        self.tableWidget = self.create_table(rows=rows)

        # Заполняем таблицу данными
        self.fill_table()

        self.set_header_labels()

        # Применяем стили для заголовков таблицы
        header = self.tableWidget.horizontalHeader()
        header.setStyleSheet(table_header_style)

        # Устанавливаем растягивание столбцов по содержимому
        self.tableWidget.resizeColumnsToContents()

        # Создаем вертикальный Layout и добавляем в него таблицу
        layout = QVBoxLayout()
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.line_edit_date, 0, 0)
        grid_layout.addWidget(self.line_edit_client, 0, 1)
        grid_layout.addWidget(self.room_type_combo_box, 0, 2)
        grid_layout.addWidget(self.search_button, 0, 3)
        grid_layout.addWidget(self.toggle_button, 1, 0)

        layout.addLayout(grid_layout)
        layout.addWidget(self.tableWidget)

        # Создаем центральный виджет и устанавливаем в него Layout
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def toggle_calendar(self):
        # Инвертируем текущее состояние enabled у календаря
        self.line_edit_date.setEnabled(not self.line_edit_date.isEnabled())
        if self.input_data["use_selected_date"] is False:
            self.input_data["use_selected_date"] = True
        else:
            self.input_data["use_selected_date"] = False

    def fill_table(self):
        for index, row in enumerate(self.all_data):
            self.tableWidget.setItem(index, 0, QTableWidgetItem(f"{row["room_id"]}"))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(f"{row["employee_full_name"]}"))
            self.tableWidget.setItem(index, 2, QTableWidgetItem(f"{row["date_from"]}"))
            self.tableWidget.setItem(index, 3, QTableWidgetItem(f"{row["date_to"]}"))
            self.tableWidget.setItem(index, 4, QTableWidgetItem(f"{row["creation_date"]}"))
            self.tableWidget.setItem(index, 5, QTableWidgetItem(f"{row["payment_type_description"]}"))
            self.tableWidget.setItem(index, 6, QTableWidgetItem(f"{row["client_full_name"]}"))
            self.tableWidget.setItem(index, 7, QTableWidgetItem(f"{row["payment_status"]}"))
            self.tableWidget.setItem(index, 8, QTableWidgetItem(f"{row["final_price"]}"))

            button_edit = QPushButton("Редактировать")
            button_edit.clicked.connect(partial(self.create_edit_form, row["id"]))
            self.tableWidget.setCellWidget(index, 9, button_edit)

            button = QPushButton("Удалить")
            button.clicked.connect(partial(self.delete_item, row["id"]))
            self.tableWidget.setCellWidget(index, 10, button)

    def create_edit_form(self, booking_id):
        from design.form import QTBookingForm
        self.edit_form = QTBookingForm(booking_id)
        self.edit_form.show()

    def delete_item(self, object_id):
        BookingController.submit_delete(object_id=object_id)
        self.all_data = BookingSerializer.prepare_data_to_print(Booking.all())
        self.update_table()

    def update_table(self):
        self.tableWidget.clearContents()
        self.fill_table()

    def search_booking(self):
        self.all_data = BookingSerializer.prepare_data_to_print(Booking.search_booking(self.input_data))
        self.update_table()


class QTAvailableRoomsTable(QTBaseTable):
    width = 1000
    window_title = "Список доступных комнат"
    items_to_draw = ["id Номера", "Сотрудник", "Категория", "Описание", "Стоимость"]

    def __init__(self, date_from, date_to):
        self.date_from = date_from
        self.date_to = date_to

        self.available_rooms_data = HotelRoomSerializer.prepare_data_to_print(
            HotelRoom.get_available_rooms(date_from, date_to))
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
            button.clicked.connect(partial(self.create_booking_form, self.date_from, self.date_to, row["id"], row["room_type_price"]))
            self.tableWidget.setCellWidget(index, 5, button)

    def create_booking_form(self, date_from, date_to, room_id, room_type_price):
        from design.form import QTBookingForm
        self.booking_form = QTBookingForm(object_id=None, date_from=date_from, date_to=date_to, room_id=room_id, room_type_price=room_type_price)
        self.booking_form.show()


class QTPaymentTypeTable(QTBaseTable):
    width = 1000
    window_title = "Способы оплаты"
    items_to_draw = ["id Оплаты", "Описание оплаты"]

    def __init__(self):
        self.all_data = PaymentTypeSerializer.prepare_data_to_print(PaymentType.all())
        self.rows = len(self.all_data)
        super().__init__(width=self.width, rows=self.rows)

    def fill_table(self):
        for index, row in enumerate(self.all_data):
            self.tableWidget.setItem(index, 0, QTableWidgetItem(f"{row["id"]}"))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(f"{row["description"]}"))

            button_edit = QPushButton("Редактировать")
            button_edit.clicked.connect(partial(self.create_edit_form, row["id"]))
            self.tableWidget.setCellWidget(index, 2, button_edit)

            button = QPushButton("Удалить")
            button.clicked.connect(partial(self.delete_item, row["id"]))
            self.tableWidget.setCellWidget(index, 3, button)

    def create_edit_form(self, object_id):
        from design.form import QTPaymentTypeForm
        self.edit_form = QTPaymentTypeForm(object_id)
        self.edit_form.show()

    def delete_item(self, object_id):
        PaymentTypeController.submit_delete(object_id=object_id)
        self.update_table()

    def update_table(self):
        self.all_data = PaymentTypeSerializer.prepare_data_to_print(PaymentType.all())
        self.tableWidget.clearContents()
        self.fill_table()


class QTEmployeeTable(QTBaseTable):
    width = 1000
    window_title = "Сотрудники"
    items_to_draw = ["Номер", "Фамилия", "Имя", "Отчество", "Дата рождения", "Номер паспорта", "Должность",
                     "Электронная почта", "Номер телефона", "Дата найма", "Зарплата", "Отдел", "График работы",
                     "Статус"]

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

            button_edit = QPushButton("Редактировать")
            button_edit.clicked.connect(partial(self.create_edit_form, row["id"]))
            self.tableWidget.setCellWidget(index, 14, button_edit)

            button = QPushButton("Удалить")
            button.clicked.connect(partial(self.delete_item, row["id"]))
            self.tableWidget.setCellWidget(index, 15, button)

    def create_edit_form(self, object_id):
        from design.form import QTEmployeeForm
        self.edit_form = QTEmployeeForm(object_id)
        self.edit_form.show()

    def delete_item(self, object_id):
        EmployeeController.submit_delete(object_id=object_id)
        self.update_table()

    def update_table(self):
        self.all_data = EmployeeSerializer.prepare_data_to_print(Employee.all())
        self.tableWidget.clearContents()
        self.fill_table()


class QTJobPositionTable(QTBaseTable):
    width = 1000
    window_title = "Должности"
    items_to_draw = ["Номер", "Название"]
    columns = len(items_to_draw) + 1

    def __init__(self):
        self.all_data = JobPositionSerializer.prepare_data_to_print(JobPosition.all())
        self.rows = len(self.all_data)
        super().__init__(width=self.width, rows=self.rows)

    def fill_table(self):
        for index, row in enumerate(self.all_data):
            self.tableWidget.setItem(index, 0, QTableWidgetItem(f"{row["id"]}"))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(f"{row["job_title"]}"))

            button_edit = QPushButton("Редактировать")
            button_edit.clicked.connect(partial(self.create_edit_form, row["id"]))
            self.tableWidget.setCellWidget(index, 2, button_edit)

            button = QPushButton("Удалить")
            button.clicked.connect(partial(self.delete_item, row["id"]))
            self.tableWidget.setCellWidget(index, 3, button)

    def create_edit_form(self, object_id):
        from design.form import QTJobPositionForm
        self.edit_form = QTJobPositionForm(object_id)
        self.edit_form.show()

    def delete_item(self, object_id):
        JobPositionController.submit_delete(object_id=object_id)
        self.update_table()

    def update_table(self):
        self.all_data = JobPositionSerializer.prepare_data_to_print(JobPosition.all())
        self.tableWidget.clearContents()
        self.fill_table()


class QTDepartmentTable(QTBaseTable):
    width = 1000
    window_title = "Отделы"
    items_to_draw = ["Номер", "Название"]

    def __init__(self):
        self.all_data = DepartmentSerializer.prepare_data_to_print(Department.all())
        self.rows = len(self.all_data)
        super().__init__(width=self.width, rows=self.rows)

    def fill_table(self):
        for index, row in enumerate(self.all_data):
            self.tableWidget.setItem(index, 0, QTableWidgetItem(f"{row["id"]}"))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(f"{row["department_title"]}"))

            button_edit = QPushButton("Редактировать")
            button_edit.clicked.connect(partial(self.create_edit_form, row["id"]))
            self.tableWidget.setCellWidget(index, 2, button_edit)

            button = QPushButton("Удалить")
            button.clicked.connect(partial(self.delete_item, row["id"]))
            self.tableWidget.setCellWidget(index, 3, button)

    def create_edit_form(self, object_id):
        from design.form import QTDepartmentForm
        self.edit_form = QTDepartmentForm(object_id)
        self.edit_form.show()

    def delete_item(self, object_id):
        DepartmentController.submit_delete(object_id=object_id)
        self.update_table()

    def update_table(self):
        self.all_data = DepartmentSerializer.prepare_data_to_print(Department.all())
        self.tableWidget.clearContents()
        self.fill_table()


class QTWorkScheduleTable(QTBaseTable):
    width = 1000
    window_title = "График работы"
    items_to_draw = ["Номер", "Название"]
    columns = len(items_to_draw) + 1

    def __init__(self):
        self.all_data = WorkScheduleSerializer.prepare_data_to_print(WorkSchedule.all())
        self.rows = len(self.all_data)
        super().__init__(width=self.width, rows=self.rows)

    def fill_table(self):
        for index, row in enumerate(self.all_data):
            self.tableWidget.setItem(index, 0, QTableWidgetItem(f"{row["id"]}"))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(f"{row["work_schedule_title"]}"))

            button_edit = QPushButton("Редактировать")
            button_edit.clicked.connect(partial(self.create_edit_form, row["id"]))
            self.tableWidget.setCellWidget(index, 2, button_edit)

            button = QPushButton("Удалить")
            button.clicked.connect(partial(self.delete_item, row["id"]))
            self.tableWidget.setCellWidget(index, 3, button)

    def create_edit_form(self, object_id):
        from design.form import QTWorkScheduleForm
        self.edit_form = QTWorkScheduleForm(object_id)
        self.edit_form.show()

    def delete_item(self, object_id):
        WorkScheduleController.submit_delete(object_id=object_id)
        self.update_table()

    def update_table(self):
        self.all_data = WorkScheduleSerializer.prepare_data_to_print(WorkSchedule.all())
        self.tableWidget.clearContents()
        self.fill_table()


class QTHotelRoomTable(QTBaseTable):
    width = 1200
    window_title = "Номера"
    items_to_draw = ["Номер", "ФИО сотрудника", "Тип", "Описание", "Цена", "Активна", "Действие"]

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

            button_edit = QPushButton("Редактировать")
            button_edit.clicked.connect(partial(self.create_edit_form, row["id"]))
            self.tableWidget.setCellWidget(index, 7, button_edit)

            button_delete = QPushButton("Удалить")
            button_delete.clicked.connect(partial(self.delete_item, row["id"]))
            self.tableWidget.setCellWidget(index, 8, button_delete)

    def create_edit_form(self, object_id):
        from design.form import QTHotelRoomForm
        self.edit_form = QTHotelRoomForm(object_id)
        self.edit_form.show()

    def delete_item(self, object_id):
        HotelRoomController.submit_delete(object_id=object_id)
        self.update_table()

    def activate_hotel_room(self, object_id):
        HotelRoom.activate(object_id)
        self.update_table()

    def deactivate_hotel_room(self, object_id):
        HotelRoom.deactivate(object_id)
        self.update_table()

    def update_table(self):
        self.all_data = HotelRoomSerializer.prepare_data_to_print(HotelRoom.all())
        self.tableWidget.clearContents()
        self.fill_table()


class QTRoomTypeTable(QTBaseTable):
    width = 1000
    window_title = "Типы номеров"
    items_to_draw = ["Номер", "Название", "Описание", "Стоимость"]

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

            button_edit = QPushButton("Редактировать")
            button_edit.clicked.connect(partial(self.create_edit_form, row["id"]))
            self.tableWidget.setCellWidget(index, 4, button_edit)

            button = QPushButton("Удалить")
            button.clicked.connect(partial(self.delete_item, row["id"]))
            self.tableWidget.setCellWidget(index, 5, button)

    def create_edit_form(self, object_id):
        from design.form import QTRoomTypeForm
        self.edit_form = QTRoomTypeForm(object_id)
        self.edit_form.show()

    def delete_item(self, object_id):
        RoomTypeController.submit_delete(object_id=object_id)
        self.update_table()

    def update_table(self):
        self.all_data = RoomTypeSerializer.prepare_data_to_print(RoomType.all())
        self.tableWidget.clearContents()
        self.fill_table()
