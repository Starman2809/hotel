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