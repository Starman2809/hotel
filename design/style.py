from PyQt6.QtCore import QCoreApplication

# Define CSS styles in a string
login_form_style_sheet = """
/* General form styling */
QWidget {
    background-color: #F0F0F0;
    border-radius: 10px;
    padding: 20px;
}

/* Labels */
QLabel {
    font-family: Arial, sans-serif;
    font-size: 16px;
    margin-bottom: 5px;
}

/* Input fields */
QLineEdit {
    font-family: Arial, sans-serif;
    font-size: 14px;
    padding: 8px;
    border: 1px solid #CCC;
    border-radius: 5px;
    margin-bottom: 10px;
}

/* Login button */
QPushButton {
    background-color: #007BFF;
    color: white;
    font-family: Arial, sans-serif;
    font-size: 16px;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

/* Hover effect for button */
QPushButton:hover {
    background-color: #0056b3;
}
"""

red_qt_push_button = """
background-color: red; color: white;
"""

green_qt_push_button = """
background-color: green; color: white;
"""

form_create_title = """
font-size: 24px; font-weight: bold; margin-bottom: 20px; color: black; background-color: #ddd;
"""

form_create_label_name_font_style = """
color: #333; font-size: 16px;
"""

form_create_input_field_style = """
padding: 6px; border: 1px solid #ccc; border-radius: 4px; font-size: 16px; background-color: #fff;
"""

calendar_style = """
QCalendarWidget QAbstractItemView { 
    border: 2px solid black;
} 

QCalendarWidget QToolButton { 
    color: black; 
}
"""

submit_button_style = """
QPushButton { 
    background-color: #007bff; color: #fff; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px;
}

QPushButton:hover { 
    background-color: #0056b3; 
}

QPushButton:pressed { 
    background-color: #28a745; 
}
"""

table_header_style = """
color: #000000; /* Цвет текста */
border: 1px solid #dee2e6; /* Серый бордюр */
border-radius: 4px; /* Закругленные углы */
"""

input_edit_style = """
padding: 6px; 
border: 1px solid #ccc; 
border-radius: 4px; 
font-size: 16px; 
background-color: #fff;
"""