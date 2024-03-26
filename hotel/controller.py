from db.serializers import ClientDataSerializer, EmployeeSerializer
from hotel.models import Client, Employee
from utils.utils import get_key_from_dict_by_value


class ClientController:
    def __init__(self):
        self.entries = {}
        self.root = None

    def cleanup(self):
        """
        Method for deleting old values from memory after use
        """
        self.entries = {}

    def submit_create_client_data(self):
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

    def submit_update_client_data(self, client_id):
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

        Client.update_client(client_id, serialized_client)

        self.cleanup()


class EmployeeController:

    def __init__(self):
        self.entries = {}
        self.root = None

    def cleanup(self):
        """
        Method for deleting old values from memory after use
        """
        self.entries = {}

    def submit_create_employee_data(self):

        job_type_id = get_key_from_dict_by_value(self.entries["job_type_list"], self.entries["job_type_combobox_selected_text"].get())
        department_type_id = get_key_from_dict_by_value(self.entries["department_list"], self.entries["department_type_combobox_selected_text"].get())
        work_schedule_type_id = get_key_from_dict_by_value(self.entries["work_schedule_list"], self.entries["work_schedule_combobox_selected_text"].get())

        first_name_text = self.entries["first_name_entry"].get()
        last_name_text = self.entries["last_name_entry"].get()
        patronymic_text = self.entries["patronymic_entry"].get()
        birthday_date = self.entries["birthday_date_calendar"].selection_get()
        passport_number_text = self.entries["passport_number_entry"].get()
        email_text = self.entries["email_entry"].get()
        phone_number_text = self.entries["phone_number_entry"].get()
        job_type_text = job_type_id
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
            job_type_text=job_type_text,
            hiring_date_text=hiring_date_text,
            salary_text=salary_text,
            department_text=department_text,
            work_schedule_text=work_schedule_text,
            work_status_text=work_status_text,
        )

        Employee.create(serialized_employee)

        self.cleanup()

    def submit_update_employee_data(self, employee_id):
        print('-----------------')
        print(employee_id)
        job_type_id = get_key_from_dict_by_value(self.entries["job_type_list"], self.entries["job_type_combobox_selected_text"].get())
        department_type_id = get_key_from_dict_by_value(self.entries["department_list"], self.entries["department_type_combobox_selected_text"].get())
        work_schedule_type_id = get_key_from_dict_by_value(self.entries["work_schedule_list"], self.entries["work_schedule_combobox_selected_text"].get())

        first_name_text = self.entries["first_name_entry"].get()
        last_name_text = self.entries["last_name_entry"].get()
        patronymic_text = self.entries["patronymic_entry"].get()
        birthday_date = self.entries["birthday_date_calendar"].selection_get()
        passport_number_text = self.entries["passport_number_entry"].get()
        email_text = self.entries["email_entry"].get()
        phone_number_text = self.entries["phone_number_entry"].get()
        job_type_text = job_type_id
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
            job_type_text=job_type_text,
            hiring_date_text=hiring_date_text,
            salary_text=salary_text,
            department_text=department_text,
            work_schedule_text=work_schedule_text,
            work_status_text=work_status_text,
        )

        Employee.update(employee_id, serialized_employee)

        self.cleanup()
