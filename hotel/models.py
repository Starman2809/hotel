from abc import ABC, abstractmethod
from typing import List

from config.settings import DB_PATH
from db.manager import DatabaseManager
from db.serializers import (ClientDataSerializer, JobPositionSerializer, DepartmentSerializer, WorkScheduleSerializer,
                            EmployeeSerializer, Serializer, HotelRoomSerializer, RoomTypeSerializer,
                            AdditionalServiceSerializer)


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

    # @classmethod
    # @abstractmethod
    # def create(cls, serialized_object: BaseSerializer):
    #     pass


class Client(DBObject):
    id = None
    first_name = None
    last_name = None
    patronymic = None
    birthday_date = None
    email = None
    phone = None
    passport_number = None

    @classmethod
    def all(cls):
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Клиенты ORDER BY Фамилия ASC")

        rows = cursor.fetchall()

        cls.database_manager.close()

        return rows

    @classmethod
    def create(cls, serialized_client: ClientDataSerializer):
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()

        query_string = """INSERT INTO Клиенты ([Имя], [Фамилия], [Отчество], [Дата Рождения], [Электронная почта], [Номер телефона], [Номер паспорта]) VALUES (?,?,?,?,?,?,?)"""
        values = (
            serialized_client.first_name,
            serialized_client.last_name,
            serialized_client.patronymic,
            serialized_client.birthday_date,
            serialized_client.email,
            serialized_client.phone_number,
            serialized_client.passport_number_text,
        )
        cursor.execute(query_string, values)

        connection.commit()

        cursor.close()
        cls.database_manager.close()

    @classmethod
    def get(cls, client_id: int):
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()
        query_string = """SELECT * FROM Клиенты WHERE id = ?"""
        cursor.execute(query_string, (client_id,))

        row = cursor.fetchone()

        cursor.close()
        cls.database_manager.close()

        return row

    @classmethod
    def update(cls, client_id: int, serialized_client: ClientDataSerializer):
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()

        query_string = f"""UPDATE Клиенты SET [Имя] = ?,  [Фамилия] = ?, [Отчество] = ?, [Дата Рождения] = ?, [Электронная почта] = ?, [Номер телефона] = ?, [Номер паспорта] = ? WHERE id = ?"""

        values = (
            serialized_client.first_name,
            serialized_client.last_name,
            serialized_client.patronymic,
            serialized_client.birthday_date,
            serialized_client.email,
            serialized_client.phone_number,
            serialized_client.passport_number_text,
            client_id,
        )
        cursor.execute(query_string, values)

        connection.commit()

        cursor.close()
        cls.database_manager.close()

    @classmethod
    def delete(cls, client_id: int):
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()
        query_string = """DELETE FROM Клиенты WHERE id = ?"""
        cursor.execute(query_string, (client_id,))
        connection.commit()

        cursor.close()
        cls.database_manager.close()


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

    @classmethod
    def create(cls, serialized_client: EmployeeSerializer):
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()

        query_string = """INSERT INTO Персонал ([Фамилия], [Имя], [Отчество], [Дата Рождения], [Номер Паспорта], [Должность], [Электронная почта], [Номер телефона], [Дата Найма], [Зарплата], [Отдел], [График Работы], [Статус]) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        values = (
            serialized_client.last_name,
            serialized_client.first_name,
            serialized_client.patronymic,
            serialized_client.birthday_date,
            serialized_client.passport_number,
            serialized_client.job_position,
            serialized_client.email,
            serialized_client.phone_number,
            serialized_client.hiring_date,
            serialized_client.salary,
            serialized_client.department,
            serialized_client.work_schedule,
            serialized_client.work_status,
        )
        cursor.execute(query_string, values)

        connection.commit()

        cursor.close()
        cls.database_manager.close()

    @classmethod
    def all(cls) -> List[str]:
        print(DB_PATH)

        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()
        cursor.execute("SELECT [Персонал].[id], [Персонал].[Фамилия], [Персонал].[Имя], [Персонал].[Отчество], [Персонал].[Дата рождения], [Персонал].[Номер Паспорта], [Должности].[Название], [Персонал].[Электронная почта], [Персонал].[Номер телефона], [Персонал].[Дата найма], [Персонал].[Зарплата], [Отделы].[Название], [График работы].[Название], [Персонал].[Статус] FROM (([Персонал] LEFT JOIN [Отделы] ON ([Персонал].[Отдел] = [Отделы].[id])) LEFT JOIN [Должности] ON ([Персонал].[Должность] = [Должности].[id])) LEFT JOIN [График работы] ON ([Персонал].[График работы] = [График работы].[id]) ORDER BY [Персонал].[id] ASC")
        rows = cursor.fetchall()

        cursor.close()
        cls.database_manager.close()

        return rows

    @classmethod
    def all_as_dict(cls):
        return EmployeeSerializer.get_all_as_dict(cls.all())

    @classmethod
    def get(cls, employee_id: int):
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()
        query_string = """SELECT * FROM Персонал WHERE id = ?"""
        cursor.execute(query_string, (employee_id,))

        row = cursor.fetchone()

        cursor.close()
        cls.database_manager.close()

        return row

    @classmethod
    def update(cls, employee_id: int, serialized_employee: EmployeeSerializer):

        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()

        query_string = """UPDATE Персонал SET [Фамилия] = ?, [Имя] = ?, [Отчество] = ?, [Дата Рождения] = ?, [Номер Паспорта] = ?, [Должность] = ?, [Электронная почта] = ?, [Номер телефона] = ?, [Дата Найма] = ?, [Зарплата] = ?, [Отдел] = ?, [График Работы] = ?, [Статус] = ? WHERE id = ?"""
        values = (
            serialized_employee.last_name,
            serialized_employee.first_name,
            serialized_employee.patronymic,
            serialized_employee.birthday_date,
            serialized_employee.passport_number,
            serialized_employee.job_position,
            serialized_employee.email,
            serialized_employee.phone_number,
            serialized_employee.hiring_date,
            serialized_employee.salary,
            serialized_employee.department,
            serialized_employee.work_schedule,
            serialized_employee.work_status,
            employee_id,
        )
        cursor.execute(query_string, values)

        connection.commit()

        cursor.close()
        cls.database_manager.close()

    @classmethod
    def delete(cls, employee_id: int):
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()
        query_string = """DELETE FROM Персонал WHERE id = ?"""
        cursor.execute(query_string, (employee_id,))
        connection.commit()

        cursor.close()
        cls.database_manager.close()


class JobPosition(DBObject):
    id = None
    title = None

    query_string_create = """INSERT INTO [Должности] ([Название]) VALUES (?)"""
    query_string_list = """SELECT * FROM [Должности] ORDER BY [Название] ASC"""
    query_string_get = """SELECT * FROM [Должности] WHERE id = ?"""
    query_string_update = """UPDATE [Должности] SET [Название] = ? WHERE id = ?"""
    query_string_delete = """DELETE FROM [Должности] WHERE id = ?"""


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

    query_string_list = """SELECT [Гостиничные номера].[id], [Персонал].[Фамилия], [Персонал].[Имя], [Персонал].[Отчество], [Категории Номеров].[Название], [Категории Номеров].[Описание], [Категории Номеров].[Стоимость], [Гостиничные номера].[Статус] FROM ([Гостиничные номера] LEFT JOIN [Персонал] ON [Гостиничные номера].[Сотрудник] = [Персонал].[id]) LEFT JOIN [Категории номеров] ON [Гостиничные номера].[Категория] = [Категории номеров].[id] ORDER BY [Гостиничные номера].[id] ASC"""

    @classmethod
    def create(cls, serialized_hotel_room: HotelRoomSerializer):
        cls.database_manager.connect()
        connection = cls.database_manager.connection
        cursor = connection.cursor()
        query_string = """INSERT INTO [Гостиничные номера] ([Сотрудник], [Категория], [Статус]) VALUES (?,?,?)"""
        values = (
            serialized_hotel_room.employee_id,
            serialized_hotel_room.room_type_id,
            True
        )
        cursor.execute(query_string, values)

        connection.commit()

        cursor.close()
        cls.database_manager.close()

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
    def get(cls, room_id: int):
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()
        query_string = """SELECT * FROM [Гостиничные номера] WHERE id = ?"""
        cursor.execute(query_string, (room_id,))

        row = cursor.fetchone()

        cursor.close()
        cls.database_manager.close()

        return row

    @classmethod
    def update(cls, hotel_room_id: int, serialized_hotel_room: HotelRoomSerializer):
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()

        query_string = """UPDATE [Гостиничные номера] SET [Сотрудник] = ?, [Категория] = ? WHERE id = ?"""
        values = (
            serialized_hotel_room.employee_id,
            serialized_hotel_room.room_type_id,
            hotel_room_id
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


class AdditionalServiceType(DBObject):
    query_string_list = "SELECT * FROM [Типы дополнительных услуг] ORDER BY id ASC"

    @classmethod
    def create(cls, serialized_hotel_room: AdditionalServiceSerializer):
        cls.database_manager.connect()
        connection = cls.database_manager.connection
        cursor = connection.cursor()
        query_string = """INSERT INTO [Типы дополнительных услуг] ([Название], [Описание], [Стоимость]) VALUES (?,?,?)"""
        values = (
            serialized_hotel_room.service_name,
            serialized_hotel_room.service_description,
            serialized_hotel_room.service_price
        )
        cursor.execute(query_string, values)

        connection.commit()

        cursor.close()
        cls.database_manager.close()

    @classmethod
    def delete(cls, service_id: int):
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()
        query_string = """DELETE FROM [Типы дополнительных услуг] WHERE id = ?"""
        cursor.execute(query_string, (service_id,))
        connection.commit()

        cursor.close()
        cls.database_manager.close()

    @classmethod
    def get(cls, service_id: int):
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()
        query_string = """SELECT * FROM [Типы дополнительных услуг] WHERE id = ?"""
        cursor.execute(query_string, (service_id,))

        row = cursor.fetchone()

        cursor.close()
        cls.database_manager.close()

        return row

    @classmethod
    def update(cls, service_id: int, serialized_service: AdditionalServiceSerializer):
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()

        query_string = """UPDATE [Типы дополнительных услуг] SET [Название] = ?,  [Описание] = ?, [Стоимость] = ? WHERE id = ?"""

        values = (
            serialized_service.service_name,
            serialized_service.service_description,
            serialized_service.service_price,
            service_id,
        )
        cursor.execute(query_string, values)

        connection.commit()

        cursor.close()
        cls.database_manager.close()


class Booking(DBObject):
    query_string_create = """INSERT INTO [Бронирование] ([Номер комнаты], [Дата приезда], [Дата отъезда], [Дата бронирования], [Форма оплаты], [Клиент], [Статус оплаты], [Итоговая стоимость]) VALUES (?,?,?,?,?,?,?,?)"""
    query_string_list = """SELECT [Бронирование].*, [Персонал].[Фамилия], [Персонал].[Имя], [Персонал].[Отчество] FROM ([Бронирование] LEFT JOIN [Гостиничные номера] ON [Бронирование].[room_id] = [Гостиничные номера].[id]) LEFT JOIN [Персонал] ON [Гостиничные номера].[Сотрудник] = [Персонал].[id] ORDER BY [Бронирование].room_id ASC"""


class PaymentType(DBObject):
    query_string_list = "SELECT * FROM [Форма оплаты] ORDER BY id ASC"