import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCalendarWidget
from PyQt6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Независимые календари")

        layout = QVBoxLayout()

        # Создаем два календаря
        self.calendar1 = QCalendarWidget()
        self.calendar2 = QCalendarWidget()

        # Устанавливаем формат заголовка для скрытия номера недели
        self.calendar1.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.calendar2.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)

        layout.addWidget(self.calendar1)
        layout.addWidget(self.calendar2)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())