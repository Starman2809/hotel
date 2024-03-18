from contants import DB_PATH
from db.manager import DatabaseManager
from serializers import ClientDataSerializer


class HotelRoom:
    pass


class RoomType:
    pass


class Client:
    id = None
    first_name = None
    last_name = None
    patronymic = None
    email = None
    phone = None
    passport_number = None

    database_manager = DatabaseManager(DB_PATH)

    @classmethod
    def get_all_clients(cls):
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Клиенты ORDER BY Фамилия ASC")

        rows = cursor.fetchall()

        cls.database_manager.close()

        return rows

    @classmethod
    def create_client(cls, serialized_client: ClientDataSerializer):
        cls.database_manager.connect()

        connection = cls.database_manager.connection
        cursor = connection.cursor()

        query_string = """INSERT INTO Клиенты ([Фамилия], [Имя], [Отчество], [Электронная почта], [Номер телефона], [Номер паспорта]) VALUES (?,?,?,?,?,?)"""
        values = (
            serialized_client.first_name,
            serialized_client.last_name,
            serialized_client.patronymic,
            serialized_client.email,
            serialized_client.phone_number,
            serialized_client.passport_number_text,
        )
        cursor.execute(query_string, values)

        connection.commit()

        cursor.close()

        cls.database_manager.close()


class Booking:
    pass


class Payment:
    pass


class Employees:
    id = None
    first_name = None
    last_name = None
    patronymic = None
    job_type = None
    email = None
    phone = None
    hiring_date = None
    salary = None
    department = None
    work_schedule = None
    work_status = None


class JobType:
    pass


class WorkScheduleType:
    pass


class Department:
    pass


class AdditionalService:
    pass
