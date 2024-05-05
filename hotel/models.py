from abc import ABC
from typing import List
from config.settings import DB_PATH
from db.manager import DatabaseManager
from db.serializers import (ClientDataSerializer, JobPositionSerializer, DepartmentSerializer, WorkScheduleSerializer,
                            EmployeeSerializer, Serializer, RoomTypeSerializer,
                            PaymentTypeSerializer)


class DBObject(ABC):
    database_manager = DatabaseManager(DB_PATH)

    query_string_create = ""
    query_string_list = ""
    query_string_get = ""
    query_string_update = ""
    query_string_delete = ""

    @classmethod
    def create(cls, serialized_object: Serializer):
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()

        values = serialized_object.get_values_in_order()

        cursor.execute(cls.query_string_create, values)

        connection.commit()

        cursor.close()
        cls.database_manager.close()

    @classmethod
    def all(cls):
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()
        cursor.execute(cls.query_string_list)

        rows = cursor.fetchall()

        cursor.close()
        cls.database_manager.close()

        return rows

    @classmethod
    def get(cls, object_id: int):
        cls.database_manager.connect()
        connection = cls.database_manager.connection
        cursor = connection.cursor()
        cursor.execute(cls.query_string_get, (object_id,))
        row = cursor.fetchone()
        cursor.close()
        cls.database_manager.close()

        return row

    @classmethod
    def update(cls, object_id: int, serialized_object: Serializer):
        cls.database_manager.connect()
        connection = cls.database_manager.connection
        cursor = connection.cursor()
        values = serialized_object.get_values_in_order(object_id)
        cursor.execute(cls.query_string_update, values)
        connection.commit()
        cursor.close()
        cls.database_manager.close()

    @classmethod
    def delete(cls, object_id: int):
        cls.database_manager.connect()
        connection = cls.database_manager.connection
        cursor = connection.cursor()
        cursor.execute(cls.query_string_delete, (object_id,))
        connection.commit()
        cursor.close()
        cls.database_manager.close()


class Client(DBObject):
    id = None
    first_name = None
    last_name = None
    patronymic = None
    birthday_date = None
    email = None
    phone = None
    passport_number = None

    query_string_create = "INSERT INTO [Клиенты] ([Имя], [Фамилия], [Отчество], [Дата Рождения], [Электронная почта], [Номер телефона], [Номер паспорта]) VALUES (?,?,?,?,?,?,?)"
    query_string_list = "SELECT * FROM [Клиенты] ORDER BY Фамилия ASC"
    query_string_get = "SELECT * FROM [Клиенты] WHERE id = ?"
    query_string_update = "UPDATE [Клиенты] SET [Имя] = ?,  [Фамилия] = ?, [Отчество] = ?, [Дата Рождения] = ?, [Электронная почта] = ?, [Номер телефона] = ?, [Номер паспорта] = ? WHERE id = ?"
    query_string_delete = "DELETE FROM [Клиенты] WHERE id = ?"

    @classmethod
    def all_as_dict(cls):
        cls.database_manager.connect()
        connection = cls.database_manager.connection
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM [Клиенты] ORDER BY id ASC")
        rows = cursor.fetchall()
        cursor.close()
        cls.database_manager.close()

        return ClientDataSerializer.get_all_as_dict(rows)

class Employee(DBObject):
    id = None
    first_name = None
    last_name = None
    patronymic = None
    birthday_date = None
    passport_number = None
    email = None
    phone = None
    job_position = None
    hiring_date = None
    salary = None
    department = None
    work_schedule = None
    work_status = None

    query_string_create = "INSERT INTO Персонал ([Фамилия], [Имя], [Отчество], [Дата Рождения], [Номер Паспорта], [Должность], [Электронная почта], [Номер телефона], [Дата Найма], [Зарплата], [Отдел], [График Работы], [Статус]) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"
    query_string_list = "SELECT [Персонал].[id], [Персонал].[Фамилия], [Персонал].[Имя], [Персонал].[Отчество], [Персонал].[Дата рождения], [Персонал].[Номер Паспорта], [Должности].[Название], [Персонал].[Электронная почта], [Персонал].[Номер телефона], [Персонал].[Дата найма], [Персонал].[Зарплата], [Отделы].[Название], [График работы].[Название], [Персонал].[Статус] FROM (([Персонал] LEFT JOIN [Отделы] ON ([Персонал].[Отдел] = [Отделы].[id])) LEFT JOIN [Должности] ON ([Персонал].[Должность] = [Должности].[id])) LEFT JOIN [График работы] ON ([Персонал].[График работы] = [График работы].[id]) ORDER BY [Персонал].[id] ASC"
    query_string_get = "SELECT * FROM [Персонал] WHERE id = ?"
    query_string_update = "UPDATE Персонал SET [Фамилия] = ?, [Имя] = ?, [Отчество] = ?, [Дата Рождения] = ?, [Номер Паспорта] = ?, [Должность] = ?, [Электронная почта] = ?, [Номер телефона] = ?, [Дата Найма] = ?, [Зарплата] = ?, [Отдел] = ?, [График Работы] = ?, [Статус] = ? WHERE id = ?"
    query_string_delete = "DELETE FROM [Персонал] WHERE id = ?"


    @classmethod
    def all_as_dict(cls):
        return EmployeeSerializer.get_all_as_dict(cls.all())


class JobPosition(DBObject):
    id = None
    title = None

    query_string_create = "INSERT INTO [Должности] ([Название]) VALUES (?)"
    query_string_list = "SELECT * FROM [Должности] ORDER BY [Название] ASC"
    query_string_get = "SELECT * FROM [Должности] WHERE id = ?"
    query_string_update = "UPDATE [Должности] SET [Название] = ? WHERE id = ?"
    query_string_delete = "DELETE FROM [Должности] WHERE id = ?"

    @classmethod
    def all_as_dict(cls):
        cls.database_manager.connect()
        connection = cls.database_manager.connection
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM [Должности] ORDER BY id ASC")
        rows = cursor.fetchall()
        cursor.close()
        cls.database_manager.close()

        return JobPositionSerializer.get_all_as_dict(rows)


class Department(DBObject):
    id = None
    description = None

    query_string_create = """INSERT INTO [Отделы] ([Название]) VALUES (?)"""
    query_string_list = """SELECT * FROM [Отделы] ORDER BY [id] ASC"""
    query_string_get = """SELECT * FROM [Отделы] WHERE id = ?"""
    query_string_update = """UPDATE [Отделы] SET [Название] = ? WHERE id = ?"""
    query_string_delete = """DELETE FROM [Отделы] WHERE id = ?"""

    @classmethod
    def all_as_dict(cls):
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Отделы ORDER BY id ASC")

        rows = cursor.fetchall()

        cursor.close()
        cls.database_manager.close()

        return DepartmentSerializer.get_all_as_dict(rows)


class WorkSchedule(DBObject):
    id = None
    description = None

    query_string_create = """INSERT INTO [График работы] ([Название]) VALUES (?)"""
    query_string_list = """SELECT * FROM [График работы] ORDER BY [id] ASC"""
    query_string_get = """SELECT * FROM [График работы] WHERE id = ?"""
    query_string_update = """UPDATE [График работы] SET [Название] = ? WHERE id = ?"""
    query_string_delete = """DELETE FROM [График работы] WHERE id = ?"""

    @classmethod
    def all_as_dict(cls):
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM [График работы] ORDER BY id ASC")

        rows = cursor.fetchall()

        cursor.close()
        cls.database_manager.close()

        return WorkScheduleSerializer.get_all_as_dict(rows)


class HotelRoom(DBObject):
    id = None
    employee = None
    room_type = None
    # Доступна ли комната для использования или нет впринципе, мб ее закрыли на ремонт и ее нельзя бронировать впринципе
    status = True

    query_string_create = "INSERT INTO [Гостиничные номера] ([Сотрудник], [Категория], [Статус]) VALUES (?,?,?)"
    query_string_list = "SELECT [Гостиничные номера].[id], [Персонал].[Фамилия], [Персонал].[Имя], [Персонал].[Отчество], [Категории Номеров].[Название], [Категории Номеров].[Описание], [Категории Номеров].[Стоимость], [Гостиничные номера].[Статус] FROM ([Гостиничные номера] LEFT JOIN [Персонал] ON [Гостиничные номера].[Сотрудник] = [Персонал].[id]) LEFT JOIN [Категории номеров] ON [Гостиничные номера].[Категория] = [Категории номеров].[id] ORDER BY [Гостиничные номера].[id] ASC"
    query_string_get = "SELECT * FROM [Гостиничные номера] WHERE id = ?"
    query_string_update = "UPDATE [Гостиничные номера] SET [Сотрудник] = ?, [Категория] = ?, [Статус] = ? WHERE id = ?"
    query_string_delete = "DELETE FROM [Гостиничные номера] WHERE id = ?"

    @classmethod
    def deactivate(cls, room_id: int):
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()

        query_string = f"""UPDATE [Гостиничные Номера] SET [Статус] = False WHERE id = ?"""

        values = (
            room_id,
        )
        cursor.execute(query_string, values)

        connection.commit()

        cursor.close()
        cls.database_manager.close()

    @classmethod
    def activate(cls, room_id: int):
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()

        query_string = f"""UPDATE [Гостиничные Номера] SET [Статус] = True WHERE id = ?"""

        values = (
            room_id,
        )
        cursor.execute(query_string, values)

        connection.commit()

        cursor.close()
        cls.database_manager.close()

    @classmethod
    def get_available_rooms(cls, date_from, date_to) -> List:
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()
        query_string = """SELECT [Гостиничные номера].[id], [Персонал].[Фамилия], [Персонал].[Имя], [Персонал].[Отчество], [Категории Номеров].[Название], [Категории Номеров].[Описание], [Категории Номеров].[Стоимость], [Гостиничные номера].[Статус] FROM ([Гостиничные номера] LEFT JOIN [Персонал] ON [Гостиничные номера].[Сотрудник] = [Персонал].[id]) LEFT JOIN [Категории номеров] ON [Гостиничные номера].[Категория] = [Категории номеров].[id] WHERE [Гостиничные номера].[id] NOT IN (SELECT room_id FROM [Бронирование] WHERE [Дата приезда] <= ? AND [Дата отъезда] >= ?) ORDER BY [Гостиничные номера].[id] ASC"""
        values = (
            date_to,
            date_from
        )
        cursor.execute(query_string, values)

        row = cursor.fetchall()

        cursor.close()
        cls.database_manager.close()

        return row


class RoomType(DBObject):
    id = None
    title = None
    description = None
    price = None

    query_string_create = """INSERT INTO [Категории номеров] ([Название], [Описание], [Стоимость]) VALUES (?,?,?)"""
    query_string_list = """SELECT * FROM [Категории номеров] ORDER BY [id] ASC"""
    query_string_get = """SELECT * FROM [Категории номеров] WHERE [id] = ?"""
    query_string_update = """UPDATE [Категории номеров] SET [Название] = ?,  [Описание] = ?, [Стоимость] = ? WHERE [id] = ?"""
    query_string_delete = """DELETE FROM [Категории номеров] WHERE [id] = ?"""

    @classmethod
    def all_as_dict(cls):
        return RoomTypeSerializer.get_all_as_dict(cls.all())


class Booking(DBObject):
    query_string_create = "INSERT INTO [Бронирование] ([room_id], [Дата приезда], [Дата отъезда], [Дата бронирования], [Форма оплаты], [Клиент], [Статус оплаты], [Итоговая стоимость]) VALUES (?,?,?,?,?,?,?,?)"
    query_string_list = "SELECT [Бронирование].*, [Персонал].[Фамилия], [Персонал].[Имя], [Персонал].[Отчество], [Клиенты].[Фамилия], [Клиенты].[Имя], [Клиенты].[Отчество], [Форма оплаты].[Описание оплаты] FROM ((([Бронирование] LEFT JOIN [Гостиничные номера] ON [Бронирование].[room_id] = [Гостиничные номера].[id]) LEFT JOIN [Персонал] ON [Гостиничные номера].[Сотрудник] = [Персонал].[id]) LEFT JOIN [Клиенты] ON [Бронирование].[Клиент] = [Клиенты].[id]) LEFT JOIN [Форма оплаты] ON [Бронирование].[Форма оплаты] = [Форма оплаты].[id] ORDER BY [Бронирование].[id] DESC"
    query_string_get = "SELECT [Бронирование].*, [Персонал].[Фамилия], [Персонал].[Имя], [Персонал].[Отчество], [Клиенты].[Фамилия], [Клиенты].[Имя], [Клиенты].[Отчество], [Форма оплаты].[Описание оплаты] FROM ((([Бронирование] LEFT JOIN [Гостиничные номера] ON [Бронирование].[room_id] = [Гостиничные номера].[id]) LEFT JOIN [Персонал] ON [Гостиничные номера].[Сотрудник] = [Персонал].[id]) LEFT JOIN [Клиенты] ON [Бронирование].[Клиент] = [Клиенты].[id]) LEFT JOIN [Форма оплаты] ON [Бронирование].[Форма оплаты] = [Форма оплаты].[id] WHERE [Бронирование].[id] = ?"
    query_string_update = "UPDATE [Бронирование] SET [room_id] = ?, [Дата приезда] = ?, [Дата отъезда] = ?, [Дата бронирования] = ?, [Форма оплаты] = ?, [Клиент] = ?, [Статус оплаты] = ?, [Итоговая стоимость] = ? WHERE id = ?"
    query_string_delete = "DELETE FROM [Бронирование] WHERE id = ?"

    @classmethod
    def search_booking(cls, input_data) -> List:
        where_query_part = ""
        list_of_search_queries = []
        if input_data["use_selected_date"] is True:
            date = input_data["date"].selectedDate().toPyDate()
            list_of_search_queries.append(f"([Бронирование].[Дата приезда] <= #{date}# AND [Бронирование].[Дата отъезда] >= #{date}#)")
            where_query_part = " WHERE "
        if input_data["client"].text() != "":
            client = input_data["client"].text()
            list_of_search_queries.append(f"([Клиенты].[Фамилия] LIKE '{client}%')")
            where_query_part = " WHERE "
        if input_data["room_type"].currentData() != "":
            room_type = input_data["room_type"].currentData()
            list_of_search_queries.append(f"([Гостиничные номера].[Категория] = {room_type})")
            where_query_part = " WHERE "

        where_query_final_part = where_query_part + " AND ".join(list_of_search_queries)

        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()

        query_string = "SELECT [Бронирование].*, [Персонал].[Фамилия], [Персонал].[Имя], [Персонал].[Отчество], [Клиенты].[Фамилия], [Клиенты].[Имя], [Клиенты].[Отчество], [Форма оплаты].[Описание оплаты] FROM ((([Бронирование] LEFT JOIN [Гостиничные номера] ON [Бронирование].[room_id] = [Гостиничные номера].[id]) LEFT JOIN [Персонал] ON [Гостиничные номера].[Сотрудник] = [Персонал].[id]) LEFT JOIN [Клиенты] ON [Бронирование].[Клиент] = [Клиенты].[id]) LEFT JOIN [Форма оплаты] ON [Бронирование].[Форма оплаты] = [Форма оплаты].[id]" + where_query_final_part

        cursor.execute(query_string)

        row = cursor.fetchall()

        cursor.close()
        cls.database_manager.close()

        return row

class PaymentType(DBObject):
    query_string_create = "INSERT INTO [Форма оплаты] ([Описание оплаты]) VALUES (?)"
    query_string_list = "SELECT * FROM [Форма оплаты] ORDER BY id ASC"
    query_string_get = "SELECT * FROM [Форма оплаты] WHERE id = ?"
    query_string_update = "UPDATE [Форма оплаты] SET [Описание оплаты] = ? WHERE id = ?"
    query_string_delete = "DELETE FROM [Форма оплаты] WHERE [id] = ?"

    @classmethod
    def all_as_dict(cls):
        cls.database_manager.connect()
        connection = cls.database_manager.connection
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM [Форма оплаты] ORDER BY id ASC")
        rows = cursor.fetchall()
        cursor.close()
        cls.database_manager.close()

        return PaymentTypeSerializer.get_all_as_dict(rows)


class Auth:
    database_manager = DatabaseManager(DB_PATH)

    @classmethod
    def is_user_in_db(cls, username, password):
        cls.database_manager.connect()
        connection = cls.database_manager.connection
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM [Администраторы]")
        columns = [column[0] for column in cursor.description]
        rows_as_dict = [dict(zip(columns, row)) for row in cursor.fetchall()]

        cursor.close()
        cls.database_manager.close()

        for item in rows_as_dict:
            if item["Login"] == username and item["password"] == password:
                return True

        return False