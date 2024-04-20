import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView

class MainWindow(QMainWindow):
    columns = 5

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Table Example")
        self.setGeometry(100, 100, 800, 600)

        # Создаем таблицу
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(100)  # Устанавливаем количество строк
        self.tableWidget.setColumnCount(self.columns)  # Устанавливаем количество столбцов

        # Заполняем таблицу данными
        for row in range(100):
            for col in range(self.columns):
                item = QTableWidgetItem(f"Row {row+1}, Col {col+1}")
                self.tableWidget.setItem(row, col, item)

        # Устанавливаем горизонтальные заголовки
        self.tableWidget.setHorizontalHeaderLabels([f"Column {col+1}" for col in range(self.columns)])

        # Применяем стили для заголовков таблицы
        header = self.tableWidget.horizontalHeader()
        header.setStyleSheet("""
            color: #000000; /* Цвет текста */
            border: 1px solid #dee2e6; /* Серый бордюр */
            border-radius: 4px; /* Закругленные углы */
        """)

        # Устанавливаем растягивание столбцов по содержимому
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Устанавливаем цвет фона и цвет текста для ячеек таблицы
        # self.tableWidget.setStyleSheet("""
        #     background-color: #ffffff; /* Белый фон */
        #     color: #333333; /* Цвет текста */
        #     border: 1px solid #dee2e6; /* Серый бордюр */
        # """)

        # Создаем вертикальный Layout и добавляем в него таблицу
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)

        # Создаем центральный виджет и устанавливаем в него Layout
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()