from db.serializers import (ClientDataSerializer, EmployeeSerializer, HotelRoomSerializer,
                            JobPositionSerializer, DepartmentSerializer, RoomTypeSerializer, WorkScheduleSerializer,
                            PaymentTypeSerializer, BookingSerializer)
from hotel.models import (Client, Employee, HotelRoom, JobPosition, Department, RoomType,
                          WorkSchedule, PaymentType, Booking)


class PaymentTypeController:
    @staticmethod
    def submit_create(input_data):
        description = input_data["description_entry"].text()

        serialized_payment_type = PaymentTypeSerializer(
            description=description,
        )

        PaymentType.create(serialized_payment_type)

    @staticmethod
    def submit_update(input_data, payment_type_id):
        description = input_data["description_entry"].text()

        serialized_payment_type = PaymentTypeSerializer(
            description=description,
        )

        PaymentType.update(payment_type_id, serialized_payment_type)

    @staticmethod
    def submit_delete(object_id):
        PaymentType.delete(object_id)


class ClientController:
    @staticmethod
    def submit_create(input_data):
        first_name_text = input_data["first_name_entry"].text()
        last_name_text = input_data["last_name_entry"].text()
        patronymic_text = input_data["patronymic_entry"].text()
        birthday_date = input_data["birthday_date_calendar"].selectedDate().toPyDate()
        email_text = input_data["email_entry"].text()
        phone_number_text = input_data["phone_number_entry"].text()
        passport_number_text = input_data["passport_number_entry"].text()

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

    @staticmethod
    def submit_update(input_data, client_id):
        first_name_text = input_data["first_name_entry"].text()
        last_name_text = input_data["last_name_entry"].text()
        patronymic_text = input_data["patronymic_entry"].text()
        birthday_date = input_data["birthday_date_calendar"].selectedDate().toPyDate()
        email_text = input_data["email_entry"].text()
        phone_number_text = input_data["phone_number_entry"].text()
        passport_number_text = input_data["passport_number_entry"].text()

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

    @staticmethod
    def submit_delete(client_id):
        Client.delete(client_id)


class EmployeeController:
    @staticmethod
    def submit_create(input_data):

        first_name_text = input_data["first_name_entry"].text()
        last_name_text = input_data["last_name_entry"].text()
        patronymic_text = input_data["patronymic_entry"].text()
        birthday_date = input_data["birthday_date_calendar"].selectedDate().toPyDate()
        passport_number_text = input_data["passport_number_entry"].text()
        email_text = input_data["email_entry"].text()
        phone_number_text = input_data["phone_number_entry"].text()
        job_position_text = input_data["job_position_combobox"].currentData()
        hiring_date_text = input_data["hiring_date_calendar"].selectedDate().toPyDate()
        salary_text = input_data["salary_entry"].text()
        department_text = input_data["department_combobox"].currentData()
        work_schedule_text = input_data["work_schedule_combobox"].currentData()
        work_status_text = input_data["work_status_entry"].text()

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

    @staticmethod
    def submit_update(input_data, employee_id):
        first_name_text = input_data["first_name_entry"].text()
        last_name_text = input_data["last_name_entry"].text()
        patronymic_text = input_data["patronymic_entry"].text()
        birthday_date = input_data["birthday_date_calendar"].selectedDate().toPyDate()
        passport_number_text = input_data["passport_number_entry"].text()
        email_text = input_data["email_entry"].text()
        phone_number_text = input_data["phone_number_entry"].text()
        job_position_text = input_data["job_position_combobox"].currentData()
        hiring_date_text = input_data["hiring_date_calendar"].selectedDate().toPyDate()
        salary_text = input_data["salary_entry"].text()
        department_text = input_data["department_combobox"].currentData()
        work_schedule_text = input_data["work_schedule_combobox"].currentData()
        work_status_text = input_data["work_status_entry"].text()

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

    @staticmethod
    def submit_delete(object_id):
        try:
            Employee.delete(object_id)
        except Exception as e:
            print(e)


class HotelRoomController:
    @staticmethod
    def submit_create(input_data):
        employee_id = input_data["employee_combobox"].currentData()
        room_type_id = input_data["room_type_combobox"].currentData()

        serialized_hotel_room = HotelRoomSerializer(employee_id=employee_id, room_type_id=room_type_id)
        HotelRoom.create(serialized_hotel_room)

    @staticmethod
    def submit_update(input_data, room_id):
        employee_id = input_data["employee_combobox"].currentData()
        room_type_id = input_data["room_type_combobox"].currentData()

        serialized_hotel_room = HotelRoomSerializer(employee_id=employee_id, room_type_id=room_type_id)
        HotelRoom.update(room_id, serialized_hotel_room)

    @staticmethod
    def submit_delete(object_id):
        try:
            HotelRoom.delete(object_id)
        except Exception as e:
            print(e)


class JobPositionController:
    @staticmethod
    def submit_create(input_data):
        job_title = input_data["job_title_entry"].text()
        serialized_job_position = JobPositionSerializer(job_title=job_title)
        JobPosition.create(serialized_job_position)

    @staticmethod
    def submit_update(input_data, object_id):
        job_title = input_data["job_title_entry"].text()
        serialized_job_position = JobPositionSerializer(job_title=job_title)
        JobPosition.update(object_id, serialized_job_position)

    @staticmethod
    def submit_delete(object_id):
        try:
            JobPosition.delete(object_id)
        except Exception as e:
            print(e)


class DepartmentController:
    @staticmethod
    def submit_create(input_data):
        department_title = input_data["department_title_entry"].text()
        serialized_department = DepartmentSerializer(department_title=department_title)
        Department.create(serialized_department)

    @staticmethod
    def submit_update(input_data, object_id):
        department_title = input_data["department_title_entry"].text()
        serialized_department = DepartmentSerializer(department_title=department_title)
        Department.update(object_id, serialized_department)

    @staticmethod
    def submit_delete(object_id):
        try:
            Department.delete(object_id)
        except Exception as e:
            print(e)


class RoomTypeController:
    @staticmethod
    def submit_create(input_data):
        hotel_room_type_title = input_data["room_type_title_entry"].text()
        hotel_room_type_description = input_data["room_type_description_entry"].text()
        hotel_room_type_price = input_data["room_type_price_entry"].text()

        serialized_room_type = RoomTypeSerializer(title=hotel_room_type_title, description=hotel_room_type_description, price=hotel_room_type_price)
        RoomType.create(serialized_room_type)

    @staticmethod
    def submit_update(input_data, object_id):
        hotel_room_type_title = input_data["room_type_title_entry"].text()
        hotel_room_type_description = input_data["room_type_description_entry"].text()
        hotel_room_type_price = input_data["room_type_price_entry"].text()

        serialized_room_type = RoomTypeSerializer(title=hotel_room_type_title, description=hotel_room_type_description, price=hotel_room_type_price)
        RoomType.update(object_id, serialized_room_type)

    @staticmethod
    def submit_delete(object_id):
        try:
            RoomType.delete(object_id)
        except Exception as e:
            print(e)


class WorkScheduleController:
    @staticmethod
    def submit_create(input_data):
        work_schedule_title = input_data["work_schedule_title_entry"].text()
        serialized_work_schedule = WorkScheduleSerializer(work_schedule_title=work_schedule_title)
        WorkSchedule.create(serialized_work_schedule)

    @staticmethod
    def submit_update(input_data, object_id):
        work_schedule_title = input_data["work_schedule_title_entry"].text()
        serialized_work_schedule = WorkScheduleSerializer(work_schedule_title=work_schedule_title)
        WorkSchedule.update(object_id, serialized_work_schedule)

    @staticmethod
    def submit_delete(object_id):
        try:
            WorkSchedule.delete(object_id)
        except Exception as e:
            print(e)


class BookingController:
    @staticmethod
    def submit_create(input_data):
        room_id = input_data["room_id_entry"].text()
        date_from = input_data["date_from_calendar"].selectedDate().toPyDate()
        date_to = input_data["date_to_calendar"].selectedDate().toPyDate()
        booking_date = input_data["booking_date_calendar"].selectedDate().toPyDate()
        payment_type = input_data["payment_type_combobox"].currentData()
        client = input_data["client_combobox"].currentData()
        payment_status = input_data["payment_status_checkbox"].isChecked()
        final_price = input_data["final_price_entry"].text()

        serialized_booking = BookingSerializer(
            room_id=room_id, date_from=date_from, date_to=date_to,
            booking_date=booking_date, payment_type=payment_type, client=client,
            payment_status=payment_status, final_price=final_price
        )
        Booking.create(serialized_booking)

    @staticmethod
    def submit_update(input_data, object_id):
        room_id = input_data["room_id_entry"].text()
        date_from = input_data["date_from_calendar"].selectedDate().toPyDate()
        date_to = input_data["date_to_calendar"].selectedDate().toPyDate()
        booking_date = input_data["booking_date_calendar"].selectedDate().toPyDate()
        payment_type = input_data["payment_type_combobox"].currentData()
        client = input_data["client_combobox"].currentData()
        payment_status = input_data["payment_status_checkbox"].isChecked()
        final_price = float(input_data["final_price_entry"].text())

        serialized_booking = BookingSerializer(
            room_id=room_id, date_from=date_from, date_to=date_to,
            booking_date=booking_date, payment_type=payment_type, client=client,
            payment_status=payment_status, final_price=final_price
        )
        Booking.update(object_id, serialized_booking)

    @staticmethod
    def submit_delete(object_id):
        try:
            Booking.delete(object_id)
        except Exception as e:
            print(e)
