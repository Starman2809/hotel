import tkinter
from tkinter import Button
from functools import partial

from hotel.models import Client, Employee, HotelRoom
from db.serializers import ClientDataSerializer, EmployeeSerializer, HotelRoomSerializer


class Table(tkinter.Canvas):
    def __init__(self, parent, rows=10, columns=3, cell_width=100, cell_height=30, **kwargs):
        super().__init__(parent, **kwargs)
        self.rows = rows
        self.columns = columns
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.cells = {}
        self.draw_grid()

    def draw_grid(self):
        for row in range(self.rows + 1):
            self.create_line(0, row * self.cell_height, self.columns * self.cell_width, row * self.cell_height)
        for col in range(self.columns + 1):
            self.create_line(col * self.cell_width, 0, col * self.cell_width, self.rows * self.cell_height)

    def set_cell(self, row, col, value):
        x0 = col * self.cell_width
        y0 = row * self.cell_height
        x1 = x0 + self.cell_width
        y1 = y0 + self.cell_height
        cell_id = self.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=value)
        self.cells[(row, col)] = cell_id

    def set_button_cell(self, row, col, button: Button):
        x0 = col * self.cell_width
        y0 = row * self.cell_height
        x1 = x0 + self.cell_width
        y1 = y0 + self.cell_height
        button.place(x=(x0 + x1) / 2, y=(y0 + y1) / 2, anchor="center")

    def draw_all(self):
        pass

    def redraw(self):
        # Удаляем все объекты на Canvas
        self.delete("all")
        # Рисуем сетку заново
        self.draw_grid()
        # Обновляем данные внутри обьекта
        self.update_data()
        # Ваш код для рисования объектов заново
        self.draw_all()

    def update_data(self):
        pass


class ClientsTable(Table):
    def __init__(self, parent, columns=3, cell_width=100, cell_height=30, **kwargs):
        self.parent = parent
        self.all_clients_data = ClientDataSerializer.prepare_data_to_print(Client.all())
        self.rows = len(self.all_clients_data)
        super().__init__(parent, self.rows, columns, cell_width, cell_height, **kwargs)

    def update_data(self):
        self.all_clients_data = ClientDataSerializer.prepare_data_to_print(Client.all())

    def draw_all(self):
        self.pack(fill="both", expand=True)

        self.set_cell(0, 0, "Номер")
        self.set_cell(0, 1, "Фамилия")
        self.set_cell(0, 2, "Имя")
        self.set_cell(0, 3, "Отчество")
        self.set_cell(0, 4, "Дата рождения")
        self.set_cell(0, 5, "Электронная почта")
        self.set_cell(0, 6, "Номер телефона")
        self.set_cell(0, 7, "Номер паспорта")
        self.set_cell(0, 8, "")

        for index, client in enumerate(self.all_clients_data):
            self.set_cell(index + 1, 0, client['id'])
            self.set_cell(index + 1, 1, client['last_name'])
            self.set_cell(index + 1, 2, client['first_name'])
            self.set_cell(index + 1, 3, client['patronymic'])
            self.set_cell(index + 1, 4, client['birthday_date'])
            self.set_cell(index + 1, 5, client['email'])
            self.set_cell(index + 1, 6, client['phone_number'])
            self.set_cell(index + 1, 7, client['passport_number'])

            button = tkinter.Button(self.parent, text="Удалить", command=partial(self.delete_client, client["id"]))
            self.set_button_cell(index + 1, 8, button)

    def delete_client(self, client_id: int):
        Client.delete_client(client_id)
        self.redraw()


class EmployeesTable(Table):
    def __init__(self, parent, columns=3, cell_width=50, cell_height=30, **kwargs):
        self.parent = parent
        self.all_employees_data = EmployeeSerializer.prepare_data_to_print(Employee.all())
        self.rows = len(self.all_employees_data)
        super().__init__(parent, self.rows, columns, cell_width, cell_height, **kwargs)

    def update_data(self):
        self.all_employees_data = EmployeeSerializer.prepare_data_to_print(Employee.all())

    def draw_all(self):
        self.pack(fill="both", expand=True)

        self.set_cell(0, 0, "Номер")
        self.set_cell(0, 1, "Фамилия")
        self.set_cell(0, 2, "Имя")
        self.set_cell(0, 3, "Отчество")
        self.set_cell(0, 4, "Дата рождения")
        self.set_cell(0, 5, "Номер паспорта")
        self.set_cell(0, 6, "Должность")
        self.set_cell(0, 7, "Электронная почта")
        self.set_cell(0, 8, "Номер телефона")
        self.set_cell(0, 9, "Дата найма")
        self.set_cell(0, 10, "Зарплата")
        self.set_cell(0, 11, "Отдел")
        self.set_cell(0, 12, "График работы")
        self.set_cell(0, 13, "Статус")
        self.set_cell(0, 14, "")

        for index, employee in enumerate(self.all_employees_data):
            self.set_cell(index + 1, 0, employee['id'])
            self.set_cell(index + 1, 1, employee['last_name'])
            self.set_cell(index + 1, 2, employee['first_name'])
            self.set_cell(index + 1, 3, employee['patronymic'])
            self.set_cell(index + 1, 4, employee['birthday_date'])
            self.set_cell(index + 1, 5, employee['passport_number'])
            self.set_cell(index + 1, 6, employee['job_type'])
            self.set_cell(index + 1, 7, employee['email'])
            self.set_cell(index + 1, 8, employee['phone_number'])
            self.set_cell(index + 1, 9, employee['hiring_date'])
            self.set_cell(index + 1, 10, employee['salary'])
            self.set_cell(index + 1, 11, employee['department'])
            self.set_cell(index + 1, 12, employee['work_schedule'])
            self.set_cell(index + 1, 13, employee['work_status'])

            button = tkinter.Button(self.parent, text="Удалить", command=partial(self.delete_employee, employee["id"]))
            self.set_button_cell(index + 1, 14, button)

    def delete_employee(self, employee_id: int):
        Employee.delete(employee_id)
        self.redraw()


class HotelRoomTable(Table):
    def __init__(self, parent, columns=7, cell_width=100, cell_height=30, **kwargs):
        self.parent = parent
        self.all_hotel_rooms_data = HotelRoomSerializer.prepare_data_to_print(HotelRoom.all())
        self.rows = len(self.all_hotel_rooms_data)
        super().__init__(parent, self.rows, columns, cell_width, cell_height, **kwargs)

    def update_data(self):
        self.all_hotel_rooms_data = HotelRoomSerializer.prepare_data_to_print(HotelRoom.all())

    def draw_all(self):
        self.pack(fill="both", expand=True)

        self.set_cell(0, 0, "Номер")
        self.set_cell(0, 1, "ФИО сотрудника")
        self.set_cell(0, 2, "Тип")
        self.set_cell(0, 3, "Описание")
        self.set_cell(0, 4, "Цена")
        self.set_cell(0, 5, "Активна")
        self.set_cell(0, 6, "")

        for index, hotel_room in enumerate(self.all_hotel_rooms_data):
            self.set_cell(index + 1, 0, hotel_room['id'])
            self.set_cell(index + 1, 1, hotel_room['employee_full_name'])
            self.set_cell(index + 1, 2, hotel_room['room_type_name'])
            self.set_cell(index + 1, 3, hotel_room['room_type_description'])
            self.set_cell(index + 1, 4, hotel_room['room_type_price'])
            self.set_cell(index + 1, 5, hotel_room['active'])

            if hotel_room['active'] == "Да":
                button = tkinter.Button(self.parent, text="Деактивировать", command=partial(self.deactivate_hotel_room, hotel_room["id"]))
            else:
                button = tkinter.Button(self.parent, text="Активировать", command=partial(self.activate_hotel_room, hotel_room["id"]))

            self.set_button_cell(index + 1, 6, button)

    def deactivate_hotel_room(self, room_id: int):
        HotelRoom.deactivate(room_id)
        self.redraw()

    def activate_hotel_room(self, room_id: int):
        HotelRoom.activate(room_id)
        self.redraw()
