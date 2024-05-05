import sys
from abc import abstractmethod
from functools import partial

from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QRect, QDate
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QSpacerItem, QSizePolicy,
                             QPushButton, QHBoxLayout, QComboBox, QCheckBox, QApplication)

from db.serializers import (ClientDataSerializer, PaymentTypeSerializer, EmployeeSerializer, JobPositionSerializer,
    DepartmentSerializer, WorkScheduleSerializer, HotelRoomSerializer, RoomTypeSerializer,
    BookingSerializer)
from design.calendar import RussianCalendar
from design.style import (form_create_title, form_create_label_name_font_style, form_create_input_field_style,
                          submit_button_style, input_edit_style)

from design.window import QTAllActionsWindow

from hotel.controller import (ClientController, PaymentTypeController, EmployeeController, JobPositionController,
                              DepartmentController, WorkScheduleController, HotelRoomController, RoomTypeController,
                              BookingController)
from hotel.models import (JobPosition, Department, WorkSchedule, Employee, RoomType, Client, PaymentType, HotelRoom, Booking, Auth)


class QTBaseForm(QWidget):
    window_title = "Table Example"
    window_edit_title = "Table Edit Example"
    window_geometry = QRect(0, 0, 800, 600)
    items_to_draw = [i for i in range(5)]
    input_data = {}
    object_data = None

    def __init__(self, object_id=None):
        super().__init__()

        self.setGeometry(self.window_geometry)
        self.setStyleSheet("font-family: Arial, sans-serif;")

        if object_id is not None:
            self.setWindowTitle(self.window_edit_title)
            self.object_data = self._get_serializer_data(object_id)
            self.init_edit_ui()
        else:
            self.setWindowTitle(self.window_title)
            self.init_ui()

    @abstractmethod
    def _get_serializer_data(self, object_id):
        # client_data = ClientDataSerializer.prepare_data_to_print([Client.get(client_id)])[0]
        return None

    def init_ui(self):
        # Создаем вертикальный макет для главного окна
        main_layout = QVBoxLayout()

        # Создаем заголовок
        title_label = QLabel(self.window_title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        title_label.setStyleSheet(form_create_title)
        main_layout.addWidget(title_label)

        self.add_objects_to_form(main_layout)

    def init_edit_ui(self):
        # Создаем вертикальный макет для главного окна
        main_layout = QVBoxLayout()

        # Создаем заголовок
        title_label = QLabel(self.window_title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        title_label.setStyleSheet(form_create_title)
        main_layout.addWidget(title_label)

        self.add_objects_to_form(main_layout)

    def add_objects_to_form(self, main_layout):
        # Создаем сеточный макет для полей формы
        form_layout = QGridLayout()

        self._add_labels_and_inputs(form_layout)

        # Добавляем сеточный макет с полями в вертикальный макет
        main_layout.addLayout(form_layout)

        # Создаем горизонтальный пространственный элемент перед кнопкой
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        main_layout.addItem(spacer_bottom)

        self._add_submit_button(main_layout)
        # Создаем кнопку "Отправить"

        # Устанавливаем вертикальный макет для главного окна
        self.setLayout(main_layout)

        # Привязываем события наведения курсора на поля ввода
        for i in range(len(self.items_to_draw)):
            edit_widget = self.findChild(QLineEdit, f"edit_{i}")
            if edit_widget:
                edit_widget.installEventFilter(self)

    def _add_submit_button(self, main_layout):
        self.submit_button = QPushButton("Отправить")
        self.submit_button.setStyleSheet(submit_button_style)  # Изменяем цвет при нажатии
        self.submit_button.clicked.connect(self.on_submit_button_clicked)
        main_layout.addWidget(self.submit_button,
                              alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)

    def _add_labels_and_inputs(self, form_layout):
        if self.object_data is not None:
            pass
        else:
            # Создаем и добавляем названия полей и поля для ввода
            for i in self.items_to_draw:
                label = QLabel(f"Поле {i}:")
                label.setStyleSheet("color: #333; font-size: 16px;")
                edit = QLineEdit()
                edit.setStyleSheet(input_edit_style)
                edit.setObjectName(f"edit_{i}")  # Добавляем objectName для дальнейшей настройки стилей через CSS
                form_layout.addWidget(label, i, 0)
                form_layout.addWidget(edit, i, 1)

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


class QTBookingForm(QTBaseForm):
    window_title = "Создание бронирования"
    window_geometry = QRect(100, 100, 1200, 600)
    items_to_draw = {
        "room_id_entry": "Номер комнаты",
        "date_from_calendar": "Дата приезда",
        "date_to_calendar": "Дата отъезда",
        "booking_date_calendar": "Дата создания бронирования",
        "payment_type_combobox": "Форма оплаты",
        "client_combobox": "Клиент",
        "payment_status_checkbox": "Статус оплаты",
        "final_price_entry": "Итоговая стоимость",
    }

    def __init__(self, object_id=None, date_from=None, date_to=None, room_id=None, room_type_price=None):
        self.date_from = date_from
        self.date_to = date_to
        self.room_id = room_id
        self.room_type_price = room_type_price
        super().__init__(object_id)

    def _get_serializer_data(self, object_id):
        object_data = BookingSerializer.prepare_data_to_print([Booking.get(object_id)])[0]
        return object_data

    def _add_submit_button(self, main_layout):
        self.submit_button = QPushButton("Отправить")
        self.submit_button.setStyleSheet(submit_button_style)  # Изменяем цвет при нажатии

        if self.object_data is not None:
            self.submit_button.clicked.connect(partial(BookingController.submit_update, self.input_data, self.object_data["id"]))
        else:
            self.submit_button.clicked.connect(partial(BookingController.submit_create, self.input_data))

        main_layout.addWidget(self.submit_button,
                              alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)

    def _add_labels_and_inputs(self, form_layout):
        self.input_data = {}
        if self.object_data is not None:
            for index, (field_name, label_name) in enumerate(self.items_to_draw.items()):
                label = QLabel(f"{label_name}:")
                label.setStyleSheet(form_create_label_name_font_style)

                if "room_id_entry" in field_name:
                    edit = QLineEdit()
                    edit.setStyleSheet(form_create_input_field_style)
                    edit.setText(str(self.object_data["room_id"]))
                elif "date_from_calendar" in field_name:
                    edit = RussianCalendar()
                    specific_date = QDate(self.object_data["date_from"].year,
                                          self.object_data["date_from"].month,
                                          self.object_data["date_from"].day)
                    edit.setSelectedDate(specific_date)
                elif "date_to_calendar" in field_name:
                    edit = RussianCalendar()
                    specific_date = QDate(self.object_data["date_to"].year,
                                          self.object_data["date_to"].month,
                                          self.object_data["date_to"].day)
                    edit.setSelectedDate(specific_date)
                elif "booking_date_calendar" in field_name:
                    edit = RussianCalendar()
                    specific_date = QDate(self.object_data["creation_date"].year,
                                          self.object_data["creation_date"].month,
                                          self.object_data["creation_date"].day)
                    edit.setSelectedDate(specific_date)
                    edit.setEnabled(False)

                elif "payment_type_combobox" in field_name:

                    payment_type_list = PaymentType.all_as_dict()
                    edit = QComboBox()

                    for item_id, text in payment_type_list.items():
                        edit.addItem(text, item_id)

                    default_id = self.object_data["payment_type"]
                    combobox_index = edit.findData(default_id)
                    edit.setCurrentIndex(combobox_index)
                elif "client_combobox" in field_name:
                    client_list = Client.all_as_dict()
                    edit = QComboBox()

                    for item_id, text in client_list.items():
                        edit.addItem(text, item_id)

                    default_id = self.object_data["client"]
                    combobox_index = edit.findData(default_id)
                    edit.setCurrentIndex(combobox_index)

                elif "payment_status_checkbox" in field_name:
                    edit = QCheckBox()
                    edit.setStyleSheet(form_create_input_field_style)
                    edit.setChecked(self.object_data["payment_status"])
                elif "final_price_entry" in field_name:
                    edit = QLineEdit()
                    edit.setStyleSheet(form_create_input_field_style)
                    edit.setText(str(self.object_data["final_price"]))

                edit.setObjectName(f"edit_{index}")  # Добавляем objectName для дальнейшей настройки стилей через CSS

                self.input_data[field_name] = edit

                form_layout.addWidget(label, index, 0)
                form_layout.addWidget(edit, index, 1)
        else:
            # Создаем и добавляем названия полей и поля для ввода
            for index, (field_name, label_name) in enumerate(self.items_to_draw.items()):
                label = QLabel(f"{label_name}:")
                label.setStyleSheet(form_create_label_name_font_style)
                if "date_from_calendar" in field_name:
                    edit = RussianCalendar()
                    specific_date = QDate(self.date_from.year,
                                          self.date_from.month,
                                          self.date_from.day)
                    edit.setSelectedDate(specific_date)
                    edit.setEnabled(False)
                elif "date_to_calendar" in field_name:
                    edit = RussianCalendar()
                    specific_date = QDate(self.date_to.year,
                                          self.date_to.month,
                                          self.date_to.day)
                    edit.setSelectedDate(specific_date)
                    edit.setEnabled(False)
                elif "booking_date_calendar" in field_name:
                    edit = RussianCalendar()
                    edit.setSelectedDate(edit.selectedDate())
                    edit.setEnabled(False)
                elif "payment_type_combobox" in field_name:
                    payment_type_list = PaymentType.all_as_dict()
                    edit = QComboBox()
                    for item_id, text in payment_type_list.items():
                        edit.addItem(text, item_id)
                elif "client_combobox" in field_name:
                    client_list = Client.all_as_dict()
                    edit = QComboBox()
                    for item_id, text in client_list.items():
                        edit.addItem(text, item_id)
                elif "room_id_entry" in field_name:
                    edit = QLineEdit()
                    edit.setStyleSheet(form_create_input_field_style)
                    edit.setText(str(self.room_id))
                    edit.setEnabled(False)
                elif "checkbox" in field_name:
                    edit = QCheckBox()
                elif "final_price_entry" in field_name:
                    edit = QLineEdit()
                    edit.setStyleSheet(form_create_input_field_style)
                    delta = self.date_to - self.date_from
                    if delta.days == 0:
                        days = 1
                    else:
                        days = delta.days
                    final_price = self.room_type_price * days
                    edit.setText(str(final_price))
                    edit.setEnabled(False)
                edit.setObjectName(f"edit_{index}")  # Добавляем objectName для дальнейшей настройки стилей через CSS

                self.input_data[field_name] = edit

                form_layout.addWidget(label, index, 0)
                form_layout.addWidget(edit, index, 1)


class QTBookingSearchForm(QTBaseForm):
    window_title = "Поиск доступных номеров"
    window_geometry = QRect(100, 100, 1200, 600)

    def __init__(self):
        self.calendar_date_from = RussianCalendar()
        self.calendar_date_to = RussianCalendar()

        self.calendar_date_from.setMinimumHeight(180)
        self.calendar_date_to.setMinimumHeight(180)
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
        self.submit_button.setStyleSheet(submit_button_style)  # Изменяем цвет при нажатии
        self.submit_button.clicked.connect(self.on_submit_button_clicked)
        main_layout.addWidget(self.submit_button,
                              alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)

        # Устанавливаем вертикальный макет для главного окна
        self.setLayout(main_layout)

    def on_submit_button_clicked(self):
        from design.table import QTAvailableRoomsTable

        date_from = self.calendar_date_from.selectedDate()
        print("Выбранная дата в календаре 1:", date_from.toString())

        date_to = self.calendar_date_to.selectedDate()
        print("Выбранная дата в календаре 2:", date_to.toString())

        self.available_rooms = QTAvailableRoomsTable(date_from.toPyDate(), date_to.toPyDate())
        self.available_rooms.show()


class LoginForm(QWidget):
    window_title = "Авторизация"
    window_geometry = QRect(100, 100, 400, 200)

    def __init__(self,):
        super().__init__()
        # self.all_actions_window = all_actions_window

        self.setWindowTitle(self.window_title)
        self.setGeometry(self.window_geometry)

        # Create form elements
        self.username_label = QLabel("Username:")
        self.username_edit = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_button = QPushButton("Login")

        # Create layout for form elements
        form_layout = QVBoxLayout()
        form_layout.addWidget(self.username_label)
        form_layout.addWidget(self.username_edit)
        form_layout.addWidget(self.password_label)
        form_layout.addWidget(self.password_edit)

        # Create layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.login_button)

        # Добавить QLabel для сообщения
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")  # Стиль для сообщения об ошибке
        form_layout.addWidget(self.error_label)  # Разместить в макете

        # Combine layouts and set main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        # Подключить обработчики событий
        self.login_button.clicked.connect(self.login_handler)

    def login_handler(self):
        # Получить введенные данные
        username = self.username_edit.text()
        password = self.password_edit.text()

        result = Auth.is_user_in_db(username, password)
        # Проверка данных (заменить на свою логику)
        if result:
            # Авторизация прошла успешно
            print("Авторизация прошла успешно!")
            self.hide()

            if "admin" in username:
                self.create_all_actions_window_for_admin()
            else:
                self.create_all_actions_window_for_manager()
        else:
            # Неверные логин/пароль
            print("Неверные логин/пароль!")
            self.error_label.setText("Неверный логин или пароль!")

    def create_all_actions_window_for_admin(self):
        self.all_actions_view = QTAllActionsForm()
        self.all_actions_window = QTAllActionsWindow(self.all_actions_view.items_to_draw_for_admin)
        self.all_actions_window.show()


    def create_all_actions_window_for_manager(self):
        self.all_actions_view = QTAllActionsForm()
        self.all_actions_window = QTAllActionsWindow(self.all_actions_view.items_to_draw_for_manager)
        self.all_actions_window.show()



class QTClientForm(QTBaseForm):
    window_title = "Создание клиента"
    window_edit_title = "Редактирование клиента"
    window_geometry = QRect(100, 100, 1200, 600)
    items_to_draw = {
        "last_name_entry": "Фамилия",
        "first_name_entry": "Имя",
        "patronymic_entry": "Отчество",
        "birthday_date_calendar": "Дата рождения",
        "email_entry": "Электронная почта",
        "phone_number_entry": "Номер телефона",
        "passport_number_entry": "Номер паспорта",
    }

    def _get_serializer_data(self, object_id):
        client_data = ClientDataSerializer.prepare_data_to_print([Client.get(object_id)])[0]
        return client_data

    def _add_submit_button(self, main_layout):
        self.submit_button = QPushButton("Отправить")
        self.submit_button.setStyleSheet(submit_button_style)  # Изменяем цвет при нажатии

        if self.object_data is not None:
            self.submit_button.clicked.connect(
                partial(ClientController.submit_update, self.input_data, self.object_data["id"]))
        else:
            self.submit_button.clicked.connect(partial(ClientController.submit_create, self.input_data))

        main_layout.addWidget(self.submit_button,
                              alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)

    def _add_labels_and_inputs(self, form_layout):
        self.input_data = {}
        if self.object_data is not None:
            for index, (field_name, label_name) in enumerate(self.items_to_draw.items()):
                label = QLabel(f"{label_name}:")
                label.setStyleSheet(form_create_label_name_font_style)

                if "first_name_entry" in field_name:
                    edit = QLineEdit()
                    edit.setStyleSheet(form_create_input_field_style)
                    edit.setText(self.object_data["first_name"])
                elif "last_name_entry" in field_name:
                    edit = QLineEdit()
                    edit.setStyleSheet(form_create_input_field_style)
                    edit.setText(self.object_data["last_name"])
                elif "patronymic_entry" in field_name:
                    edit = QLineEdit()
                    edit.setStyleSheet(form_create_input_field_style)
                    edit.setText(self.object_data["patronymic"])
                elif "birthday_date_calendar" in field_name:
                    edit = RussianCalendar()
                    specific_date = QDate(self.object_data["birthday_date"].year,
                                          self.object_data["birthday_date"].month,
                                          self.object_data["birthday_date"].day)
                    edit.setSelectedDate(specific_date)
                elif "email_entry" in field_name:
                    edit = QLineEdit()
                    edit.setStyleSheet(form_create_input_field_style)
                    edit.setText(self.object_data["email"])
                elif "phone_number_entry" in field_name:
                    edit = QLineEdit()
                    edit.setStyleSheet(form_create_input_field_style)
                    edit.setText(self.object_data["phone_number"])
                elif "passport_number_entry" in field_name:
                    edit = QLineEdit()
                    edit.setStyleSheet(form_create_input_field_style)
                    edit.setText(self.object_data["passport_number"])

                edit.setObjectName(f"edit_{index}")  # Добавляем objectName для дальнейшей настройки стилей через CSS

                self.input_data[field_name] = edit

                form_layout.addWidget(label, index, 0)
                form_layout.addWidget(edit, index, 1)
        else:
            # Создаем и добавляем названия полей и поля для ввода
            for index, (field_name, label_name) in enumerate(self.items_to_draw.items()):
                label = QLabel(f"{label_name}:")
                label.setStyleSheet(form_create_label_name_font_style)
                if "calendar" in field_name:
                    edit = RussianCalendar()
                else:
                    edit = QLineEdit()
                    edit.setStyleSheet(form_create_input_field_style)
                edit.setObjectName(f"edit_{index}")  # Добавляем objectName для дальнейшей настройки стилей через CSS

                self.input_data[field_name] = edit

                form_layout.addWidget(label, index, 0)
                form_layout.addWidget(edit, index, 1)


class QTPaymentTypeForm(QTBaseForm):
    window_title = "Создание способа оплаты"
    window_geometry = QRect(100, 100, 1200, 600)
    items_to_draw = {
        "description_entry": "Описание оплаты",
    }

    def _get_serializer_data(self, object_id):
        payment_type_data = PaymentTypeSerializer.prepare_data_to_print([PaymentType.get(object_id)])[0]
        return payment_type_data

    def _add_submit_button(self, main_layout):
        self.submit_button = QPushButton("Отправить")
        self.submit_button.setStyleSheet(submit_button_style)  # Изменяем цвет при нажатии

        if self.object_data is not None:
            self.submit_button.clicked.connect(partial(PaymentTypeController.submit_update, self.input_data, self.object_data["id"]))
        else:
            self.submit_button.clicked.connect(partial(PaymentTypeController.submit_create, self.input_data))

        main_layout.addWidget(self.submit_button,
                              alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)

    def _add_labels_and_inputs(self, form_layout):
        self.input_data = {}

        label = QLabel(f"{self.items_to_draw["description_entry"]}:")
        label.setStyleSheet(form_create_label_name_font_style)
        edit = QLineEdit()
        edit.setStyleSheet(form_create_input_field_style)

        if self.object_data is not None:
            edit.setText(self.object_data["description"])

        edit.setObjectName(f"edit_{0}")  # Добавляем objectName для дальнейшей настройки стилей через CSS
        self.input_data["description_entry"] = edit
        form_layout.addWidget(label, 0, 0)
        form_layout.addWidget(edit, 0, 1)


class QTEmployeeForm(QTBaseForm):
    window_title = "Добавление новых сотрудников"
    window_geometry = QRect(100, 100, 1200, 600)
    items_to_draw = {
        "last_name_entry": "Фамилия",
        "first_name_entry": "Имя",
        "patronymic_entry": "Отчество",
        "birthday_date_calendar": "Дата рождения",
        "passport_number_entry": "Номер паспорта",
        "job_position_combobox": "Должность",
        "email_entry": "Электронная почта",
        "phone_number_entry": "Номер телефона",
        "hiring_date_calendar": "Дата найма",
        "salary_entry": "Зарплата",
        "department_combobox": "Отдел",
        "work_schedule_combobox": "График работы",
        "work_status_entry": "Статус",
    }

    def _get_serializer_data(self, object_id):
        object_data = EmployeeSerializer.prepare_data_to_print([Employee.get(object_id)])[0]
        return object_data

    def _add_submit_button(self, main_layout):
        self.submit_button = QPushButton("Отправить")
        self.submit_button.setStyleSheet(submit_button_style)  # Изменяем цвет при нажатии

        if self.object_data is not None:
            self.submit_button.clicked.connect(partial(EmployeeController.submit_update, self.input_data, self.object_data["id"]))
        else:
            self.submit_button.clicked.connect(partial(EmployeeController.submit_create, self.input_data))

        main_layout.addWidget(self.submit_button,
                              alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)

    def _add_labels_and_inputs(self, form_layout):
        self.input_data = {}
        if self.object_data is not None:
            # Создаем и добавляем названия полей и поля для ввода
            for index, (field_name, label_name) in enumerate(self.items_to_draw.items()):
                label = QLabel(f"{label_name}:")
                label.setStyleSheet(form_create_label_name_font_style)

                if "first_name_entry" in field_name:
                    edit = QLineEdit()
                    edit.setStyleSheet(form_create_input_field_style)
                    edit.setText(self.object_data["first_name"])
                elif "last_name_entry" in field_name:
                    edit = QLineEdit()
                    edit.setStyleSheet(form_create_input_field_style)
                    edit.setText(self.object_data["last_name"])
                elif "patronymic_entry" in field_name:
                    edit = QLineEdit()
                    edit.setStyleSheet(form_create_input_field_style)
                    edit.setText(self.object_data["patronymic"])
                elif "birthday_date_calendar" in field_name:
                    edit = RussianCalendar()
                    specific_date = QDate(self.object_data["birthday_date"].year,
                                          self.object_data["birthday_date"].month,
                                          self.object_data["birthday_date"].day)
                    edit.setSelectedDate(specific_date)
                elif "passport_number_entry" in field_name:
                    edit = QLineEdit()
                    edit.setStyleSheet(form_create_input_field_style)
                    edit.setText(self.object_data["passport_number"])
                elif "email_entry" in field_name:
                    edit = QLineEdit()
                    edit.setStyleSheet(form_create_input_field_style)
                    edit.setText(self.object_data["email"])
                elif "phone_number_entry" in field_name:
                    edit = QLineEdit()
                    edit.setStyleSheet(form_create_input_field_style)
                    edit.setText(self.object_data["phone_number"])
                elif "job_position_combobox" in field_name:

                    job_position_list = JobPosition.all_as_dict()
                    edit = QComboBox()

                    for item_id, text in job_position_list.items():
                        edit.addItem(text, item_id)

                    default_id = self.object_data["job_position"]
                    combobox_index = edit.findData(default_id)
                    edit.setCurrentIndex(combobox_index)

                elif "hiring_date_calendar" in field_name:
                    edit = RussianCalendar()
                    specific_date = QDate(self.object_data["hiring_date"].year,
                                          self.object_data["hiring_date"].month,
                                          self.object_data["hiring_date"].day)
                    edit.setSelectedDate(specific_date)
                elif "salary_entry" in field_name:
                    edit = QLineEdit()
                    edit.setStyleSheet(form_create_input_field_style)
                    edit.setText(f"{self.object_data["salary"]}")
                elif "department_combobox" in field_name:
                    department_list = Department.all_as_dict()
                    edit = QComboBox()
                    for item_id, text in department_list.items():
                        edit.addItem(text, item_id)

                    default_id = self.object_data["department"]
                    combobox_index = edit.findData(default_id)
                    edit.setCurrentIndex(combobox_index)
                elif "work_schedule_combobox" in field_name:
                    work_schedule_list = WorkSchedule.all_as_dict()
                    edit = QComboBox()

                    for item_id, text in work_schedule_list.items():
                        edit.addItem(text, item_id)

                    default_id = self.object_data["work_schedule"]
                    combobox_index = edit.findData(default_id)
                    edit.setCurrentIndex(combobox_index)
                elif "work_status_entry" in field_name:
                    edit = QLineEdit()
                    edit.setStyleSheet(form_create_input_field_style)
                    edit.setText(self.object_data["work_status"])

                edit.setObjectName(f"edit_{index}")  # Добавляем objectName для дальнейшей настройки стилей через CSS

                self.input_data[field_name] = edit

                form_layout.addWidget(label, index, 0)
                form_layout.addWidget(edit, index, 1)
        else:
            # Создаем и добавляем названия полей и поля для ввода
            for index, (field_name, label_name) in enumerate(self.items_to_draw.items()):
                label = QLabel(f"{label_name}:")
                label.setStyleSheet(form_create_label_name_font_style)
                if "calendar" in field_name:
                    edit = RussianCalendar()
                elif "job_position_combobox" in field_name:
                    job_position_list = JobPosition.all_as_dict()
                    edit = QComboBox()

                    for item_id, text in job_position_list.items():
                        edit.addItem(text, item_id)

                elif "department_combobox" in field_name:
                    department_list = Department.all_as_dict()
                    edit = QComboBox()

                    for item_id, text in department_list.items():
                        edit.addItem(text, item_id)

                elif "work_schedule_combobox" in field_name:
                    work_schedule_list = WorkSchedule.all_as_dict()
                    edit = QComboBox()

                    for item_id, text in work_schedule_list.items():
                        edit.addItem(text, item_id)

                else:
                    edit = QLineEdit()
                    edit.setStyleSheet(form_create_input_field_style)
                edit.setObjectName(f"edit_{index}")  # Добавляем objectName для дальнейшей настройки стилей через CSS

                self.input_data[field_name] = edit

                form_layout.addWidget(label, index, 0)
                form_layout.addWidget(edit, index, 1)


class QTJobPositionForm(QTBaseForm):
    window_title = "Добавление новых должностей"
    window_geometry = QRect(100, 100, 1200, 600)
    items_to_draw = {
        "job_title_entry": "Название",
    }

    def _get_serializer_data(self, object_id):
        object_data = JobPositionSerializer.prepare_data_to_print([JobPosition.get(object_id)])[0]
        return object_data

    def _add_submit_button(self, main_layout):
        self.submit_button = QPushButton("Отправить")
        self.submit_button.setStyleSheet(submit_button_style)  # Изменяем цвет при нажатии

        if self.object_data is not None:
            self.submit_button.clicked.connect(partial(JobPositionController.submit_update, self.input_data, self.object_data["id"]))
        else:
            self.submit_button.clicked.connect(partial(JobPositionController.submit_create, self.input_data))

        main_layout.addWidget(self.submit_button,
                              alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)

    def _add_labels_and_inputs(self, form_layout):
        label = QLabel(f"{self.items_to_draw["job_title_entry"]}:")
        label.setStyleSheet(form_create_label_name_font_style)

        edit = QLineEdit()
        edit.setStyleSheet(form_create_input_field_style)

        if self.object_data is not None:
            edit.setText(self.object_data["job_title"])

        edit.setObjectName(f"edit_{0}")  # Добавляем objectName для дальнейшей настройки стилей через CSS

        self.input_data["job_title_entry"] = edit

        form_layout.addWidget(label, 0, 0)
        form_layout.addWidget(edit, 0, 1)


class QTDepartmentForm(QTBaseForm):
    window_title = "Добавление новых должностей"
    window_geometry = QRect(100, 100, 1200, 600)
    items_to_draw = {
        "department_title_entry": "Название",
    }

    def _get_serializer_data(self, object_id):
        object_data = DepartmentSerializer.prepare_data_to_print([Department.get(object_id)])[0]
        return object_data

    def _add_submit_button(self, main_layout):
        self.submit_button = QPushButton("Отправить")
        self.submit_button.setStyleSheet(submit_button_style)  # Изменяем цвет при нажатии

        if self.object_data is not None:
            self.submit_button.clicked.connect(partial(DepartmentController.submit_update, self.input_data, self.object_data["id"]))
        else:
            self.submit_button.clicked.connect(partial(DepartmentController.submit_create, self.input_data))


        main_layout.addWidget(self.submit_button,
                              alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)

    def _add_labels_and_inputs(self, form_layout):
        label = QLabel(f"{self.items_to_draw["department_title_entry"]}:")
        label.setStyleSheet(form_create_label_name_font_style)

        edit = QLineEdit()
        edit.setStyleSheet(form_create_input_field_style)

        if self.object_data is not None:
            edit.setText(self.object_data["department_title"])

        edit.setObjectName(f"edit_{0}")  # Добавляем objectName для дальнейшей настройки стилей через CSS

        self.input_data["department_title_entry"] = edit

        form_layout.addWidget(label, 0, 0)
        form_layout.addWidget(edit, 0, 1)


class QTWorkScheduleForm(QTBaseForm):
    window_title = "Добавление новых должностей"
    window_geometry = QRect(100, 100, 1200, 600)
    items_to_draw = {
        "work_schedule_title_entry": "Название",
    }

    def _get_serializer_data(self, object_id):
        object_data = WorkScheduleSerializer.prepare_data_to_print([WorkSchedule.get(object_id)])[0]
        return object_data

    def _add_submit_button(self, main_layout):
        self.submit_button = QPushButton("Отправить")
        self.submit_button.setStyleSheet(submit_button_style)  # Изменяем цвет при нажатии

        if self.object_data is not None:
            self.submit_button.clicked.connect(partial(WorkScheduleController.submit_update, self.input_data, self.object_data["id"]))
        else:
            self.submit_button.clicked.connect(partial(WorkScheduleController.submit_create, self.input_data))

        main_layout.addWidget(self.submit_button,
                              alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)

    def _add_labels_and_inputs(self, form_layout):
        label = QLabel(f"{self.items_to_draw["work_schedule_title_entry"]}:")
        label.setStyleSheet(form_create_label_name_font_style)

        edit = QLineEdit()
        edit.setStyleSheet(form_create_input_field_style)

        if self.object_data is not None:
            edit.setText(self.object_data["work_schedule_title"])

        edit.setObjectName(f"edit_{0}")  # Добавляем objectName для дальнейшей настройки стилей через CSS

        self.input_data["work_schedule_title_entry"] = edit

        form_layout.addWidget(label, 0, 0)
        form_layout.addWidget(edit, 0, 1)


class QTHotelRoomForm(QTBaseForm):
    window_title = "Добавление новых номеров"
    window_geometry = QRect(100, 100, 1200, 600)
    items_to_draw = {
        "employee_combobox": "Сотрудник",
        "room_type_combobox": "Категория номера",
    }

    def _get_serializer_data(self, object_id):
        object_data = HotelRoomSerializer.prepare_data_for_edit_form([HotelRoom.get(object_id)])[0]
        return object_data

    def _add_submit_button(self, main_layout):
        self.submit_button = QPushButton("Отправить")
        self.submit_button.setStyleSheet(submit_button_style)  # Изменяем цвет при нажатии

        if self.object_data is not None:
            self.submit_button.clicked.connect(partial(HotelRoomController.submit_update, self.input_data, self.object_data["id"]))
        else:
            self.submit_button.clicked.connect(partial(HotelRoomController.submit_create, self.input_data))

        main_layout.addWidget(self.submit_button,
                              alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)

    def _add_labels_and_inputs(self, form_layout):
        self.input_data = {}
        if self.object_data is not None:
            # Создаем и добавляем названия полей и поля для ввода
            for index, (field_name, label_name) in enumerate(self.items_to_draw.items()):
                label = QLabel(f"{label_name}:")
                label.setStyleSheet(form_create_label_name_font_style)
                if "employee_combobox" in field_name:
                    employee_list = Employee.all_as_dict()
                    edit = QComboBox()

                    for item_id, text in employee_list.items():
                        edit.addItem(text, item_id)

                    default_id = self.object_data["employee_id"]
                    combobox_index = edit.findData(default_id)
                    edit.setCurrentIndex(combobox_index)
                elif "room_type_combobox" in field_name:
                    room_type_list = RoomType.all_as_dict()
                    edit = QComboBox()

                    for item_id, text in room_type_list.items():
                        edit.addItem(text, item_id)

                    default_id = self.object_data["room_type_id"]
                    combobox_index = edit.findData(default_id)
                    edit.setCurrentIndex(combobox_index)

                edit.setObjectName(f"edit_{index}")  # Добавляем objectName для дальнейшей настройки стилей через CSS

                self.input_data[field_name] = edit

                form_layout.addWidget(label, index, 0)
                form_layout.addWidget(edit, index, 1)
        else:
            # Создаем и добавляем названия полей и поля для ввода
            for index, (field_name, label_name) in enumerate(self.items_to_draw.items()):
                label = QLabel(f"{label_name}:")
                label.setStyleSheet(form_create_label_name_font_style)
                if "employee_combobox" in field_name:
                    employee_list = Employee.all_as_dict()
                    edit = QComboBox()

                    for item_id, text in employee_list.items():
                        edit.addItem(text, item_id)

                elif "room_type_combobox" in field_name:
                    room_type_list = RoomType.all_as_dict()
                    edit = QComboBox()

                    for item_id, text in room_type_list.items():
                        edit.addItem(text, item_id)

                edit.setObjectName(f"edit_{index}")  # Добавляем objectName для дальнейшей настройки стилей через CSS

                self.input_data[field_name] = edit

                form_layout.addWidget(label, index, 0)
                form_layout.addWidget(edit, index, 1)


class QTRoomTypeForm(QTBaseForm):
    window_title = "Добавление новых типов номеров"
    window_geometry = QRect(100, 100, 1200, 600)
    items_to_draw = {
        "room_type_title_entry": "Название",
        "room_type_description_entry": "Описание",
        "room_type_price_entry": "Стоимость",
    }

    def _get_serializer_data(self, object_id):
        object_data = RoomTypeSerializer.prepare_data_to_print([RoomType.get(object_id)])[0]
        return object_data

    def _add_submit_button(self, main_layout):
        self.submit_button = QPushButton("Отправить")
        self.submit_button.setStyleSheet(submit_button_style)  # Изменяем цвет при нажатии

        if self.object_data is not None:
            self.submit_button.clicked.connect(partial(RoomTypeController.submit_update, self.input_data, self.object_data["id"]))
        else:
            self.submit_button.clicked.connect(partial(RoomTypeController.submit_create, self.input_data))

        main_layout.addWidget(self.submit_button,
                              alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)

    def _add_labels_and_inputs(self, form_layout):
        self.input_data = {}
        if self.object_data is not None:
            # Создаем и добавляем названия полей и поля для ввода
            for index, (field_name, label_name) in enumerate(self.items_to_draw.items()):
                label = QLabel(f"{label_name}:")
                label.setStyleSheet(form_create_label_name_font_style)
                edit = QLineEdit()
                edit.setStyleSheet(form_create_input_field_style)

                if "room_type_title_entry" in field_name:
                    edit.setText(self.object_data["title"])
                elif "room_type_description_entry" in field_name:
                    edit.setText(self.object_data["description"])
                elif "room_type_price_entry" in field_name:
                    edit.setText(str(self.object_data["price"]))

                edit.setObjectName(f"edit_{index}")  # Добавляем objectName для дальнейшей настройки стилей через CSS

                self.input_data[field_name] = edit

                form_layout.addWidget(label, index, 0)
                form_layout.addWidget(edit, index, 1)
        else:
            # Создаем и добавляем названия полей и поля для ввода
            for index, (field_name, label_name) in enumerate(self.items_to_draw.items()):
                label = QLabel(f"{label_name}:")
                label.setStyleSheet(form_create_label_name_font_style)
                edit = QLineEdit()
                edit.setStyleSheet(form_create_input_field_style)
                edit.setObjectName(f"edit_{index}")  # Добавляем objectName для дальнейшей настройки стилей через CSS

                self.input_data[field_name] = edit

                form_layout.addWidget(label, index, 0)
                form_layout.addWidget(edit, index, 1)


class QTAllActionsForm:
    def __init__(self):
        self.booking_window = None
        self.clients_window = None
        self.payment_type_window = None
        self.employee_window = None
        self.job_position_window = None
        self.departments_window = None
        self.work_schedule_window = None
        self.rooms_window = None
        self.room_types_window = None

        self.items_to_draw_for_admin = {
            "Бронирование": {
                "create": QTBookingSearchForm(),
                "read": self.open_booking_window,
            },
            "Клиенты": {
                "create": QTClientForm(),
                "read": self.open_clients_window,
            },
            "Способы оплаты": {
                "create": QTPaymentTypeForm(),
                "read": self.open_payment_type_window,
            },
            "Персонал": {
                "create": QTEmployeeForm(),
                "read": self.open_employee_window,
            },
            "Должности": {
                "create": QTJobPositionForm(),
                "read": self.open_job_position_window,
            },
            "Отделы": {
                "create": QTDepartmentForm(),
                "read": self.open_departments_window,
            },
            "График работы": {
                "create": QTWorkScheduleForm(),
                "read": self.open_work_schedule_window,
            },
            "Номера": {
                "create": QTHotelRoomForm(),
                "read": self.open_rooms_window,
            },
            "Типы номеров": {
                "create": QTRoomTypeForm(),
                "read": self.open_room_types_window,
            },
        }

        self.items_to_draw_for_manager = {
            "Бронирование": {
                "create": QTBookingSearchForm(),
                "read": self.open_booking_window,
            },
            "Клиенты": {
                "create": QTClientForm(),
                "read": self.open_clients_window,
            },
            "Способы оплаты": {
                "create": QTPaymentTypeForm(),
                "read": self.open_payment_type_window,
            },
            "Номера": {
                "create": QTHotelRoomForm(),
                "read": self.open_rooms_window,
            },
            "Типы номеров": {
                "create": QTRoomTypeForm(),
                "read": self.open_room_types_window,
            },
        }


    def open_booking_window(self):
        from design.table import QTBookingsTable
        self.booking_window = QTBookingsTable()
        self.booking_window.show()

    def open_clients_window(self):
        from design.table import QTClientsTable
        self.clients_window = QTClientsTable()
        self.clients_window.show()

    def open_payment_type_window(self):
        from design.table import QTPaymentTypeTable
        self.payment_type_window = QTPaymentTypeTable()
        self.payment_type_window.show()

    def open_employee_window(self):
        from design.table import QTEmployeeTable
        self.employee_window = QTEmployeeTable()
        self.employee_window.show()

    def open_job_position_window(self):
        from design.table import QTJobPositionTable
        self.job_position_window = QTJobPositionTable()
        self.job_position_window.show()

    def open_departments_window(self):
        from design.table import QTDepartmentTable
        self.departments_window = QTDepartmentTable()
        self.departments_window.show()

    def open_work_schedule_window(self):
        from design.table import QTWorkScheduleTable
        self.work_schedule_window = QTWorkScheduleTable()
        self.work_schedule_window.show()

    def open_rooms_window(self):
        from design.table import QTHotelRoomTable
        self.rooms_window = QTHotelRoomTable()
        self.rooms_window.show()

    def open_room_types_window(self):
        from design.table import QTRoomTypeTable
        self.room_types_window = QTRoomTypeTable()
        self.room_types_window.show()
