from contants import DB_PATH
from db.manager import DatabaseManager
from db.models import Client
from serializers import ClientDataSerializer


class HotelHandler:
    registration_number_entry = None
    fio_entry = None
    room_number_entry = None
    date_from_calendar = None
    date_to_calendar = None
    additional_service_entry = None
    payment_type_entry = None

    def __init__(self):
        self.db_manager = DatabaseManager(DB_PATH)
        self.entries = {}

    def submit_client_data(self):
        first_name_text = self.entries["first_name_entry"].get()
        last_name_text = self.entries["last_name_entry"].get()
        patronymic_text = self.entries["patronymic_entry"].get()
        email_text = self.entries["email_entry"].get()
        phone_number_text = self.entries["phone_number_entry"].get()
        passport_number_text = self.entries["passport_number_entry"].get()

        serialized_client = ClientDataSerializer(
            first_name_text=first_name_text,
            last_name_text=last_name_text,
            patronymic_text=patronymic_text,
            email_text=email_text,
            phone_number_text=phone_number_text,
            passport_number_text=passport_number_text,
        )

        Client.create_client(serialized_client)
