import tkinter
from abc import abstractmethod
from functools import partial
from tkinter import ttk
from typing import Dict

from tkcalendar import Calendar

from hotel.models import Client, JobPosition, Department, WorkSchedule, Employee, RoomType, AdditionalServiceType
from db.serializers import ClientDataSerializer, EmployeeSerializer, AdditionalServiceSerializer, JobPositionSerializer, \
    DepartmentSerializer, RoomTypeSerializer, WorkScheduleSerializer
from design_objects.table import ClientsTable, EmployeesTable, HotelRoomTable, AdditionalServiceTable, JobPositionTable, \
    DepartmentTable, RoomTypeTable, WorkScheduleTable
from hotel.controller import EmployeeController, ClientController, HotelRoomController, AdditionalServiceController, \
    Controller, JobPositionController, DepartmentController, RoomTypeController, WorkScheduleController


class Renderer:
    create_window_title = "empty title"
    create_window_size = "800x600"
    submit_create_button_position_row = 3

    list_all_window_title = ""
    list_all_window_size = "1800x600"

    update_window_title = ""
    update_window_size = "800x600"
    submit_update_button_position_row = 3

    form_items_to_draw = {
        "department_title_entry": "Название:",
    }

    def __init__(self):
        self.controller = self.set_controller()

    @abstractmethod
    def set_controller(self):
        """
        Method for set controller for all children
        :return:
        """
        pass

    def draw_window_create(self):
        root = tkinter.Tk()
        root.title(f"{self.create_window_title}")
        root.geometry(f"{self.create_window_size}")

        self.draw_create_object_form(root)

        submit_button = tkinter.Button(
            root, text="Отправить", command=self.controller.submit_create
        )
        submit_button.grid(row=self.submit_create_button_position_row, columnspan=7, padx=5, pady=5)

        root.mainloop()

    @abstractmethod
    def draw_create_object_form(self, root: tkinter.Tk):
        pass

    def draw_window_read_delete(self):
        self.controller.root = tkinter.Tk()
        root = self.controller.root
        root.title(self.list_all_window_title)
        root.geometry(self.list_all_window_size)
        self.list_all_objects_grid(root)
        root.mainloop()

    @abstractmethod
    def list_all_objects_grid(self, root: tkinter.Tk):
        pass

    def draw_window_update(self, object_id: int):
        root = tkinter.Tk()
        root.title(self.update_window_title)
        root.geometry(self.update_window_size)
        self.update_object_input_grid(root, object_id)
        submit_button = tkinter.Button(
            root, text="Отправить", command=partial(self.controller.submit_update, object_id)
        )
        submit_button.grid(row=self.submit_update_button_position_row, columnspan=7, padx=5, pady=5)
        root.mainloop()

    @abstractmethod
    def update_object_input_grid(self, root: tkinter.Tk, object_id: int):
        pass


class ClientRenderer:
    def __init__(self):
        self.controller = ClientController()

    def create_new_client_window(self):
        root = tkinter.Tk()
        root.title("Создание нового клиента")
        root.geometry("800x600")

        self.__create_new_client_input_grid(root)

        submit_button = tkinter.Button(
            root, text="Отправить", command=self.controller.submit_create
        )
        submit_button.grid(row=7, columnspan=7, padx=5, pady=5)

        root.mainloop()

    def read_all_clients_window(self):
        self.controller.root = tkinter.Tk()
        root = self.controller.root
        root.title("Список всех клиентов")
        root.geometry("1800x600")

        self.__display_all_clients_grid(root)

        root.mainloop()

    def draw_update_client_window(self, client_id):
        root = tkinter.Tk()
        root.title("Создание нового клиента")
        root.geometry("800x600")

        self.__update_new_client_input_grid(root, client_id)

        submit_button = tkinter.Button(
            root, text="Отправить", command=partial(self.controller.submit_update, client_id)
        )
        submit_button.grid(row=7, columnspan=7, padx=5, pady=5)

        root.mainloop()

    def draw_create_client_form(self, root, items_to_draw: Dict):
        for index, (field_name, label_name) in enumerate(items_to_draw.items()):
            tkinter.Label(root, text=label_name).grid(row=index, column=0, padx=5, pady=5)

            if "calendar" in field_name:
                self.controller.entries[field_name] = Calendar(root, selectmode="day", date_pattern="dd.MM.yyyy")
            else:
                self.controller.entries[field_name] = tkinter.Entry(root)

            self.controller.entries[field_name].grid(row=index, column=1, padx=5, pady=5)

    def draw_update_client_form(self, root, items_to_draw: Dict, client):

        for index, (field_name, label_name) in enumerate(items_to_draw.items()):
            tkinter.Label(root, text=label_name).grid(row=index, column=0, padx=5, pady=5)

            if "first_name_entry" in field_name:
                self.controller.entries[field_name] = tkinter.Entry(root)
                self.controller.entries[field_name].insert(0, client["first_name"])
            elif "last_name_entry" in field_name:
                self.controller.entries[field_name] = tkinter.Entry(root)
                self.controller.entries[field_name].insert(0, client["last_name"])
            elif "patronymic_entry" in field_name:
                self.controller.entries[field_name] = tkinter.Entry(root)
                self.controller.entries[field_name].insert(0, client["patronymic"])
            elif "birthday_date_calendar" in field_name:
                self.controller.entries[field_name] = Calendar(root, selectmode="day", date_pattern="dd.MM.yyyy", day=client["birthday_date"].day, month=client["birthday_date"].month, year=client["birthday_date"].year)
            elif "email_entry" in field_name:
                self.controller.entries[field_name] = tkinter.Entry(root)
                self.controller.entries[field_name].insert(0, client["email"])
            elif "phone_number_entry" in field_name:
                self.controller.entries[field_name] = tkinter.Entry(root)
                self.controller.entries[field_name].insert(0, client["phone_number"])
            elif "passport_number_entry" in field_name:
                self.controller.entries[field_name] = tkinter.Entry(root)
                self.controller.entries[field_name].insert(0, client["passport_number"])

            self.controller.entries[field_name].grid(row=index, column=1, padx=5, pady=5)

    def __create_new_client_input_grid(self, root):
        items_to_draw = {
            "first_name_entry": "Фамилия:",
            "last_name_entry": "Имя:",
            "patronymic_entry": "Отчество:",
            "birthday_date_calendar": "Дата рождения:",
            "email_entry": "Электронная почта:",
            "phone_number_entry": "Номер телефона:",
            "passport_number_entry": "Номер паспорта:",
        }
        self.draw_create_client_form(root, items_to_draw)

    def __update_new_client_input_grid(self, root, client_id: int):

        client = ClientDataSerializer.prepare_data_to_print([Client.get(client_id)])[0]
        items_to_draw = {
            "first_name_entry": "Фамилия:",
            "last_name_entry": "Имя:",
            "patronymic_entry": "Отчество:",
            "birthday_date_calendar": "Дата рождения:",
            "email_entry": "Электронная почта:",
            "phone_number_entry": "Номер телефона:",
            "passport_number_entry": "Номер паспорта:",
        }
        self.draw_update_client_form(root, items_to_draw, client)

    def __display_all_clients_grid(self, root):
        all_clients_table = ClientsTable(root, columns=9, cell_width=200, cell_height=30)
        all_clients_table.draw_all()


class EmployeeRenderer:
    def __init__(self):
        self.controller = EmployeeController()

    def draw_create_new_employee_window(self):
        root = tkinter.Tk()
        root.title("Создание нового сотрудника")
        root.geometry("1000x800")

        self.__create_new_employee_input_grid(root)

        submit_button = tkinter.Button(
            root, text="Отправить", command=self.controller.submit_create
        )
        submit_button.grid(row=14, columnspan=7, padx=5, pady=5)

        root.mainloop()

    def __create_new_employee_input_grid(self, root: tkinter.Tk):
        items_to_draw = {
            "first_name_entry": "Фамилия:",
            "last_name_entry": "Имя:",
            "patronymic_entry": "Отчество:",
            "birthday_date_calendar": "Дата рождения:",
            "passport_number_entry": "Номер паспорта:",
            "email_entry": "Электронная почта:",
            "phone_number_entry": "Номер телефона:",
            "job_position_combobox": "Должность:",
            "hiring_date_calendar": "Дата найма:",
            "salary_entry": "Зарплата:",
            "department_combobox": "Отдел:",
            "work_schedule_combobox": "График работы:",
            "work_status_entry": "Статус:",
        }
        self.draw_create_employee_form(root, items_to_draw)

    def __update_employee_input_grid(self, root: tkinter.Tk, employee_id: int):
        employee_dict = EmployeeSerializer.prepare_data_to_print([Employee.get(employee_id)])[0]

        items_to_draw = {
            "first_name_entry": "Фамилия:",
            "last_name_entry": "Имя:",
            "patronymic_entry": "Отчество:",
            "birthday_date_calendar": "Дата рождения:",
            "passport_number_entry": "Номер паспорта:",
            "email_entry": "Электронная почта:",
            "phone_number_entry": "Номер телефона:",
            "job_position_combobox": "Должность:",
            "hiring_date_calendar": "Дата найма:",
            "salary_entry": "Зарплата:",
            "department_combobox": "Отдел:",
            "work_schedule_combobox": "График работы:",
            "work_status_entry": "Статус:",
        }
        self.draw_update_employee_form(root, items_to_draw, employee_dict)

    def draw_create_employee_form(self, root: tkinter.Tk, items_to_draw: Dict):

        self.controller.entries["job_position_list"] = JobPosition.all_as_dict()
        self.controller.entries["department_list"] = Department.all_as_dict()
        self.controller.entries["work_schedule_list"] = WorkSchedule.all_as_dict()

        for index, (field_name, label_name) in enumerate(items_to_draw.items()):
            tkinter.Label(root, text=label_name).grid(row=index, column=0, padx=5, pady=5)

            if "calendar" in field_name:
                self.controller.entries[field_name] = Calendar(root, selectmode="day", date_pattern="dd.MM.yyyy")
            elif "job_position_combobox" in field_name:
                self.controller.entries["job_position_combobox_selected_text"] = tkinter.StringVar()
                self.controller.entries[field_name] = ttk.Combobox(root, textvariable=self.controller.entries["job_position_combobox_selected_text"])
                self.controller.entries[field_name]['values'] = list(self.controller.entries["job_position_list"].values())
            elif "department_combobox" in field_name:
                self.controller.entries["department_type_combobox_selected_text"] = tkinter.StringVar()
                self.controller.entries[field_name] = ttk.Combobox(root, textvariable=self.controller.entries["department_type_combobox_selected_text"])
                self.controller.entries[field_name]['values'] = list(self.controller.entries["department_list"].values())
            elif "work_schedule_combobox" in field_name:
                self.controller.entries["work_schedule_combobox_selected_text"] = tkinter.StringVar()
                self.controller.entries[field_name] = ttk.Combobox(root, textvariable=self.controller.entries["work_schedule_combobox_selected_text"])
                self.controller.entries[field_name]['values'] = list(self.controller.entries["work_schedule_list"].values())

            else:
                self.controller.entries[field_name] = tkinter.Entry(root)

            # Отрисовка списка
            self.controller.entries[field_name].grid(row=index, column=1, padx=5, pady=5)

    def draw_update_employee_form(self, root: tkinter.Tk, items_to_draw: Dict, employee: Dict):

        self.controller.entries["job_position_list"] = JobPosition.all_as_dict()
        self.controller.entries["department_list"] = Department.all_as_dict()
        self.controller.entries["work_schedule_list"] = WorkSchedule.all_as_dict()

        for index, (field_name, label_name) in enumerate(items_to_draw.items()):
            tkinter.Label(root, text=label_name).grid(row=index, column=0, padx=5, pady=5)

            if "first_name_entry" in field_name:
                self.controller.entries[field_name] = tkinter.Entry(root)
                self.controller.entries[field_name].insert(0, employee["first_name"])
            elif "last_name_entry" in field_name:
                self.controller.entries[field_name] = tkinter.Entry(root)
                self.controller.entries[field_name].insert(0, employee["last_name"])
            elif "patronymic_entry" in field_name:
                self.controller.entries[field_name] = tkinter.Entry(root)
                self.controller.entries[field_name].insert(0, employee["patronymic"])
            elif "birthday_date_calendar" in field_name:
                self.controller.entries[field_name] = Calendar(root, selectmode="day", date_pattern="dd.MM.yyyy", day=employee["birthday_date"].day, month=employee["birthday_date"].month, year=employee["birthday_date"].year)
            elif "passport_number_entry" in field_name:
                self.controller.entries[field_name] = tkinter.Entry(root)
                self.controller.entries[field_name].insert(0, employee["passport_number"])
            elif "job_position_combobox" in field_name:
                self.controller.entries["job_position_combobox_selected_text"] = tkinter.StringVar()
                self.controller.entries[field_name] = ttk.Combobox(root, textvariable=self.controller.entries["job_position_combobox_selected_text"])
                self.controller.entries[field_name]['values'] = list(self.controller.entries["job_position_list"].values())
            elif "email_entry" in field_name:
                self.controller.entries[field_name] = tkinter.Entry(root)
                self.controller.entries[field_name].insert(0, employee["email"])
            elif "phone_number_entry" in field_name:
                self.controller.entries[field_name] = tkinter.Entry(root)
                self.controller.entries[field_name].insert(0, employee["phone_number"])
            elif "hiring_date_calendar" in field_name:
                self.controller.entries[field_name] = Calendar(root, selectmode="day", date_pattern="dd.MM.yyyy", day=employee["hiring_date"].day, month=employee["hiring_date"].month, year=employee["hiring_date"].year)
            elif "salary_entry" in field_name:
                self.controller.entries[field_name] = tkinter.Entry(root)
                self.controller.entries[field_name].insert(0, employee["salary"])
            elif "department_combobox" in field_name:
                self.controller.entries["department_type_combobox_selected_text"] = tkinter.StringVar()
                self.controller.entries[field_name] = ttk.Combobox(root, textvariable=self.controller.entries["department_type_combobox_selected_text"])
                self.controller.entries[field_name]['values'] = list(self.controller.entries["department_list"].values())
            elif "work_schedule_combobox" in field_name:
                self.controller.entries["work_schedule_combobox_selected_text"] = tkinter.StringVar()
                self.controller.entries[field_name] = ttk.Combobox(root, textvariable=self.controller.entries["work_schedule_combobox_selected_text"])
                self.controller.entries[field_name]['values'] = list(self.controller.entries["work_schedule_list"].values())
            elif "work_status_entry" in field_name:
                self.controller.entries[field_name] = tkinter.Entry(root)
                self.controller.entries[field_name].insert(0, employee["work_status"])


            # Отрисовка списка
            self.controller.entries[field_name].grid(row=index, column=1, padx=5, pady=5)

    def draw_read_all_employees_window(self):
        self.controller.root = tkinter.Tk()
        root = self.controller.root
        root.title("Список персонала")
        root.geometry("1800x600")

        self.__display_all_employees_grid(root)

        root.mainloop()

    def __display_all_employees_grid(self, root):
        all_clients_table = EmployeesTable(root, columns=14, cell_width=120, cell_height=30)
        all_clients_table.draw_all()

    def draw_update_employee_window(self, employee_id):
        root = tkinter.Tk()
        root.title("Изменение данных сотрудника")
        root.geometry("1000x800")

        self.__update_employee_input_grid(root, employee_id)

        submit_button = tkinter.Button(
            root, text="Отправить", command=partial(self.controller.submit_update, employee_id)
        )
        submit_button.grid(row=14, columnspan=7, padx=5, pady=5)

        root.mainloop()


class HotelRoomRenderer:
    def __init__(self):
        self.controller = HotelRoomController()

    def draw_create_new_room_window(self):
        root = tkinter.Tk()
        root.title("Создание нового номера")
        root.geometry("800x600")

        self.__create_new_room_input_grid(root)

        submit_button = tkinter.Button(
            root, text="Отправить", command=self.controller.submit_create
        )
        submit_button.grid(row=3, columnspan=7, padx=5, pady=5)

        root.mainloop()

    def __create_new_room_input_grid(self, root):
        items_to_draw = {
            "employee_combobox": "Сотрудник:",
            "room_type_combobox": "Категория номера:",
        }
        self.draw_create_room_form(root, items_to_draw)

    def draw_create_room_form(self, root, items_to_draw):
        self.controller.entries["employee_list"] = Employee.all_as_dict()
        self.controller.entries["room_type_list"] = RoomType.all_as_dict()

        for index, (field_name, label_name) in enumerate(items_to_draw.items()):
            tkinter.Label(root, text=label_name).grid(row=index, column=0, padx=5, pady=5)

            if "employee_combobox" in field_name:
                self.controller.entries["employee_combobox_selected_text"] = tkinter.StringVar()
                self.controller.entries[field_name] = ttk.Combobox(root, textvariable=self.controller.entries["employee_combobox_selected_text"])
                self.controller.entries[field_name]['values'] = list(self.controller.entries["employee_list"].values())
            elif "room_type_combobox" in field_name:
                self.controller.entries["room_type_combobox_selected_text"] = tkinter.StringVar()
                self.controller.entries[field_name] = ttk.Combobox(root, textvariable=self.controller.entries["room_type_combobox_selected_text"])
                self.controller.entries[field_name]['values'] = list(self.controller.entries["room_type_list"].values())

            # Отрисовка списка
            self.controller.entries[field_name].grid(row=index, column=1, padx=5, pady=5)

    def draw_list_and_deactivate_hotel_rooms_window(self):
        self.controller.root = tkinter.Tk()
        root = self.controller.root
        root.title("Список номеров")
        root.geometry("1800x600")

        self.__display_all_hotel_rooms_grid(root)

        root.mainloop()

    def __display_all_hotel_rooms_grid(self, root):
        all_hotel_rooms_table = HotelRoomTable(root, columns=7, cell_width=265, cell_height=65)
        all_hotel_rooms_table.draw_all()

    def draw_update_hotel_room_window(self, room_id):
        root = tkinter.Tk()
        root.title("Изменение данных сотрудника")
        root.geometry("1000x800")

        self.__update_hotel_room_input_grid(root, room_id)

        submit_button = tkinter.Button(
            root, text="Отправить", command=partial(self.controller.submit_update, room_id)
        )
        submit_button.grid(row=14, columnspan=7, padx=5, pady=5)

        root.mainloop()

    def __update_hotel_room_input_grid(self, root: tkinter.Tk, room_id: int):
        # TODO: добавить значения по умолчанию для формы
        # hotel_room_dict = HotelRoomSerializer.prepare_data_to_print([HotelRoom.get(room_id)])[0]
        items_to_draw = {
            "employee_combobox": "Сотрудник:",
            "room_type_combobox": "Категория номера:",
        }
        self.draw_update_hotel_room_form(root, items_to_draw)

    def draw_update_hotel_room_form(self, root: tkinter.Tk, items_to_draw: Dict):

        # TODO: Добавить значения по умолчанию для combobox из hotel_room_dict

        self.controller.entries["employee_list"] = Employee.all_as_dict()
        self.controller.entries["room_type_list"] = RoomType.all_as_dict()

        for index, (field_name, label_name) in enumerate(items_to_draw.items()):
            tkinter.Label(root, text=label_name).grid(row=index, column=0, padx=5, pady=5)

            if "employee_combobox" in field_name:
                self.controller.entries["employee_combobox_selected_text"] = tkinter.StringVar()
                self.controller.entries[field_name] = ttk.Combobox(root, textvariable=self.controller.entries["employee_combobox_selected_text"])
                self.controller.entries[field_name]['values'] = list(self.controller.entries["employee_list"].values())
            elif "room_type_combobox" in field_name:
                self.controller.entries["room_type_combobox_selected_text"] = tkinter.StringVar()
                self.controller.entries[field_name] = ttk.Combobox(root, textvariable=self.controller.entries["room_type_combobox_selected_text"])
                self.controller.entries[field_name]['values'] = list(self.controller.entries["room_type_list"].values())

            # Отрисовка списка
            self.controller.entries[field_name].grid(row=index, column=1, padx=5, pady=5)


class AdditionalServiceRenderer:
    def __init__(self):
        self.controller = AdditionalServiceController()

    def draw_create_new_service_window(self):
        root = tkinter.Tk()
        root.title("Создание новой услуги")
        root.geometry("800x600")

        self.__create_new_service_input_grid(root)

        submit_button = tkinter.Button(
            root, text="Отправить", command=self.controller.submit_create
        )
        submit_button.grid(row=3, columnspan=7, padx=5, pady=5)

        root.mainloop()

    def __create_new_service_input_grid(self, root):
        items_to_draw = {
            "service_name_entry": "Название:",
            "service_description_entry": "Описание:",
            "service_price_entry": "Стоимость:",
        }
        self.draw_create_service_form(root, items_to_draw)

    def draw_create_service_form(self, root: tkinter.Tk, items_to_draw: Dict):
        for index, (field_name, label_name) in enumerate(items_to_draw.items()):
            tkinter.Label(root, text=label_name).grid(row=index, column=0, padx=5, pady=5)
            self.controller.entries[field_name] = tkinter.Entry(root)
            # Отрисовка списка
            self.controller.entries[field_name].grid(row=index, column=1, padx=5, pady=5)

    def draw_list_and_delete_service_window(self):
        self.controller.root = tkinter.Tk()
        root = self.controller.root
        root.title("Список дополнительных услуг")
        root.geometry("1800x800")

        self.__display_all_services_grid(root)

        root.mainloop()

    def __display_all_services_grid(self, root):
        all_hotel_rooms_table = AdditionalServiceTable(root, columns=5, cell_width=265, cell_height=85)
        all_hotel_rooms_table.draw_all()

    def draw_update_service_window(self, service_id):
        root = tkinter.Tk()
        root.title("Редактирование услуги")
        root.geometry("800x600")

        self.__update_service_input_grid(root, service_id)

        submit_button = tkinter.Button(
            root, text="Отправить", command=partial(self.controller.submit_update, service_id)
        )
        submit_button.grid(row=3, columnspan=7, padx=5, pady=5)

        root.mainloop()

    def __update_service_input_grid(self, root, service_id: int):

        service = AdditionalServiceSerializer.prepare_data_to_print([AdditionalServiceType.get(service_id)])[0]
        items_to_draw = {
            "service_name_entry": "Название:",
            "service_description_entry": "Описание:",
            "service_price_entry": "Стоимость:",
        }
        self.draw_update_service_form(root, items_to_draw, service)

    def draw_update_service_form(self, root, items_to_draw: Dict, service):

        for index, (field_name, label_name) in enumerate(items_to_draw.items()):
            tkinter.Label(root, text=label_name).grid(row=index, column=0, padx=5, pady=5)

            if "service_name_entry" in field_name:
                self.controller.entries[field_name] = tkinter.Entry(root)
                self.controller.entries[field_name].insert(0, service["service_name"])
            elif "service_description_entry" in field_name:
                self.controller.entries[field_name] = tkinter.Entry(root)
                self.controller.entries[field_name].insert(0, service["service_description"])
            elif "service_price_entry" in field_name:
                self.controller.entries[field_name] = tkinter.Entry(root)
                self.controller.entries[field_name].insert(0, service["service_price"])

            self.controller.entries[field_name].grid(row=index, column=1, padx=5, pady=5)


class JobPositionRenderer(Renderer):
    create_window_title = "Создание новой должности"
    create_window_size = "800x600"
    submit_create_button_position_row = 3

    list_all_window_title = "Список всех должностей"
    list_all_window_size = "1800x600"

    update_window_title = "Редактирование должности"
    update_window_size = "800x600"
    submit_update_button_position_row = 3

    form_items_to_draw = {
        "job_title_entry": "Название:",
    }

    def set_controller(self):
        return JobPositionController()

    def draw_create_object_form(self, root: tkinter.Tk):
        for index, (field_name, label_name) in enumerate(self.form_items_to_draw.items()):
            tkinter.Label(root, text=label_name).grid(row=index, column=0, padx=5, pady=5)
            self.controller.entries[field_name] = tkinter.Entry(root)
            # Отрисовка списка
            self.controller.entries[field_name].grid(row=index, column=1, padx=5, pady=5)

    def list_all_objects_grid(self, root: tkinter.Tk):
        all_clients_table = JobPositionTable(root, columns=3, cell_width=200, cell_height=30)
        all_clients_table.draw_all()

    def update_object_input_grid(self, root: tkinter.Tk, job_position_id: int):
        job_positions = JobPositionSerializer.prepare_data_to_print([JobPosition.get(job_position_id)])[0]
        self.draw_update_job_position_form(root, job_positions)

    def draw_update_job_position_form(self, root, job_positions):
        for index, (field_name, label_name) in enumerate(self.form_items_to_draw.items()):
            tkinter.Label(root, text=label_name).grid(row=index, column=0, padx=5, pady=5)
            if "job_title_entry" in field_name:
                self.controller.entries[field_name] = tkinter.Entry(root)
                self.controller.entries[field_name].insert(0, job_positions["job_title"])
            self.controller.entries[field_name].grid(row=index, column=1, padx=5, pady=5)


class DepartmentRenderer(Renderer):
    create_window_title = "Создание нового отдела"
    create_window_size = "800x600"
    submit_create_button_position_row = 3

    list_all_window_title = "Список всех отделов"
    list_all_window_size = "1800x600"

    update_window_title = "Редактирование отдела"
    update_window_size = "800x600"
    submit_update_button_position_row = 3

    form_items_to_draw = {
        "department_title_entry": "Название:",
    }

    def set_controller(self):
        return DepartmentController()

    def draw_create_object_form(self, root: tkinter.Tk):
        for index, (field_name, label_name) in enumerate(self.form_items_to_draw.items()):
            tkinter.Label(root, text=label_name).grid(row=index, column=0, padx=5, pady=5)
            self.controller.entries[field_name] = tkinter.Entry(root)
            # Отрисовка списка
            self.controller.entries[field_name].grid(row=index, column=1, padx=5, pady=5)

    def list_all_objects_grid(self, root: tkinter.Tk):
        all_departments_table = DepartmentTable(root, columns=3, cell_width=200, cell_height=30)
        all_departments_table.draw_all()

    def update_object_input_grid(self, root: tkinter.Tk, department_id: int):
        department = DepartmentSerializer.prepare_data_to_print([Department.get(department_id)])[0]
        self.draw_update_department_form(root, department)

    def draw_update_department_form(self, root, department):
        for index, (field_name, label_name) in enumerate(self.form_items_to_draw.items()):
            tkinter.Label(root, text=label_name).grid(row=index, column=0, padx=5, pady=5)
            if "department_title_entry" in field_name:
                self.controller.entries[field_name] = tkinter.Entry(root)
                self.controller.entries[field_name].insert(0, department["department_title"])
            self.controller.entries[field_name].grid(row=index, column=1, padx=5, pady=5)


class RoomTypeRenderer(Renderer):
    create_window_title = "Создание нового типа номера"
    create_window_size = "800x600"
    submit_create_button_position_row = 3

    list_all_window_title = "Список всех типов номеров"
    list_all_window_size = "1800x600"

    update_window_title = "Редактирование типа номера"
    update_window_size = "800x600"
    submit_update_button_position_row = 3

    form_items_to_draw = {
        "room_type_title_entry": "Название:",
        "room_type_description_entry": "Описание:",
        "room_type_price_entry": "Стоимость:",
    }

    def set_controller(self):
        return RoomTypeController()

    def draw_create_object_form(self, root: tkinter.Tk):
        for index, (field_name, label_name) in enumerate(self.form_items_to_draw.items()):
            tkinter.Label(root, text=label_name).grid(row=index, column=0, padx=5, pady=5)
            self.controller.entries[field_name] = tkinter.Entry(root)
            # Отрисовка списка
            self.controller.entries[field_name].grid(row=index, column=1, padx=5, pady=5)

    def list_all_objects_grid(self, root: tkinter.Tk):
        all_room_types_table = RoomTypeTable(root, columns=5, cell_width=265, cell_height=85)
        all_room_types_table.draw_all()

    def update_object_input_grid(self, root: tkinter.Tk, room_type_id: int):
        room_type = RoomTypeSerializer.prepare_data_to_print([RoomType.get(room_type_id)])[0]
        self.draw_update_room_type_form(root, room_type)

    def draw_update_room_type_form(self, root, room_type):
        for index, (field_name, label_name) in enumerate(self.form_items_to_draw.items()):
            tkinter.Label(root, text=label_name).grid(row=index, column=0, padx=5, pady=5)
            if "room_type_title_entry" in field_name:
                self.controller.entries[field_name] = tkinter.Entry(root)
                self.controller.entries[field_name].insert(0, room_type["title"])
            if "room_type_description_entry" in field_name:
                self.controller.entries[field_name] = tkinter.Entry(root)
                self.controller.entries[field_name].insert(0, room_type["description"])
            if "room_type_price_entry" in field_name:
                self.controller.entries[field_name] = tkinter.Entry(root)
                self.controller.entries[field_name].insert(0, room_type["price"])
            self.controller.entries[field_name].grid(row=index, column=1, padx=5, pady=5)


class WorkScheduleRenderer(Renderer):
    create_window_title = "Создание нового графика работы"
    create_window_size = "800x600"
    submit_create_button_position_row = 3

    list_all_window_title = "Список всех графиков работы"
    list_all_window_size = "1800x600"

    update_window_title = "Редактирование графика работы"
    update_window_size = "800x600"
    submit_update_button_position_row = 3

    form_items_to_draw = {
        "work_schedule_title_entry": "Название:",
    }

    def set_controller(self):
        return WorkScheduleController()

    def draw_create_object_form(self, root: tkinter.Tk):
        for index, (field_name, label_name) in enumerate(self.form_items_to_draw.items()):
            tkinter.Label(root, text=label_name).grid(row=index, column=0, padx=5, pady=5)
            self.controller.entries[field_name] = tkinter.Entry(root)
            # Отрисовка списка
            self.controller.entries[field_name].grid(row=index, column=1, padx=5, pady=5)

    def list_all_objects_grid(self, root: tkinter.Tk):
        all_work_schedules_table = WorkScheduleTable(root, columns=3, cell_width=265, cell_height=85)
        all_work_schedules_table.draw_all()

    def update_object_input_grid(self, root: tkinter.Tk, work_schedule_id: int):
        work_schedule = WorkScheduleSerializer.prepare_data_to_print([WorkSchedule.get(work_schedule_id)])[0]
        self.draw_update_work_schedule_form(root, work_schedule)

    def draw_update_work_schedule_form(self, root, work_schedule):
        for index, (field_name, label_name) in enumerate(self.form_items_to_draw.items()):
            tkinter.Label(root, text=label_name).grid(row=index, column=0, padx=5, pady=5)
            if "work_schedule_title_entry" in field_name:
                self.controller.entries[field_name] = tkinter.Entry(root)
                self.controller.entries[field_name].insert(0, work_schedule["work_schedule_title"])
            self.controller.entries[field_name].grid(row=index, column=1, padx=5, pady=5)
