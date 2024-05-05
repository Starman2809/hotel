from abc import abstractmethod
from typing import List, Dict

from utils.utils import convert_number_to_status


class Serializer:
    @abstractmethod
    def get_values_in_order(self, object_id=None) -> tuple:
        """

        :param object_id: Needed for update object by id in database
        :return: tuple of object's data
        """
        pass

    @classmethod
    def get_all_as_dict(cls, rows) -> Dict:
        result = {}
        for row in rows:
            result[row[0]] = row[1]

        return result


class ClientDataSerializer(Serializer):
    def __init__(
            self,
            first_name_text: str,
            last_name_text: str,
            patronymic_text: str,
            birthday_date: str,
            email_text: str,
            phone_number_text: str,
            passport_number_text: str,
    ):
        """
        Класс, который конвертирует данные из формы в нужный формат,
        для сохранения в БД.


        :param first_name_text: Имя клиента
        :param last_name_text: Фамилия клиента
        :param patronymic_text: Отчество клиента
        :param email_text: Электронная почта клиента
        :param phone_number_text: Номер телефона клиента
        :param passport_number_text: Номер паспорта клиента
        """
        # TODO: Также выполняет валидацию
        self.first_name = first_name_text
        self.last_name = last_name_text
        self.patronymic = patronymic_text
        self.birthday_date = birthday_date
        self.email = email_text
        self.phone_number = phone_number_text
        self.passport_number_text = passport_number_text

    @staticmethod
    def prepare_data_to_print(client_rows):
        result = []
        # TODO: use keywords instead of number when parsing data from DB
        for row in client_rows:
            client_info_dict = {
                "id": row[0],
                "last_name": row[1],
                "first_name": row[2],
                "patronymic": row[3],
                "birthday_date": row[4],
                "email": row[5],
                "phone_number": row[6],
                "passport_number": row[7],
            }
            result.append(client_info_dict)
        return result

    @staticmethod
    def extract_full_names(clients_rows) -> List[str]:
        result = []
        for row in clients_rows:
            full_name = "{} {} {}".format(row[1], row[2], row[3])
            result.append(full_name)
        return result

    def get_values_in_order(self, object_id=None) -> tuple:
        if object_id is not None:
            return tuple([self.first_name, self.last_name, self.patronymic, self.birthday_date,
                          self.email, self.phone_number, self.passport_number_text, object_id])
        return tuple([self.first_name, self.last_name, self.patronymic, self.birthday_date,
                      self.email, self.phone_number, self.passport_number_text])

    @classmethod
    def get_all_as_dict(cls, rows) -> Dict:
        result = {}
        for row in rows:
            result[row[0]] = "{} {} {}".format(row[1], row[2], row[3])

        return result

class EmployeeSerializer(Serializer):

    def __init__(
            self,
            first_name_text: str,
            last_name_text: str,
            patronymic_text: str,
            birthday_date: str,
            passport_number_text: str,
            email_text: str,
            phone_number_text: str,
            job_position_text: str,
            hiring_date_text: str,
            salary_text: str,
            department_text: str,
            work_schedule_text: str,
            work_status_text: str,
    ):
        """
        Класс, который конвертирует данные из формы в нужный формат,
        для сохранения в БД.

        :param first_name_text:
        :param last_name_text:
        :param patronymic_text:
        :param birthday_date:
        :param passport_number_text:
        :param email_text:
        :param phone_number_text:
        :param job_position_text:
        :param hiring_date_text:
        :param salary_text:
        :param department_text:
        :param work_schedule_text:
        :param work_status_text:
        """

        # TODO: Также выполняет валидацию

        self.first_name = first_name_text
        self.last_name = last_name_text
        self.patronymic = patronymic_text
        self.birthday_date = birthday_date
        self.passport_number = passport_number_text
        self.email = email_text
        self.phone_number = phone_number_text
        self.job_position = job_position_text
        self.hiring_date = hiring_date_text
        self.salary = float(salary_text)
        self.department = department_text
        self.work_schedule = work_schedule_text
        self.work_status = work_status_text

    @staticmethod
    def prepare_data_to_print(employee_rows) -> List:
        result = []
        # TODO: use keywords instead of number when parsing data from DB
        for row in employee_rows:
            client_info_dict = {
                "id": row[0],
                "last_name": row[1],
                "first_name": row[2],
                "patronymic": row[3],
                "birthday_date": row[4],
                "passport_number": row[5],
                "job_position": row[6],
                "email": row[7],
                "phone_number": row[8],
                "hiring_date": row[9],
                "salary": row[10],
                "department": row[11],
                "work_schedule": row[12],
                "work_status": row[13],
            }
            result.append(client_info_dict)

        return result

    @classmethod
    def get_all_as_dict(cls, rows) -> Dict:
        result = {}
        for row in rows:
            result[row[0]] = f"{row[1]} {row[2]} {row[3]}"

        return result

    def get_values_in_order(self, object_id=None) -> tuple:
        if object_id is not None:
            return tuple([self.last_name, self.first_name, self.patronymic, self.birthday_date,
                          self.passport_number, self.job_position, self.email, self.phone_number,
                          self.hiring_date, self.salary, self.department, self.work_schedule,
                          self.work_status, object_id])
        return tuple([self.last_name, self.first_name, self.patronymic, self.birthday_date,
                      self.passport_number, self.job_position, self.email, self.phone_number,
                      self.hiring_date, self.salary, self.department, self.work_schedule,
                      self.work_status])


class JobPositionSerializer(Serializer):
    def __init__(self, job_title):
        self.job_title = job_title

    @classmethod
    def get_all_as_dict(cls, rows) -> Dict:
        result = {}
        for row in rows:
            result[row[0]] = row[1]

        return result

    def get_values_in_order(self, object_id=None) -> tuple:
        if object_id is not None:
            return tuple([self.job_title, object_id])
        return tuple([self.job_title])

    @staticmethod
    def prepare_data_to_print(job_position_rows):
        result = []
        # TODO: use keywords instead of number when parsing data from DB
        for row in job_position_rows:
            job_position_info_dict = {
                "id": row[0],
                "job_title": row[1],
            }
            result.append(job_position_info_dict)
        return result


class DepartmentSerializer(Serializer):
    def __init__(self, department_title):
        self.department_title = department_title

    def get_values_in_order(self, object_id=None) -> tuple:
        if object_id is not None:
            return tuple([self.department_title, object_id])
        return tuple([self.department_title])

    @classmethod
    def get_all_as_dict(cls, rows) -> Dict:
        result = {}
        for row in rows:
            result[row[0]] = row[1]

        return result

    @staticmethod
    def prepare_data_to_print(department_rows):
        result = []
        # TODO: use keywords instead of number when parsing data from DB
        for row in department_rows:
            department_info_dict = {
                "id": row[0],
                "department_title": row[1],
            }
            result.append(department_info_dict)
        return result


class WorkScheduleSerializer(Serializer):
    def __init__(self, work_schedule_title):
        self.work_schedule_title = work_schedule_title

    @staticmethod
    def prepare_data_to_print(work_schedule_rows):
        result = []
        # TODO: use keywords instead of number when parsing data from DB
        for row in work_schedule_rows:
            work_schedule_info_dict = {
                "id": row[0],
                "work_schedule_title": row[1],
            }
            result.append(work_schedule_info_dict)
        return result

    @classmethod
    def get_all_as_dict(cls, rows) -> Dict:
        result = {}
        for row in rows:
            result[row[0]] = row[1]

        return result

    def get_values_in_order(self, object_id=None) -> tuple:
        if object_id is not None:
            return tuple([self.work_schedule_title, object_id])
        return tuple([self.work_schedule_title])


class HotelRoomSerializer(Serializer):
    def __init__(
            self,
            employee_id: int,
            room_type_id: int,
    ):
        self.employee_id = employee_id
        self.room_type_id = room_type_id
        self.status = True

    @staticmethod
    def prepare_data_to_print(hotel_room_rows) -> List:
        result = []
        # TODO: use keywords instead of number when parsing data from DB
        for row in hotel_room_rows:
            hotel_room_info_dict = {
                "id": row[0],
                "employee_full_name": f"{row[1]} {row[2]} {row[3]}",
                "room_type_name": row[4],
                "room_type_description": row[5],
                "room_type_price": row[6],
                "active": convert_number_to_status(row[7]),
            }
            result.append(hotel_room_info_dict)

        return result

    @staticmethod
    def prepare_data_for_edit_form(hotel_room_rows) -> List:
        result = []
        # TODO: use keywords instead of number when parsing data from DB
        for row in hotel_room_rows:
            hotel_room_info_dict = {
                "id": row[0],
                "employee_id": row[1],
                "room_type_id": row[2],
            }
            result.append(hotel_room_info_dict)

        return result

    def get_values_in_order(self, object_id=None) -> tuple:
        if object_id is not None:
            return tuple([self.employee_id, self.room_type_id, self.status, object_id])
        return tuple([self.employee_id, self.room_type_id, self.status])


class RoomTypeSerializer(Serializer):
    def __init__(self, title, description, price):
        self.title = title
        self.description = description
        self.price = float(price)

    @classmethod
    def get_all_as_dict(cls, rows) -> Dict:
        result = {}
        for row in rows:
            result[row[0]] = row[1]

        return result

    @staticmethod
    def prepare_data_to_print(room_type_rows) -> List:
        result = []
        # TODO: use keywords instead of number when parsing data from DB
        for row in room_type_rows:
            room_type_info_dict = {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "price": row[3],
            }
            result.append(room_type_info_dict)

        return result

    def get_values_in_order(self, object_id=None) -> tuple:
        if object_id is not None:
            return tuple([self.title, self.description, self.price, object_id])
        return tuple([self.title, self.description, self.price])


class BookingSerializer(Serializer):
    def __init__(self, room_id, date_from, date_to, booking_date, payment_type, client, payment_status, final_price):
        self.room_id = int(room_id)
        self.date_from = date_from
        self.date_to = date_to
        self.booking_date = booking_date
        self.payment_type = int(payment_type)
        self.client = int(client)
        self.payment_status = payment_status
        self.final_price = float(final_price)

    @staticmethod
    def prepare_data_to_print(booking_rows) -> List:
        result = []
        # TODO: use keywords instead of number when parsing data from DB
        for row in booking_rows:
            booking_info_dict = {
                "id": row[0],
                "room_id": row[1],
                "date_from": row[2],
                "date_to": row[3],
                "creation_date": row[4],
                "payment_type": row[5],
                "client": row[6],
                "payment_status": row[7],
                "final_price": row[8],
                "employee_full_name": "{} {} {}".format(row[9], row[10], row[11]),
                "client_full_name": "{} {} {}".format(row[12], row[13], row[14]),
                "payment_type_description": row[15]
            }
            result.append(booking_info_dict)

        return result

    def get_values_in_order(self, object_id=None) -> tuple:
        if object_id is not None:
            return tuple([self.room_id, self.date_from, self.date_to, self.booking_date, self.payment_type, self.client, self.payment_status, self.final_price, object_id])
        return tuple([self.room_id, self.date_from, self.date_to, self.booking_date, self.payment_type, self.client, self.payment_status, self.final_price])


class PaymentTypeSerializer(Serializer):
    def __init__(self, description):
        self.description = description

    @staticmethod
    def prepare_data_to_print(payment_type_rows) -> List:
        result = []
        # TODO: use keywords instead of number when parsing data from DB
        for row in payment_type_rows:
            payment_type_info_dict = {
                "id": row[0],
                "description": row[1],
            }
            result.append(payment_type_info_dict)

        return result

    def get_values_in_order(self, object_id=None) -> tuple:
        if object_id is not None:
            return tuple([self.description, object_id])
        return tuple([self.description])
