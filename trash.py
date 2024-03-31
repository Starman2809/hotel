# def query_data(self):
    #     cursor = self.db_manager.connection.cursor()
    #     cursor.execute("SELECT * FROM HotelRooms")
    #     rows = cursor.fetchall()
    #     cursor.close()
    #     return rows

    # def get_tables(self) -> List[Any]:
    #     tables_result = []
    #
    #     self.db_manager.connect()
    #
    #     connection = self.db_manager.connection
    #     tables = connection.cursor().tables()
    #
    #     for table in tables:
    #         tables_result.append(table.table_name)
    #     self.db_manager.close()
    #
    #     return tables_result


    # def get_rooms(self):
    #     self.db_manager.connect()
    #
    #     connection = self.db_manager.connection
    #     cursor = connection.cursor()
    #     cursor.execute("SELECT * FROM Клиенты")
    #     rows = cursor.fetchall()
    #
    #     self.db_manager.close()
    #
    #     return rows

    # def get_columns_from_table(self, table_name: str):
    #     result = []
    #
    #     self.db_manager.connect()
    #     connection = self.db_manager.connection
    #     cursor = connection.cursor()
    #
    #     query_string = f"SELECT * FROM {table_name}"
    #     cursor.execute(query_string)
    #
    #     columns = [column[0] for column in cursor.description]
    #
    #     for column in columns:
    #         result.append(column)
    #     return result

# """
#         Метод, который конвертирует данные из формы в нужный формат, для сохранения в БД
#
#         :param registration_number:
#         :param fio:
#         :param room_number:
#         :param date_from: формат строки - 17.03.2024
#         :param date_to: формат строки - 17.03.2024
#         :param additional_service:
#         :param payment_type:
#         """
# self.date_from = datetime.strptime(date_from, "%d.%m.%Y")
#         self.date_to = datetime.strptime(date_to, "%d.%m.%Y")