from abc import ABC, abstractmethod
from typing import List

from config.settings import DB_PATH
from db.manager import DatabaseManager
from db.serializers import (ClientDataSerializer, JobTypeSerializer, DepartmentSerializer, WorkScheduleSerializer,
                            EmployeeSerializer, BaseSerializer, HotelRoomSerializer, RoomTypeSerializer)


class DBObject(ABC):
    database_manager = DatabaseManager(DB_PATH)

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
    def get_client(cls, client_id: int):
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
    def update_client(cls, client_id: int, serialized_client: ClientDataSerializer):
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
    def delete_client(cls, client_id: int):
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()
        query_string = """DELETE FROM Клиенты WHERE id = ?"""
        cursor.execute(query_string, (client_id,))
        connection.commit()

        cursor.close()
        cls.database_manager.close()


class Booking:
    pass


class Payment:
    pass


class Employee(DBObject):
    id = None
    first_name = None
    last_name = None
    patronymic = None
    birthday_date = None
    passport_number = None
    email = None
    phone = None
    job_type = None
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
            serialized_client.job_type,
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
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()
        cursor.execute("SELECT [Персонал].[id], [Персонал].[Фамилия], [Персонал].[Имя], [Персонал].[Отчество], [Персонал].[Дата рождения], [Персонал].[Номер Паспорта], [Должности].[Описание], [Персонал].[Электронная почта], [Персонал].[Номер Телефона], [Персонал].[Дата найма], [Персонал].[Зарплата], [Отделы].[Описание], [График работы].[Описание], [Персонал].[Статус] FROM (([Персонал] LEFT JOIN [Отделы] ON ([Персонал].[Отдел] = [Отделы].[id])) LEFT JOIN [Должности] ON ([Персонал].[Должность] = [Должности].[id])) LEFT JOIN [График работы] ON ([Персонал].[График работы] = [График работы].[id]) ORDER BY [Персонал].[id] ASC")
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
            serialized_employee.job_type,
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


class JobType(DBObject):
    id = None
    description = None


    @classmethod
    def all_as_dict(cls):
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Должности ORDER BY id ASC")

        rows = cursor.fetchall()

        cursor.close()
        cls.database_manager.close()

        return JobTypeSerializer.get_all_as_dict(rows)


class Department(DBObject):
    id = None
    description = None

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

    @classmethod
    def all(cls):
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()
        cursor.execute("SELECT [Гостиничные номера].[id], [Персонал].[Фамилия], [Персонал].[Имя], [Персонал].[Отчество], [Категории Номеров].[Имя], [Категории Номеров].[Описание], [Категории Номеров].[Стоимость], [Гостиничные номера].[Статус] FROM ([Гостиничные номера] LEFT JOIN [Персонал] ON [Гостиничные номера].[Сотрудник] = [Персонал].[id]) LEFT JOIN [Категории номеров] ON [Гостиничные номера].[Категория] = [Категории номеров].[id] ORDER BY [Гостиничные номера].[id] ASC")

        rows = cursor.fetchall()

        cls.database_manager.close()

        return rows

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

class RoomType(DBObject):
    @classmethod
    def all(cls):
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM [Категории номеров] ORDER BY id ASC")

        rows = cursor.fetchall()

        cls.database_manager.close()

        return rows

    @classmethod
    def all_as_dict(cls):
        return RoomTypeSerializer.get_all_as_dict(cls.all())


class AdditionalService:
    pass
