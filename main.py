import sys

from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt

from hotel.view import ClientView, BookingView, AllActionsView


def main():
    print(123)
    # client_view = ClientView()
    # client_view.create_new_view_window()
    # client_view.read_all()
    # client_id = 5
    # client_view.update_view_window(client_id)
    # pass
    # booking_view = BookingView()
    # booking_view.search_available_window()
    # booking_view.read_all()
    all_actions_view = AllActionsView()
    all_actions_view.show_all_actions_windows()



if __name__ == "__main__":
    main()