import os

current_directory = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(current_directory, 'hotel.accdb')

