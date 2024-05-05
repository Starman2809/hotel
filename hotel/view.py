import sys

from PyQt6.QtWidgets import QApplication

from design.form import LoginForm
from design.style import login_form_style_sheet


class AllActionsView:
    def __init__(self):
        self.app = QApplication(sys.argv)

    def show_auth_window(self):
        login_form = LoginForm()
        login_form.setStyleSheet(login_form_style_sheet)
        login_form.show()
        self.app.exec()
