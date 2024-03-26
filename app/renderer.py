import tkinter
from functools import partial
from tkinter import ttk
from typing import Dict

from tkcalendar import Calendar

from hotel.models import Client, JobType, Department, WorkSchedule, Employee
from db.serializers import ClientDataSerializer, EmployeeSerializer
from design_objects.table import ClientsTable, EmployeesTable
from hotel.controller import EmployeeController, ClientController


class ClientRenderer:
    def __init__(self):
        self.controller = ClientController()

    def create_new_client_window(self):
        root = tkinter.Tk()
        root.title("Создание нового клиента")
        root.geometry("800x600")

        self.__create_new_client_input_grid(root)

        submit_button = tkinter.Button(
            root, text="Отправить", command=self.controller.submit_create_client_data
        )
        submit_button.grid(row=7, columnspan=7, padx=5, pady=5)

        root.mainloop()

    # def book_room(self):
    #     root = tkinter.Tk()
    #     root.title("Бронирование комнаты")
    #     root.geometry("800x600")
    #
    #     self.__book_a_room_input_grid(root)
    #
    #     submit_button = tkinter.Button(
    #         root, text="Отправить", command=self.handler.book_room_for_client
    #     )
    #     submit_button.grid(row=7, columnspan=7, padx=5, pady=5)
    #
    #     root.mainloop()

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
            root, text="Отправить", command=partial(self.controller.submit_update_client_data, client_id)
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

        client = ClientDataSerializer.prepare_data_to_print([Client.get_client(client_id)])[0]
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
            root, text="Отправить", command=self.controller.submit_create_employee_data
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
            "job_type_combobox": "Должность:",
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
            "job_type_combobox": "Должность:",
            "hiring_date_calendar": "Дата найма:",
            "salary_entry": "Зарплата:",
            "department_combobox": "Отдел:",
            "work_schedule_combobox": "График работы:",
            "work_status_entry": "Статус:",
        }
        self.draw_update_employee_form(root, items_to_draw, employee_dict)

    def draw_create_employee_form(self, root: tkinter.Tk, items_to_draw: Dict):

        self.controller.entries["job_type_list"] = JobType.all_as_dict()
        self.controller.entries["department_list"] = Department.all_as_dict()
        self.controller.entries["work_schedule_list"] = WorkSchedule.all_as_dict()

        for index, (field_name, label_name) in enumerate(items_to_draw.items()):
            tkinter.Label(root, text=label_name).grid(row=index, column=0, padx=5, pady=5)

            if "calendar" in field_name:
                self.controller.entries[field_name] = Calendar(root, selectmode="day", date_pattern="dd.MM.yyyy")
            elif "job_type_combobox" in field_name:
                self.controller.entries["job_type_combobox_selected_text"] = tkinter.StringVar()
                self.controller.entries[field_name] = ttk.Combobox(root, textvariable=self.controller.entries["job_type_combobox_selected_text"])
                self.controller.entries[field_name]['values'] = list(self.controller.entries["job_type_list"].values())
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

        self.controller.entries["job_type_list"] = JobType.all_as_dict()
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
            elif "job_type_combobox" in field_name:
                self.controller.entries["job_type_combobox_selected_text"] = tkinter.StringVar()
                self.controller.entries[field_name] = ttk.Combobox(root, textvariable=self.controller.entries["job_type_combobox_selected_text"])
                self.controller.entries[field_name]['values'] = list(self.controller.entries["job_type_list"].values())
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
            root, text="Отправить", command=partial(self.controller.submit_update_employee_data, employee_id)
        )
        submit_button.grid(row=14, columnspan=7, padx=5, pady=5)

        root.mainloop()
