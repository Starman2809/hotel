from PyQt6.QtCore import QLocale
from PyQt6.QtWidgets import QCalendarWidget

from design.style import calendar_style


class RussianCalendar(QCalendarWidget):
    russian_locale = QLocale(QLocale.Language.Russian, QLocale.Country.Russia)

    def __init__(self):
        super().__init__()
        self.setLocale(self.russian_locale)
        self.setStyleSheet(calendar_style)
        self.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
