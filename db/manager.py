import pyodbc


class DatabaseManager:
    def __init__(self, db_file):
        self.conn_str = (
            r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" rf"DBQ={db_file};"
        )
        self.connection = None

    def connect(self):
        self.connection = pyodbc.connect(self.conn_str)

    def close(self):
        if self.connection:
            self.connection.close()


