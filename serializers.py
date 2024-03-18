from datetime import datetime
from typing import List


# serialized_client = ClientDataSerializer(
#             first_name_text=first_name_text,
#             last_name_text=last_name_text,
#             patronymic_text=patronymic_text,
#             email_text=email_text,
#             passport_number_text=passport_number_text,
#             additional_service_text=additional_service_text,
#             payment_type_text=payment_type_text,
#         )

class ClientDataSerializer:
    def __init__(
            self,
            first_name_text: str,
            last_name_text: str,
            patronymic_text: str,
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
        self.email = email_text
        self.phone_number = phone_number_text
        self.passport_number_text = passport_number_text

    @staticmethod
    def prepare_data_to_print(clients_rows):
        result = []
        for row in clients_rows:
            client_info_dict = {
                "registration_number": row[0],
                "fio": row[1],
                "room_number": row[2],
                "date_from": row[3],
                "date_to": row[4],
                "additional_service": row[5],
                "payment_type": row[6],
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

