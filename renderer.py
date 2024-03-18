import tkinter
import textwrap
from tkinter import ttk
from typing import Dict

from tkcalendar import Calendar

from db.models import Client
from handlers import HotelHandler
from serializers import ClientDataSerializer


class HotelRenderer:
    def __init__(self):
        self.handler = HotelHandler()

    def create_new_client_window(self):
        root = tkinter.Tk()
        root.title("Создание нового клиента")
        root.geometry("800x600")

        self.__create_new_client_input_grid(root)

        submit_button = tkinter.Button(
            root, text="Отправить", command=self.handler.submit_client_data
        )
        submit_button.grid(row=7, columnspan=7, padx=5, pady=5)

        root.mainloop()

    def book_a_room(self):
        root = tkinter.Tk()
        root.title("Бронирование комнаты")
        root.geometry("800x600")

        self.__book_a_room_input_grid(root)

        submit_button = tkinter.Button(
            root, text="Отправить", command=self.handler.submit_client_data
        )
        submit_button.grid(row=7, columnspan=7, padx=5, pady=5)

        root.mainloop()

    def read_all_clients_window(self):
        root = tkinter.Tk()
        root.title("Список всех клиентов")
        root.geometry("1600x600")

        all_clients = self.handler.db_manager.get_all_clients()
        formatted_clients_data = ClientDataSerializer.prepare_data_to_print(all_clients)

        self.__display_all_clients_grid(root, formatted_clients_data)

        root.mainloop()

    def update_client_window(self):
        pass

    def delete_client_window(self):
        pass

    def draw(self, root, items_to_draw: Dict):
        for index, (entry_name, label_name) in enumerate(items_to_draw.items()):
            tkinter.Label(root, text=label_name).grid(row=index, column=0, padx=5, pady=5)
            self.handler.entries[entry_name] = tkinter.Entry(root)
            self.handler.entries[entry_name].grid(row=index, column=1, padx=5, pady=5)

    def __create_new_client_input_grid(self, root):
        items_to_draw = {
            "first_name_entry": "Фамилия:",
            "last_name_entry": "Имя:",
            "patronymic_entry": "Отчество:",
            "email_entry": "Электронная почта:",
            "phone_number_entry": "Номер телефона:",
            "passport_number_entry": "Номер паспорта:",
        }
        self.draw(root, items_to_draw)

    def __book_a_room_input_grid(self, root):

        full_name_label = tkinter.Label(root, text="ФИО клиента:")
        full_name_label.grid(row=0, column=0, padx=5, pady=5)

        all_clients = Client.get_all_clients()
        all_client_full_names = ClientDataSerializer.extract_full_names(all_clients)

        full_name_combo = ttk.Combobox(root, values=all_client_full_names, state="readonly", width=50)
        full_name_combo.grid(row=0, column=1, padx=5, pady=5)
        full_name_combo.set("Выберите вариант")

        room_number_label = tkinter.Label(root, text="№ комнаты")
        room_number_label.grid(row=1, column=0, padx=5, pady=5)
        self.handler.room_number_entry = tkinter.Entry(root)
        self.handler.room_number_entry.grid(row=1, column=1, padx=5, pady=5)

        date_from_label = tkinter.Label(root, text="Дата приезда")
        date_from_label.grid(row=2, column=0, padx=5, pady=5)
        self.handler.date_from_calendar = Calendar(
            root, selectmode="day", date_pattern="dd.MM.yyyy"
        )
        self.handler.date_from_calendar.grid(row=2, column=1, padx=5, pady=5)

        date_to_label = tkinter.Label(root, text="Дата отъезда")
        date_to_label.grid(row=3, column=0, padx=5, pady=5)
        self.handler.date_to_calendar = Calendar(
            root, selectmode="day", date_pattern="dd.MM.yyyy"
        )
        self.handler.date_to_calendar.grid(row=3, column=1, padx=5, pady=5)

        additional_service_label = tkinter.Label(root, text="Доп услуги")
        additional_service_label.grid(row=4, column=0, padx=5, pady=5)
        self.handler.additional_service_entry = tkinter.Entry(root)
        self.handler.additional_service_entry.grid(row=4, column=1, padx=5, pady=5)

        payment_type_label = tkinter.Label(root, text="Форма оплаты")
        payment_type_label.grid(row=5, column=0, padx=5, pady=5)
        self.handler.payment_type_entry = tkinter.Entry(root)
        self.handler.payment_type_entry.grid(row=5, column=1, padx=5, pady=5)

    def __display_all_clients_grid(self, root, clients):
        style = ttk.Style()
        style.configure("My.Treeview", rowheight=100)  # Задаем начальную высоту строки

        frame = tkinter.Frame(root)
        frame.pack(pady=10)

        self.tree = ttk.Treeview(frame, columns=('registration_number', 'fio', 'room_number', 'date_from', 'date_to', 'additional_service', 'payment_type'), show='headings', style="My.Treeview")

        self.tree.heading('registration_number', text='Номер регистрации')
        self.tree.heading('fio', text='ФИО')
        self.tree.heading('room_number', text='№ комнаты')
        self.tree.heading('date_from', text='Дата приезда')
        self.tree.heading('date_to', text='Дата отъезда')
        self.tree.heading('additional_service', text='Доп услуги')
        self.tree.heading('payment_type', text='Форма оплаты')
        self.tree.pack()

        self.tree.column('additional_service', width=350)

        for client in clients:
            user_info = (
                client['registration_number'],
                client['fio'],
                client['room_number'],
                client['date_from'],
                client['date_to'],
                textwrap.fill(client['additional_service'], 36),
                client['payment_type']
            )
            self.tree.insert('', tkinter.END, values=user_info)
