from typing import List, Dict

from utils.utils import insert_new_lines, convert_number_to_status


class BaseSerializer:
    pass


class ClientDataSerializer(BaseSerializer):
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


class EmployeeSerializer(BaseSerializer):

    def __init__(
            self,
            first_name_text: str,
            last_name_text: str,
            patronymic_text: str,
            birthday_date: str,
            passport_number_text: str,
            email_text: str,
            phone_number_text: str,
            job_type_text: str,
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
        :param job_type_text:
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
        self.job_type = job_type_text
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
                "job_type": row[6],
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


class JobTypeSerializer(BaseSerializer):

    @classmethod
    def get_all_as_dict(cls, rows) -> Dict:
        result = {}
        for row in rows:
            result[row[0]] = row[1]
        return result


class DepartmentSerializer(BaseSerializer):

    @classmethod
    def get_all_as_dict(cls, rows) -> Dict:
        result = {}
        for row in rows:
            result[row[0]] = row[1]
        return result


class WorkScheduleSerializer(BaseSerializer):

    @classmethod
    def get_all_as_dict(cls, rows) -> Dict:
        result = {}
        for row in rows:
            result[row[0]] = row[1]
        return result


class HotelRoomSerializer(BaseSerializer):
    def __init__(
        self,
        employee_id: int,
        room_type_id: int,
    ):
        self.employee_id = employee_id
        self.room_type_id = room_type_id

    @staticmethod
    def prepare_data_to_print(hotel_room_rows) -> List:
        result = []
        # TODO: use keywords instead of number when parsing data from DB
        for row in hotel_room_rows:
            hotel_room_info_dict = {
                "id": row[0],
                "employee_full_name": f"{row[1]} {row[2]} {row[3]}",
                "room_type_name": row[4],
                "room_type_description": insert_new_lines(row[5], 40),
                "room_type_price": row[6],
                "active": convert_number_to_status(row[7]),
            }
            result.append(hotel_room_info_dict)
        return result


class RoomTypeSerializer(BaseSerializer):
    @classmethod
    def get_all_as_dict(cls, rows) -> Dict:
        result = {}
        for row in rows:
            result[row[0]] = row[1]
        return result
