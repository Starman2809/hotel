from abc import ABC, abstractmethod

from db.serializers import ClientDataSerializer, EmployeeSerializer, HotelRoomSerializer, AdditionalServiceSerializer, \
    JobPositionSerializer, DepartmentSerializer, RoomTypeSerializer, WorkScheduleSerializer
from hotel.models import Client, Employee, HotelRoom, AdditionalServiceType, JobPosition, Department, RoomType, \
    WorkSchedule
from utils.utils import get_key_from_dict_by_value


class Controller(ABC):
    def __init__(self):
        self.entries = {}
        self.root = None

    def cleanup(self):
        """
        Method for deleting old values from memory after use
        """
        self.entries = {}

    @abstractmethod
    def submit_create(self):
        pass

    @abstractmethod
    def submit_update(self, object_id):
        pass


class ClientController(Controller):
    def submit_create(self):
        first_name_text = self.entries["first_name_entry"].get()
        last_name_text = self.entries["last_name_entry"].get()
        patronymic_text = self.entries["patronymic_entry"].get()
        birthday_date = self.entries["birthday_date_calendar"].selection_get()
        email_text = self.entries["email_entry"].get()
        phone_number_text = self.entries["phone_number_entry"].get()
        passport_number_text = self.entries["passport_number_entry"].get()

        serialized_client = ClientDataSerializer(
            first_name_text=first_name_text,
            last_name_text=last_name_text,
            patronymic_text=patronymic_text,
            birthday_date=birthday_date,
            email_text=email_text,
            phone_number_text=phone_number_text,
            passport_number_text=passport_number_text,
        )

        Client.create(serialized_client)

        self.cleanup()

    def submit_update(self, client_id):
        first_name_text = self.entries["first_name_entry"].get()
        last_name_text = self.entries["last_name_entry"].get()
        patronymic_text = self.entries["patronymic_entry"].get()
        birthday_date = self.entries["birthday_date_calendar"].selection_get()
        email_text = self.entries["email_entry"].get()
        phone_number_text = self.entries["phone_number_entry"].get()
        passport_number_text = self.entries["passport_number_entry"].get()

        serialized_client = ClientDataSerializer(
            first_name_text=first_name_text,
            last_name_text=last_name_text,
            patronymic_text=patronymic_text,
            birthday_date=birthday_date,
            email_text=email_text,
            phone_number_text=phone_number_text,
            passport_number_text=passport_number_text,
        )

        Client.update(client_id, serialized_client)

        self.cleanup()


class EmployeeController(Controller):
    def submit_create(self):

        job_position_id = get_key_from_dict_by_value(self.entries["job_position_list"], self.entries["job_position_combobox_selected_text"].get())
        department_type_id = get_key_from_dict_by_value(self.entries["department_list"], self.entries["department_type_combobox_selected_text"].get())
        work_schedule_type_id = get_key_from_dict_by_value(self.entries["work_schedule_list"], self.entries["work_schedule_combobox_selected_text"].get())

        first_name_text = self.entries["first_name_entry"].get()
        last_name_text = self.entries["last_name_entry"].get()
        patronymic_text = self.entries["patronymic_entry"].get()
        birthday_date = self.entries["birthday_date_calendar"].selection_get()
        passport_number_text = self.entries["passport_number_entry"].get()
        email_text = self.entries["email_entry"].get()
        phone_number_text = self.entries["phone_number_entry"].get()
        job_position_text = job_position_id
        hiring_date_text = self.entries["hiring_date_calendar"].selection_get()
        salary_text = self.entries["salary_entry"].get()
        department_text = department_type_id
        work_schedule_text = work_schedule_type_id
        work_status_text = self.entries["work_status_entry"].get()

        serialized_employee = EmployeeSerializer(
            first_name_text=first_name_text,
            last_name_text=last_name_text,
            patronymic_text=patronymic_text,
            birthday_date=birthday_date,
            passport_number_text=passport_number_text,
            email_text=email_text,
            phone_number_text=phone_number_text,
            job_position_text=job_position_text,
            hiring_date_text=hiring_date_text,
            salary_text=salary_text,
            department_text=department_text,
            work_schedule_text=work_schedule_text,
            work_status_text=work_status_text,
        )

        Employee.create(serialized_employee)

        self.cleanup()

    def submit_update(self, employee_id):
        job_position_id = get_key_from_dict_by_value(self.entries["job_position_list"], self.entries["job_position_combobox_selected_text"].get())
        department_type_id = get_key_from_dict_by_value(self.entries["department_list"], self.entries["department_type_combobox_selected_text"].get())
        work_schedule_type_id = get_key_from_dict_by_value(self.entries["work_schedule_list"], self.entries["work_schedule_combobox_selected_text"].get())

        first_name_text = self.entries["first_name_entry"].get()
        last_name_text = self.entries["last_name_entry"].get()
        patronymic_text = self.entries["patronymic_entry"].get()
        birthday_date = self.entries["birthday_date_calendar"].selection_get()
        passport_number_text = self.entries["passport_number_entry"].get()
        email_text = self.entries["email_entry"].get()
        phone_number_text = self.entries["phone_number_entry"].get()
        job_position_text = job_position_id
        hiring_date_text = self.entries["hiring_date_calendar"].selection_get()
        salary_text = self.entries["salary_entry"].get()
        department_text = department_type_id
        work_schedule_text = work_schedule_type_id
        work_status_text = self.entries["work_status_entry"].get()

        serialized_employee = EmployeeSerializer(
            first_name_text=first_name_text,
            last_name_text=last_name_text,
            patronymic_text=patronymic_text,
            birthday_date=birthday_date,
            passport_number_text=passport_number_text,
            email_text=email_text,
            phone_number_text=phone_number_text,
            job_position_text=job_position_text,
            hiring_date_text=hiring_date_text,
            salary_text=salary_text,
            department_text=department_text,
            work_schedule_text=work_schedule_text,
            work_status_text=work_status_text,
        )

        Employee.update(employee_id, serialized_employee)

        self.cleanup()


class HotelRoomController(Controller):
    def submit_create(self):
        employee_id = get_key_from_dict_by_value(self.entries["employee_list"], self.entries["employee_combobox_selected_text"].get())
        room_type_id = get_key_from_dict_by_value(self.entries["room_type_list"], self.entries["room_type_combobox_selected_text"].get())

        serialized_hotel_room = HotelRoomSerializer(employee_id=employee_id, room_type_id=room_type_id)
        HotelRoom.create(serialized_hotel_room)
        self.cleanup()

    def submit_update(self, room_id):
        employee_id = get_key_from_dict_by_value(self.entries["employee_list"], self.entries["employee_combobox_selected_text"].get())
        room_type_id = get_key_from_dict_by_value(self.entries["room_type_list"], self.entries["room_type_combobox_selected_text"].get())
        serialized_hotel_room = HotelRoomSerializer(employee_id=employee_id, room_type_id=room_type_id)
        HotelRoom.update(room_id, serialized_hotel_room)
        self.cleanup()


class AdditionalServiceController(Controller):
    def submit_create(self):
        service_name = self.entries["service_name_entry"].get()
        service_description = self.entries["service_description_entry"].get()
        service_price = self.entries["service_price_entry"].get()

        serialized_service = AdditionalServiceSerializer(service_name=service_name, service_description=service_description, service_price=service_price)
        AdditionalServiceType.create(serialized_service)

    def submit_update(self, object_id):
        service_name = self.entries["service_name_entry"].get()
        service_description = self.entries["service_description_entry"].get()
        service_price = self.entries["service_price_entry"].get()

        serialized_service = AdditionalServiceSerializer(service_name=service_name, service_description=service_description, service_price=service_price)
        AdditionalServiceType.update(object_id, serialized_service)


class JobPositionController(Controller):
    def submit_create(self):
        job_title = self.entries["job_title_entry"].get()
        serialized_job_position = JobPositionSerializer(job_title=job_title)
        JobPosition.create(serialized_job_position)

    def submit_update(self, object_id):
        job_title = self.entries["job_title_entry"].get()
        serialized_job_position = JobPositionSerializer(job_title=job_title)
        JobPosition.update(object_id, serialized_job_position)


class DepartmentController(Controller):
    def submit_create(self):
        department_title = self.entries["department_title_entry"].get()
        serialized_department = DepartmentSerializer(department_title=department_title)
        Department.create(serialized_department)

    def submit_update(self, object_id):
        department_title = self.entries["department_title_entry"].get()
        serialized_department = DepartmentSerializer(department_title=department_title)
        Department.update(object_id, serialized_department)


class RoomTypeController(Controller):
    def submit_create(self):
        hotel_room_type_title = self.entries["room_type_title_entry"].get()
        hotel_room_type_description = self.entries["room_type_description_entry"].get()
        hotel_room_type_price = self.entries["room_type_price_entry"].get()

        serialized_room_type = RoomTypeSerializer(title=hotel_room_type_title, description=hotel_room_type_description, price=hotel_room_type_price)
        RoomType.create(serialized_room_type)

    def submit_update(self, object_id):
        hotel_room_type_title = self.entries["room_type_title_entry"].get()
        hotel_room_type_description = self.entries["room_type_description_entry"].get()
        hotel_room_type_price = self.entries["room_type_price_entry"].get()

        serialized_room_type = RoomTypeSerializer(title=hotel_room_type_title, description=hotel_room_type_description, price=hotel_room_type_price)
        RoomType.update(object_id, serialized_room_type)


class WorkScheduleController(Controller):
    def submit_create(self):
        work_schedule_title = self.entries["work_schedule_title_entry"].get()
        serialized_work_schedule = WorkScheduleSerializer(work_schedule_title=work_schedule_title)
        WorkSchedule.create(serialized_work_schedule)

    def submit_update(self, object_id):
        work_schedule_title = self.entries["work_schedule_title_entry"].get()
        serialized_work_schedule = WorkScheduleSerializer(work_schedule_title=work_schedule_title)
        WorkSchedule.update(object_id, serialized_work_schedule)
