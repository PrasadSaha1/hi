"""
Imports -
Pyside6 is used for Qt, which is used to make the GUI
QWidget and QApplication are the foundation of the GUI
QStackedWidget is used for changing pages
QLabel, QPushButton, QMessagebox, QComboBox and QLineEdit are widgets
QScrollArea is used to scroll through parts of the program
QFont is used for changing font
QPixmap is used for the image
QColordialog is used to help the user change the colors of the program. QtColor from QtGui is used to select the colors
QInputDialog is used to get the user's name when exporting data
Qt from QtCore is used to center text in labels, particularly when they have multiple lines
QEvent and QObject are used to show text when the user hovers over a widget
sys handles command line arguments needed for the GUI
factorial is used to quickly get a large number
mysql.connector is used to save the user's data through an account system
threading is needed to have the program update dynamically in the background
time is also needed for dynamic backup
reportlab is used to make the PDF
webbrowser is used to open the PDF in a browser
datetime is used to get the date for exporting data
openpyxl is used to create a spreadsheet in Excel
csv is used for saving data without an account system
os is used for confirming that the csv file is not empty
re is used for verifying passwords and emails
ast is used for parsing
"""

from PySide6.QtWidgets import QApplication, QWidget, QStackedWidget, QLabel, QPushButton, QLineEdit, QMessageBox, \
    QComboBox, QColorDialog, QScrollArea, QDialog, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QFont, QColor, QPixmap
from PySide6.QtCore import Qt, QEvent, QObject, QTimer, QThread, Signal
import sys
import signal
from math import factorial
import mysql.connector
import threading
import time
import random
import string
import openpyxl
from openpyxl.styles import Alignment
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import webbrowser
import datetime
import csv
import os
import re
import ast

# connecting to the SQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="digmines",
    database="gpa_calculator_database"
)

my_cursor = db.cursor()

# this SQL table will store the user's username, password, as well as elements
# of the program that they have changed in the settings as well as the GPA scale

my_cursor.execute(
    "CREATE TABLE IF NOT EXISTS user_data("
    "userID int PRIMARY KEY AUTO_INCREMENT,"
    "username TEXT, "
    "password TEXT, "
    "email VARCHAR(100),"
    "GPA_scale VARCHAR(100), "
    "honors_weight_100 VARCHAR(100),"
    "AP_weight_100 VARCHAR(100), "
    "honors_weight_4 VARCHAR(100),"
    "AP_weight_4 VARCHAR(100), "
    "honors_weight VARCHAR(100), "
    "AP_weight VARCHAR(100), "
    "default_Q1_weight VARCHAR(100), "
    "default_Q2_weight VARCHAR(100), "
    "default_E2_weight VARCHAR(100), "
    "default_Q3_weight VARCHAR(100), "
    "default_Q4_weight VARCHAR(100), "
    "default_E4_weight VARCHAR(100), "
    "color_1 VARCHAR(100), "
    "color_2 VARCHAR(100)"
    ")"
)

# each element of this table will be user class
my_cursor.execute(
    "CREATE TABLE IF NOT EXISTS class_data("
    "classID int PRIMARY KEY AUTO_INCREMENT, "
    "userID int, "
    "scope VARCHAR(50), "
    "screen VARCHAR(50), "
    "class_name TEXT, "
    "grade VARCHAR(50), "
    "weight VARCHAR(50), "
    "credit VARCHAR(50), "
    "year VARCHAR(50), "
    "Q1_weight VARCHAR(50), "
    "Q2_weight VARCHAR(50), "
    "E2_weight VARCHAR(50), "
    "Q3_weight VARCHAR(50), "
    "Q4_weight VARCHAR(50), "
    "E4_weight VARCHAR(50), "
    "exact_grade VARCHAR(50), "
    "first_time BOOLEAN, "
    "Q1_grade VARCHAR(50), " 
    "Q2_grade VARCHAR(50), " 
    "E2_grade VARCHAR(50), " 
    "Q3_grade VARCHAR(50), " 
    "Q4_grade VARCHAR(50), " 
    "E4_grade VARCHAR(50), "
    "categories TEXT, "
    "Q1_term_first_time BOOLEAN, "
    "Q1_assignments TEXT, "
    "Q1_exact_grade VARCHAR(50), "
    "Q2_term_first_time BOOLEAN, "
    "Q2_assignments TEXT, "
    "Q2_exact_grade VARCHAR(50), "
    "E2_term_first_time BOOLEAN, "
    "E2_assignments TEXT, "
    "E2_exact_grade VARCHAR(50), "
    "Q3_term_first_time BOOLEAN, "
    "Q3_assignments TEXT, "
    "Q3_exact_grade VARCHAR(50), "
    "Q4_term_first_time BOOLEAN, "
    "Q4_assignments TEXT, "
    "Q4_exact_grade VARCHAR(50), "
    "E4_term_first_time BOOLEAN, "
    "E4_assignments TEXT, "
    "E4_exact_grade VARCHAR(50) "
    ")"
)


class UserClass:
    """This class is used to save data about each of the user's classes"""
    def __init__(self, class_id, scope, screen, MORE_INFO_ID, more_info_screen, class_name, grade, weight, credit, year,
                 grade_line_edit,
                 Q1_grade=None, Q2_grade=None, E2_grade=None, Q3_grade=None, Q4_grade=None, E4_grade=None,
                 Q1_weight=None, Q2_weight=None, E2_weight=None, Q3_weight=None, Q4_weight=None, E4_weight=None,
                 Q1_grade_line_edit=None, Q2_grade_line_edit=None, E2_grade_line_edit=None, Q3_grade_line_edit=None, Q4_grade_line_edit=None, E4_grade_line_edit=None,
                 Q1_weight_line_edit=None, Q2_weight_line_edit=None, E2_weight_line_edit=None, Q3_weight_line_edit=None, Q4_weight_line_edit=None, E4_weight_line_edit=None,
                 exact_grade=None, first_time=None, more_info_button=None,
                 MORE_INFO_ID_Q1=None, MORE_INFO_ID_Q2=None, MORE_INFO_ID_E2=None, MORE_INFO_ID_Q3=None, MORE_INFO_ID_Q4=None, MORE_INFO_ID_E4=None,
                 more_info_scroll_area_Q1_QWidget=None, more_info_scroll_area_Q2_QWidget=None, more_info_scroll_area_E2_QWidget=None,
                 more_info_scroll_area_Q3_QWidget=None, more_info_scroll_area_Q4_QWidget=None, more_info_scroll_area_E4_QWidget=None):
        '''Initialize this class'''
        # note that the parameters defined with None are optional. The other parameters are mandatory

        self.class_id = class_id  # id of the class. This is based on SQL
        self.scope = scope  # Quarterly of Cumulative
        self.screen = screen  # self.quarterly_GPA_screen, self.year_8_screen, etc.
        self.current_term = None  # used for assignments in a specific term

        # creating the subclasses for each term
        self.Q1 = self.Q1()
        self.Q2 = self.Q2()
        self.E2 = self.E2()
        self.Q3 = self.Q3()
        self.Q4 = self.Q4()
        self.E4 = self.E4()

        # each of the line edits is a part of the class
        # only the grade_line_edit is actually needed, but the rest are done for consistency
        self.grade_line_edit = grade_line_edit  # needed to insert the grade after calculated based on the term grades

        self.MORE_INFO_ID = MORE_INFO_ID  # this is an index for StackedWidget
        self.more_info_screen = more_info_screen  # this is a QWidget
        self.more_info_button = more_info_button  # this is only needed for importing local data

        # information about each class based on user input
        self.class_name = class_name
        self.grade = grade
        self.weight = weight
        self.credit = credit
        self.year = year

        # these line edits are in the program as they need to be accessed to calculate GPA based off of term grades
        self.Q1_grade_line_edit = Q1_grade_line_edit
        self.Q2_grade_line_edit = Q2_grade_line_edit
        self.E2_grade_line_edit = E2_grade_line_edit
        self.Q3_grade_line_edit = Q3_grade_line_edit
        self.Q4_grade_line_edit = Q4_grade_line_edit
        self.E4_grade_line_edit = E4_grade_line_edit

        # like with the grade_line_edits, these must be accessed to calculate GPA based off of term grades
        # they do not have to be iterated through, so they do not have to be defined as ["term", None]
        self.Q1_weight_line_edit = Q1_weight_line_edit
        self.Q2_weight_line_edit = Q2_weight_line_edit
        self.E2_weight_line_edit = E2_weight_line_edit
        self.Q3_weight_line_edit = Q3_weight_line_edit
        self.Q3_weight_line_edit = Q4_weight_line_edit
        self.E4_weight_line_edit = E4_weight_line_edit

        # the grade for each term in term grades.
        self.Q1_grade = Q1_grade
        self.Q2_grade = Q2_grade
        self.E2_grade = E2_grade
        self.Q3_grade = Q3_grade
        self.Q4_grade = Q4_grade
        self.E4_grade = E4_grade

        # because the weight isn't iterated through, it doesn't have be to defined as ["term", None]
        self.Q1_weight = Q1_weight
        self.Q2_weight = Q2_weight
        self.E2_weight = E2_weight
        self.Q3_weight = Q3_weight
        self.Q4_weight = Q4_weight
        self.E4_weight = E4_weight

        self.exact_grade = exact_grade  # this is the non-rounded class grade based off of term grades
        self.first_time = first_time  # if this is false, previous inputs will be entered for the term grades screen

        # these are numbers that will act as indexes for changing the stacked_widget
        self.MORE_INFO_ID_Q1 = MORE_INFO_ID_Q1
        self.MORE_INFO_ID_Q2 = MORE_INFO_ID_Q2
        self.MORE_INFO_ID_E2 = MORE_INFO_ID_E2
        self.MORE_INFO_ID_Q3 = MORE_INFO_ID_Q3
        self.MORE_INFO_ID_Q4 = MORE_INFO_ID_Q4
        self.MORE_INFO_ID_E4 = MORE_INFO_ID_E4

        # these are the QWidgets for the more information screens
        self.more_info_scroll_area_Q1_QWidget = more_info_scroll_area_Q1_QWidget
        self.more_info_scroll_area_Q2_QWidget = more_info_scroll_area_Q2_QWidget
        self.more_info_scroll_area_E2_QWidget = more_info_scroll_area_E2_QWidget
        self.more_info_scroll_area_Q3_QWidget = more_info_scroll_area_Q3_QWidget
        self.more_info_scroll_area_Q4_QWidget = more_info_scroll_area_Q4_QWidget
        self.more_info_scroll_area_E4_QWidget = more_info_scroll_area_E4_QWidget

        self.categories = []

    def set_term(self, term):
        """This changes the current_term so the information in each of the subclasses can be accessed"""
        # Get the nested class based on the string name
        self.current_term_string = term  # set the term to the parameter
        string_term = getattr(self, term, None)  # turn the parameter into a python Class
        self.current_term = string_term

    class BaseTerm:
        """This class contains the elements that will be in each of the python classes that represents a term"""
        def __init__(self):
            self.term_first_time = True  # if it's the first time opening that term
            # this is used for making a sample category

            self.category_line_edits = []  # stores the line edits for the categories

            self.assignments = []  # stores information about the assignments
            self.assignment_line_edits = []  # stores the line edits for the assignments
            self.assignment_category_combo_boxes = []  # stores the combo boxes for each assignment
            self.exact_grade = None  # this is the grade calculated based on the assignments

            self.category_scroll_area_QWidget = None  # this is the scroll area for the categories
            self.assignment_scroll_area_QWidget = None  # this is the scroll area for the assignments

    class Q1(BaseTerm):  # inherits from the BaseTerm Class
        """This class saves data about the Q1 term"""
        def __init__(self):
            super().__init__()  # Initialize common attributes

    class Q2(BaseTerm):
        """This class saves data about the Q2 term"""
        def __init__(self):
            super().__init__()  # Initialize common attributes

    class E2(BaseTerm):
        """This class saves data about the E2 term"""
        def __init__(self):
            super().__init__()  # Initialize common attributes

    class Q3(BaseTerm):
        """This class saves data about the Q3 term"""
        def __init__(self):
            super().__init__()  # Initialize common attributes

    class Q4(BaseTerm):
        """This class saves data about the Q4 term"""
        def __init__(self):
            super().__init__()  # Initialize common attributes

    class E4(BaseTerm):
        """This class saves data about the E4 term"""
        def __init__(self):
            super().__init__()  # Initialize common attributes


class ComboBox(QComboBox):
    """This class is used to create a new version of QComboBox.
    In the new version, the user can not scroll through the combo box to change the values of the combo box
    This is done to help the user experience. Each combo box is defined with ComboBox, not QComboBox"""
    def __init__(self, parent=None):
        # Call the constructor of the parent class
        super().__init__(parent)
        # Install the event filter to capture events for this object
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        # Check if the event is for this object and is a wheel event
        if obj == self and event.type() == QEvent.Wheel:
            # Prevent the default behavior of changing the value when scrolling
            event.ignore()
            # Indicate that the event has been handled
            return True
        # Call the base class event filter for other events
        return super().eventFilter(obj, event)


class HoverEventFilter(QObject):
    """This class causes text to appear whenever the user hovers over certain widgets"""
    def __init__(self, help_label, text, widget, color_1, color_2, scroll_area=None):
        super().__init__()
        self.help_label = help_label  # the label with the help text
        self.text = text  # the text in the help_label
        self.widget = widget  # the widget that will display the help_label when hovered over
        self.color_1 = color_1  # first color of the program
        self.color_2 = color_2  # second color of the program
        self.scroll_area = scroll_area  # if the widget is from a scroll area, this is needed

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Enter:  # if the user hovers over the widget
            self.help_label.setText(self.text)  # set the label text to the text stated
            # the next line changes the color of the label to match the program colors
            # note that the colors are inverse of the rest of the program so the label can easily be seen
            self.help_label.setStyleSheet(f"color: {self.color_1}; background-color: {self.color_2};")

            x = self.widget.x()
            y = self.widget.y() - self.help_label.sizeHint().height()

            if self.scroll_area:
                x += self.scroll_area.x()
                y += self.scroll_area.y() - self.scroll_area.verticalScrollBar().value()

            if x > 300:  # if the label is on the right of the screen, it will come from the opposite side
                x += self.widget.width() - self.help_label.sizeHint().width()

            # if the help text is multiple lines, the y accounts for that
            self.help_label.move(x, y)
            self.help_label.show()
            return True
        elif event.type() == QEvent.Leave:  # if the user leaves the widget
            self.help_label.hide()  # hide the help text
            # return True - usually, this is needed, but it was removed as help text for error signs had unusual behavior with this
        return super().eventFilter(obj, event)

class AllClassesQMessageBox(QDialog):
    """This is used to get a message box before exporting data for all classes"""
    def __init__(self, title, message, combo_options, scope, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setLayout(QVBoxLayout())

        # Create and add message label
        self.message_label = QLabel(message)
        self.layout().addWidget(self.message_label)

        if scope == "Quarterly":
            self.combo_box = QComboBox()
            self.combo_box.addItems(combo_options)
            self.layout().addWidget(self.combo_box)

        # Create and add line edit
        self.line_edit_label = QLabel("Write your name:")
        self.line_edit = QLineEdit()
        self.layout().addWidget(self.line_edit_label)
        self.layout().addWidget(self.line_edit)

        # Create and add OK and Cancel buttons
        self.button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)
        self.layout().addLayout(self.button_layout)

        # Connect buttons to dialog slots
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_selected_options_and_text(self, scope):
        """This is used to get data from the message box"""
        name = self.line_edit.text()
        year = None
        if scope == "Quarterly":
            year = self.combo_box.currentText()
        return name, year


class ChooseClassQMessageBox(QDialog):
    """This is used to get a message box before exporting data for a single class"""
    def __init__(self, title, message, combo_options, parent=None, class_=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setLayout(QVBoxLayout())

        # Create and add message label
        self.message_label = QLabel(message)
        self.layout().addWidget(self.message_label)

        # Create and add combo boxes
        self.combo_boxes = []
        for label_text, options in combo_options.items():
            label = QLabel(label_text)
            combo_box = QComboBox()
            combo_box.addItems(options)
            self.layout().addWidget(label)
            self.layout().addWidget(combo_box)
            self.combo_boxes.append(combo_box)

        # Create and add line edit
        self.line_edit_label = QLabel("Write your name:")
        self.line_edit = QLineEdit()
        self.layout().addWidget(self.line_edit_label)
        self.layout().addWidget(self.line_edit)

        # Create and add OK and Cancel buttons
        self.button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)
        self.layout().addLayout(self.button_layout)

        # Connect buttons to dialog slots
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)


    def get_selected_options_and_text(self, class_):
        """This is used to get data from the message box"""
        selected_options = [combo_box.currentText() for combo_box in self.combo_boxes]
        selected_indices = [combo_box.currentIndex() for combo_box in self.combo_boxes]
        entered_text = self.line_edit.text()
        return selected_options, selected_indices, entered_text


class Window(QWidget):
    """This is the main class for the GUI"""
    def __init__(self):
        """This function defines some variables and runs many functions"""
        super().__init__()
        self.setWindowTitle("GPA Calculator")

        signal.signal(signal.SIGINT, self.save_data_when_program_finished)  # used to save data if unexpected close to the program

        self.setFixedSize(600, 600)  # the window can not be resized

        self.stacked_widget = QStackedWidget(self)  # create the stacked widget
        self.stacked_widget.setGeometry(0, 0, 700, 600)  # set the size

        # this is for the date in output reports
        current_date = datetime.date.today()  # the date
        self.formatted_date = current_date.strftime("%B %d, %Y")

        # this is used for validating emails
        self.email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        # these lists will have the line edits for classes for the quarterly screen and each year
        self.quarterly_class_line_edits = []
        self.year_8_class_line_edits = []
        self.year_9_class_line_edits = []
        self.year_10_class_line_edits = []
        self.year_11_class_line_edits = []
        self.year_12_class_line_edits = []
        # this next list is used to iterate through the above lists in update_class_data()
        self.all_class_line_edits = [[None, self.quarterly_class_line_edits], [8, self.year_8_class_line_edits], [9, self.year_9_class_line_edits],
                                     [10, self.year_10_class_line_edits], [11, self.year_11_class_line_edits], [12, self.year_12_class_line_edits]]

        query = "SELECT classID FROM class_data ORDER BY classID DESC LIMIT 1"  # get the class ID of the highest class in the database
        my_cursor.execute(query)
        last_id = int()  # here to make it look better in PyCharm as this not being defined would cause an error
        for i in my_cursor:
            last_id = i[0]  # set the ID to the highest one in the database
        self.class_id = last_id + 1  # set the current idea to the previous highest + 1

        self.user_classes = []  # used to store the user data. ALl elements in this list will be an instance of the UserClass class
        self.all_line_edits = []  # every line edit in the program. This is used for input validation
        self.all_combo_boxes = []  # every combo box in the program. This is used for input validation
        self.unweighted_gpa = ""  # the value for the weighted and unweighted GPA
        self.weighted_gpa = ""
        self.color_1 = "black"  # colors of the programs, defaults listed here
        self.color_2 = "white"

        self.logged_in = False  # if the user is logged in with SQL
        self.account_id = None  # ID of the SQL account
        self.username = None  # more information about the SQL account
        self.password = None
        self.email = None

        self.GPA_scale = 100.0  # 100.0 or 4.0
        # this list translates letter grades into grades on the 4.0 scale
        self.letter_to_4 = {"A+": 4.0, "A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7,
                            "C+": 2.3, "C": 2.0, "C-": 1.7, "D+": 1.3, "D": 1.0, "F": 0.0}
        # This translates letter grades into numerical grades
        self.grade_to_letter = {"A+": range(97, factorial(999)), "A": range(93, 97), "A-": range(90, 93), "B+": range(87, 90),
                                "B": range(83, 87), "B-": range(80, 83), "C+": range(77, 80), "C": range(73, 77),
                                "C-": range(70, 73), "D+": range(67, 70), "D": range(65, 67), "F": range(0, 65)}

        self.honors_weight_100 = 1.03  # default weights for honors and AP classes on the 2 scales
        self.AP_weight_100 = 1.05
        self.honors_weight_4 = 1.125
        self.AP_weight_4 = 1.25
        self.honors_weight = self.honors_weight_100  # this is used when calculating GPA
        self.AP_weight = self.AP_weight_100

        self.default_Q1_weight = 21.25  # the default term weights for the term grades calculate
        self.default_Q2_weight = 21.25
        self.default_E2_weight = 5
        self.default_Q3_weight = 21.25
        self.default_Q4_weight = 21.25
        self.default_E4_weight = 10

        # creating the pages
        self.home_screen = QWidget()
        self.calc_my_GPA_homepage = QWidget()

        self.instructions_screen = QWidget()  # this screen is scrollable
        # the self.instructions_screen QWidget is needed to prevent errors. The screen is this QWidget, but all widgets on that screen will be in the next QWidget
        self.instructions_screen_scroll_area_QWidget = QWidget()  # create a QWidget for the scroll area
        self.instructions_screen_scroll_area_QWidget.setFixedSize(580, 2000)  # size for the scroll area QWidget

        self.instructions_screen_scroll_area = QScrollArea(self.instructions_screen)  #the scroll area
        self.instructions_screen_scroll_area.setWidget(self.instructions_screen_scroll_area_QWidget)
        self.instructions_screen_scroll_area.setWidgetResizable(True)  # the user can scroll through it
        self.instructions_screen_scroll_area.setGeometry(0, 0, 600, 600)

        self.FAQ_screen_1 = QWidget()  # the FAQ screen is scrollable, just like the instructions screen
        self.FAQ_screen_scroll_area_QWidget = QWidget()
        self.FAQ_screen_scroll_area_QWidget.setFixedSize(580, 1020)

        self.FAQ_screen_scroll_area = QScrollArea(self.FAQ_screen_1)
        self.FAQ_screen_scroll_area.setWidget(self.FAQ_screen_scroll_area_QWidget)
        self.FAQ_screen_scroll_area.setWidgetResizable(True)
        self.FAQ_screen_scroll_area.setGeometry(0, 0, 600, 600)

        # the rest of the pages
        self.settings_screen = QWidget()
        self.account_settings_homepage = QWidget()
        self.export_data_homepage = QWidget()

        # now, we enter subpages from the home page

        # sub pages for Calculate my GPA
        self.quarterly_GPA_screen = QWidget()
        self.cumulative_GPA_screen = QWidget()
        self.year_8_screen = QWidget()
        self.year_9_screen = QWidget()
        self.year_10_screen = QWidget()
        self.year_11_screen = QWidget()
        self.year_12_screen = QWidget()

        # subpages for account settings
        self.create_account_screen = QWidget()
        self.login_screen = QWidget()
        self.logged_in_screen = QWidget()
        self.forgot_password_screen = QWidget()

        # subpages for exporting data
        self.create_PDF_screen = QWidget()
        self.export_to_spreadsheet_screen = QWidget()

        # adding pages to the stacked widget
        self.stacked_widget.addWidget(self.home_screen)  # the index for stack_widget is 0
        self.stacked_widget.addWidget(self.calc_my_GPA_homepage)  # 1
        self.stacked_widget.addWidget(self.instructions_screen)  # 2
        self.stacked_widget.addWidget(self.FAQ_screen_1)  # 3
        self.stacked_widget.addWidget(self.settings_screen)  # 4
        self.stacked_widget.addWidget(self.account_settings_homepage)  # 5
        self.stacked_widget.addWidget(self.export_data_homepage)  # 6
        self.stacked_widget.addWidget(self.quarterly_GPA_screen)  # 7
        self.stacked_widget.addWidget(self.cumulative_GPA_screen)  # 8
        self.stacked_widget.addWidget(self.year_8_screen)  # 9
        self.stacked_widget.addWidget(self.year_9_screen)  # 10
        self.stacked_widget.addWidget(self.year_10_screen)  # 11
        self.stacked_widget.addWidget(self.year_11_screen)  # 12
        self.stacked_widget.addWidget(self.year_12_screen)  # 13
        self.stacked_widget.addWidget(self.create_account_screen)  # 14
        self.stacked_widget.addWidget(self.login_screen)  # 15
        self.stacked_widget.addWidget(self.logged_in_screen)  # 16
        self.stacked_widget.addWidget(self.forgot_password_screen)  # 17
        self.stacked_widget.addWidget(self.create_PDF_screen)  # 18
        self.stacked_widget.addWidget(self.export_to_spreadsheet_screen)  # 19

        # the page numbers are defined here. This is done automatically, but these identifiers will be used to help with program readability
        # any identifiers in capital letters will be these used for self.change_screen()
        self.HOME_SCREEN = 0
        self.CALC_MY_GPA_HOMEPAGE = 1
        self.INSTRUCTIONS_SCREEN = 2
        self.FAQ_SCREEN_1 = 3
        self.SETTINGS_SCREEN = 4
        self.ACCOUNT_SETTINGS_HOMEPAGE = 5
        self.EXPORT_DATA_HOMEPAGE = 6

        self.QUARTERLY_GPA_SCREEN = 7
        self.CUMULATIVE_GPA_SCREEN = 8
        self.YEAR_8_SCREEN = 9
        self.YEAR_9_SCREEN = 10
        self.YEAR_10_SCREEN = 11
        self.YEAR_11_SCREEN = 12
        self.YEAR_12_SCREEN = 13

        self.CREATE_ACCOUNT_SCREEN = 14
        self.LOGIN_SCREEN = 15
        self.LOGGED_IN_SCREEN = 16
        self.FORGOT_PASSWORD_SCREEN = 17
        self.CREATE_PDF_SCREEN = 18
        self.EXPORT_TO_SPREADSHEET_SCREEN = 19

        # here, we call all the functions that create widgets. The contents of each function could be in the init function, but they are in separate functions for readability

        self.create_home_screen()

        # from home screen
        self.create_GPA_calculator_home_screen()
        self.create_instructions_screen()
        self.create_FAQ_screen()
        self.create_settings_screen()
        self.create_account_settings_screen()
        self.create_export_data_screen()

        # from Calculate my GPA screen
        self.create_quarterly_GPA_screen()
        self.create_cumulative_GPA_screen()
        self.create_year_8_screen()
        self.create_year_9_screen()
        self.create_year_10_screen()
        self.create_year_11_screen()
        self.create_year_12_screen()

        # from account settings screen
        self.create_create_account_screen()
        self.create_login_screen()
        self.create_logged_in_screen()
        self.create_forgot_password_screen()

        # from export data screen
        self.create_create_PDF_screen()
        self.create_export_to_spreadsheet_screen()

        # setting the initial page to the home screen
        self.stacked_widget.setCurrentIndex(self.HOME_SCREEN)

        # change the colors by default
        self.change_colors_func(first=True)

        # note that the performance time of making the error signs is about .2 seconds
        self.error_signs_line_edits = []  # list with the labels

        for i in range(350):
            error_sign = QLabel()  # start off by making a label
            error_sign.setPixmap(QPixmap("error_sign.png"))
            error_sign.setStyleSheet("background-color: rgba(0, 0, 0, 0);")  # Make the label background transparent
            self.error_signs_line_edits.append(error_sign)
        self.error_sign_number_line_edits = 0  # this will determine which error sign to use

        # separate lists are required for combo boxes and line edits to prevent errors
        self.error_signs_combo_boxes = []  # list with the labels
        for i in range(350):
            error_sign = QLabel()  # start off by making a label
            error_sign.setPixmap(QPixmap("error_sign.png"))
            error_sign.setStyleSheet("background-color: rgba(0, 0, 0, 0);")  # Make the label background transparent
            self.error_signs_combo_boxes.append(error_sign)
        self.error_sign_number_combo_boxes = 0  # this will determine which error sign to use

        self.validation_timer = QTimer(self)
        self.validation_timer.timeout.connect(self.input_validation)
        self.validation_timer.start(250)  # maybe lower this

        # this starts the input_validation function, which will always be running in the background

    def create_back_button(self, screen, new_screen):
        """This creates a back button"""
        self.back_button = QPushButton("Back", screen)  # creating the widget
        self.font_size(self.back_button, 15)  # change the size
        self.back_button.clicked.connect(lambda: self.change_screen(new_screen))  # connecting the button
        self.back_button.show()  # this is required for some screens

    def create_hover_help_text(self, widget, text, scroll_area=None):
        """This function allows help text to be displayed when the user hovers over certain widgets"""
        self.hover_label = QLabel("", self)  # creating the label that will display the help text
        self.hover_label.hide()  # making sure it isn't on screen when not needed

        # each event filter will have a unique string
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=100))
        # creating an instance of the HoverEventFilter class
        event_filter = HoverEventFilter(self.hover_label, text, widget, self.color_1, self.color_2, scroll_area)
        # installing the event_filter
        widget.installEventFilter(event_filter)

        # Assigning event_filter to a dynamic attribute name
        setattr(self, random_string, event_filter)

    def center_widget(self, widget, y, side=None):
        """This function centers a widget"""
        x = None  # prevent a useless Pycharm error
        if side is None:  # most widgets
            # sizeHint() is used as width() isn't determined if the widget isn't on screen
            x = 300 - (widget.sizeHint().width() / 2)  # center
        elif side == "left":  # center left
            x = 150 - (widget.sizeHint().width() / 2)
        elif side == "right":  # center right
            x = 450 - (widget.sizeHint().width() / 2)
        widget.move(x, y)  # move the widget

    def font_size(self, label, size):
        """This function changes the font of widgets"""
        font = QFont()  # make the font a Pyside6 standard
        font.setPointSize(size)  # set the font to the given size
        label.setFont(font)

    def change_screen(self, new_screen):
        """This function changes the screen based on user input"""
        self.stacked_widget.setCurrentIndex(new_screen)

    def create_home_screen(self):
        """This function creates elements for the home screen"""
        # most widgets in this program are defined as widget_name("Text", screen)

        # top labels
        self.home_screen_top_text_line_1 = QLabel("Welcome to the GPA Calculator", self.home_screen)
        self.font_size(self.home_screen_top_text_line_1, 20)  # this changes the font size of the widget. The parameters are (label_name, size).
        self.center_widget(self.home_screen_top_text_line_1, 20)  # this centers the widget. The parameters are (label_name, y)

        self.home_screen_top_text_line_2 = QLabel("Use this tool to calculate your GPA at Monroe-Woodbury High School", self.home_screen)
        self.font_size(self.home_screen_top_text_line_2, 12)
        self.center_widget(self.home_screen_top_text_line_2, 70)

        # buttons
        # open GPA calculator
        self.open_calc_my_GPA_screen_button = QPushButton("Calculate my GPA", self.home_screen)
        self.create_hover_help_text(self.open_calc_my_GPA_screen_button, "Click here to Calculate your GPA")  # when the user hovers over this widget, the text will appear
        self.font_size(self.open_calc_my_GPA_screen_button, 15)
        self.center_widget(self.open_calc_my_GPA_screen_button, 100)
        # the change_screen function changes the index of the stacked widget
        self.open_calc_my_GPA_screen_button.clicked.connect(lambda: self.change_screen(self.CALC_MY_GPA_HOMEPAGE))
        # self.CALC_MY_GPA_HOMEPAGE is in caps to differentiate the indexes for the stacked widget from the QWidgets

        # open instructions menu
        self.open_instructions_menu_button = QPushButton("Instructions", self.home_screen)
        self.create_hover_help_text(self.open_instructions_menu_button, "Click here for instructions on using the program")
        self.font_size(self.open_instructions_menu_button, 15)
        self.center_widget(self.open_instructions_menu_button, 150)
        self.open_instructions_menu_button.clicked.connect(lambda: self.change_screen(self.INSTRUCTIONS_SCREEN))

        # open FAQ screen
        self.open_FAQ_screen_button = QPushButton("Frequently Asked Questions", self.home_screen)
        self.create_hover_help_text(self.open_FAQ_screen_button, "Click here for view Frequently Asked Questions")
        self.font_size(self.open_FAQ_screen_button, 15)
        self.center_widget(self.open_FAQ_screen_button, 200)
        self.open_FAQ_screen_button.clicked.connect(lambda: self.change_screen(self.FAQ_SCREEN_1))

        # open settings
        self.settings_button = QPushButton("Settings", self.home_screen)
        self.create_hover_help_text(self.settings_button, "The Settings menu allows you to change default term weights, \n"
                                                          "weights for advanced classes, and the colors of the program")
        self.font_size(self.settings_button, 15)
        self.center_widget(self.settings_button, 250)
        self.settings_button.clicked.connect(lambda: self.change_screen(self.SETTINGS_SCREEN))

        # open account settings
        self.account_settings_button = QPushButton("Account Settings", self.home_screen)
        self.create_hover_help_text(self.account_settings_button, "Click here to create or log into an account")
        self.font_size(self.account_settings_button, 15)
        self.center_widget(self.account_settings_button, 300)
        self.account_settings_button.clicked.connect(lambda: self.change_screen(self.ACCOUNT_SETTINGS_HOMEPAGE))

        # import local data. This is the only button on the home screen that doesn't open a page
        self.import_local_data_button = QPushButton("Import Local Data", self.home_screen)
        self.create_hover_help_text(self.import_local_data_button, "Click here to import your locally-saved data")
        self.font_size(self.import_local_data_button, 15)
        self.center_widget(self.import_local_data_button, 350)
        self.import_local_data_button.clicked.connect(self.import_local_data_func)

        # open export data screen
        self.export_data_button = QPushButton("Export Data", self.home_screen)
        self.create_hover_help_text(self.export_data_button, "Click here to create a PDF or an Excel spreadsheet of your dad")
        self.font_size(self.export_data_button, 15)
        self.center_widget(self.export_data_button, 400)
        self.export_data_button.clicked.connect(lambda: self.change_screen(self.EXPORT_DATA_HOMEPAGE))

    def create_GPA_calculator_home_screen(self):
        """This function creates the elements for the GPA calculator home screen"""

        # back button
        self.create_back_button(self.calc_my_GPA_homepage, self.HOME_SCREEN)

        # top label
        self.GPA_calculator_home_screen_top_text = QLabel("Choose Scope of GPA", self.calc_my_GPA_homepage)
        self.font_size(self.GPA_calculator_home_screen_top_text, 20)
        self.center_widget(self.GPA_calculator_home_screen_top_text, 20)

        # buttons
        # this button opens the Quarterly/Annual GPA Screen
        self.open_quarterly_screen = QPushButton("Quarterly/Annual", self.calc_my_GPA_homepage)
        self.create_hover_help_text(self.open_quarterly_screen, "Click here to calculate your GPA for one quarter or for one year")
        self.font_size(self.open_quarterly_screen, 15)
        self.center_widget(self.open_quarterly_screen, 80)
        self.open_quarterly_screen.clicked.connect(lambda: self.change_screen(self.QUARTERLY_GPA_SCREEN))

        # this button opens the cumulative GPA screen
        self.open_cumulative_screen = QPushButton("Cumulative", self.calc_my_GPA_homepage)
        self.create_hover_help_text(self.open_cumulative_screen, "Click here to calculate your GPA for the entirety of high school, \n"
                                                                 "including High School classes taken in Middle School")
        self.font_size(self.open_cumulative_screen, 15)
        self.center_widget(self.open_cumulative_screen, 130)
        self.open_cumulative_screen.clicked.connect(lambda: self.change_screen(self.CUMULATIVE_GPA_SCREEN))

    def create_quarterly_GPA_screen(self):
        """This function creates the elements for the Quarterly GPA"""

        # back button
        self.create_back_button(self.quarterly_GPA_screen, self.CALC_MY_GPA_HOMEPAGE)

        # widgets at the top
        self.quarterly_top_text_lines_1_2 = QLabel("Fill in the information as requested \n"
                                                   "Add new classes as needed",
                                                   self.quarterly_GPA_screen)
        self.quarterly_top_text_lines_1_2.setAlignment(Qt.AlignCenter)
        self.font_size(self.quarterly_top_text_lines_1_2, 10)
        self.center_widget(self.quarterly_top_text_lines_1_2, 20)

        self.quarterly_top_text_line_3 = QLabel("When you are ready, click Calculate my GPA "
                                                "for your weighted and unweighted GPA",
                                                self.quarterly_GPA_screen)
        self.font_size(self.quarterly_top_text_line_3, 10)
        self.center_widget(self.quarterly_top_text_line_3, 58)

        # widgets for changing GPA scale
        self.change_GPA_scale_label_quarterly = QLabel(f"Scale: {self.GPA_scale}", self.quarterly_GPA_screen)
        self.create_hover_help_text(self.change_GPA_scale_label_quarterly,
                                    "Monroe-Woodbury uses the 100.0 scale, but the 4.0 scale is provided \n"
                                    "if users wish to compare their GPA to those of other schools")
        self.font_size(self.change_GPA_scale_label_quarterly, 10)
        self.change_GPA_scale_label_quarterly.move(230, 85)

        self.change_GPA_scale_button_quarterly = QPushButton("Change", self.quarterly_GPA_screen)
        self.font_size(self.change_GPA_scale_button_quarterly, 10)
        self.change_GPA_scale_button_quarterly.move(305, 81)
        self.change_GPA_scale_button_quarterly.clicked.connect(self.change_GPA_scale_func)

        # create labels above the line edits
        self.create_line_edit_descriptive_labels(self.quarterly_GPA_screen)

        # there is no stop for the class line edits in this function. At first, there are no class line edits in the program

        # GPA labels at the bottom of the screen
        self.quarterly_unweighted_GPA_label = QLabel(f"Unweighted GPA: {self.unweighted_gpa}",
                                                     self.quarterly_GPA_screen)
        self.create_hover_help_text(self.quarterly_unweighted_GPA_label, "Your Quarterly/Annual unweighted GPA")
        self.font_size(self.quarterly_unweighted_GPA_label, 10)
        self.center_widget(self.quarterly_unweighted_GPA_label, 450)

        self.quarterly_weighted_GPA_label = QLabel(f"Weighted GPA: {self.weighted_gpa}", self.quarterly_GPA_screen)
        self.create_hover_help_text(self.quarterly_weighted_GPA_label, "Your Quarterly/Annual weighted GPA")
        self.font_size(self.quarterly_weighted_GPA_label, 10)
        self.center_widget(self.quarterly_weighted_GPA_label, 470)

        # this is the scroll area for the classes
        # unlike with the scroll area for the instructions and FAQ menu, only one QWidget is needed as these are within other QWidgets, not the entire screen
        self.quarterly_scroll_area_QWidget = QWidget()
        self.quarterly_scroll_area_QWidget.setFixedSize(415, 10000)
        self.quarterly_scroll_area_QWidget.setObjectName("quarterly_scroll_area_QWidget")

        self.quarterly_classes_scroll_area = QScrollArea(self.quarterly_GPA_screen)
        self.quarterly_classes_scroll_area.setWidget(self.quarterly_scroll_area_QWidget)
        self.quarterly_classes_scroll_area.setWidgetResizable(True)
        self.quarterly_classes_scroll_area.setGeometry(92, 150, 440, 300)

        # buttons
        # adding a class
        self.quarterly_add_class_button = QPushButton("Add New Class", self.quarterly_GPA_screen)
        self.font_size(self.quarterly_add_class_button, 15)
        self.quarterly_add_class_button.move(140, 490)
        self.quarterly_add_class_button.clicked.connect(lambda: self.add_class_func(self.quarterly_GPA_screen))

        # deleting a class
        self.quarterly_delete_class_button = QPushButton("Delete Class", self.quarterly_GPA_screen)
        self.font_size(self.quarterly_delete_class_button, 15)
        self.quarterly_delete_class_button.move(150, 535)
        self.quarterly_delete_class_button.clicked.connect(lambda: self.delete_class_func(self.quarterly_GPA_screen))

        # button for calculating the GPA
        self.quarterly_calculate_GPA_button = QPushButton("Calculate my GPA", self.quarterly_GPA_screen)
        self.font_size(self.quarterly_calculate_GPA_button, 15)
        self.quarterly_calculate_GPA_button.move(320, 490)
        self.quarterly_calculate_GPA_button.clicked.connect(lambda: self.calculate_my_GPA_func("Quarterly"))

    def create_cumulative_GPA_screen(self):
        """This function creates the elements for the cumulative home screen"""

        # back button
        self.create_back_button(self.cumulative_GPA_screen, self.CALC_MY_GPA_HOMEPAGE)

        # top text
        self.cumulative_top_text_lines_1_2 = QLabel(
            "Fill in the information in each grade as requested \nAdd new classes as needed",
            self.cumulative_GPA_screen)
        self.cumulative_top_text_lines_1_2.setAlignment(Qt.AlignCenter)
        self.font_size(self.cumulative_top_text_lines_1_2, 10)
        self.center_widget(self.cumulative_top_text_lines_1_2, 20)

        self.cumulative_top_text_line_3 = QLabel(
            "When you are ready, click Calculate my GPA for your weighted and unweighted cumulative GPA",
            self.cumulative_GPA_screen)
        self.font_size(self.cumulative_top_text_line_3, 10)
        self.center_widget(self.cumulative_top_text_line_3, 58)

        # widgets for changing GPA scale. This is similar to quarterly GPA but is repeated as the widgets need different names
        # the scale will be the same for both cumulative and quarterly
        self.change_GPA_scale_label_cumulative = QLabel(f"Scale: {self.GPA_scale}", self.cumulative_GPA_screen)
        self.create_hover_help_text(self.change_GPA_scale_label_cumulative,
                                    "Monroe-Woodbury uses the 100.0 scale, but the 4.0 scale is provided \n"
                                    "if users wish to compare their GPA to those of other schools")
        self.font_size(self.change_GPA_scale_label_cumulative, 10)
        self.change_GPA_scale_label_cumulative.move(230, 85)

        self.change_GPA_scale_button_cumulative = QPushButton("Change", self.cumulative_GPA_screen)
        self.font_size(self.change_GPA_scale_button_cumulative, 10)
        self.change_GPA_scale_button_cumulative.move(305, 81)
        self.change_GPA_scale_button_cumulative.clicked.connect(self.change_GPA_scale_func)

        # this creates the text on top of each button to enter classes for a grade
        for grade, name, y, side in [(8, "year_8_label", 130, "left"), (9, "year_9_label", 130, "right"),
                                     (10, "year_10_label", 280, "left"), (11, "year_11_label", 280, "right"),
                                     (12, "year_12_label", 430, "left")]:
            self.name = QLabel(f"{grade}th Grade", self.cumulative_GPA_screen)  # creates the label
            self.font_size(self.name, 10)
            self.center_widget(self.name, y, side=side)  # the side parameter centers it about the given side
            if grade == 8:  # for 8th grade, the program specifies the classes to enter
                self.create_hover_help_text(self.name, "Only enter Algebra I, Biology, and World Language")

        # buttons to open the screen to enter classes for each grade
        # 8th Grade
        self.open_8th_grade_button = QPushButton("Open", self.cumulative_GPA_screen)
        self.open_8th_grade_button.clicked.connect(lambda: self.change_screen(self.YEAR_8_SCREEN))
        self.font_size(self.open_8th_grade_button, 30)
        self.center_widget(self.open_8th_grade_button, 160, side="left")

        # 9th Grade
        self.open_9th_grade_button = QPushButton("Open", self.cumulative_GPA_screen)
        self.open_9th_grade_button.clicked.connect(lambda: self.change_screen(self.YEAR_9_SCREEN))
        self.font_size(self.open_9th_grade_button, 30)
        self.center_widget(self.open_9th_grade_button, 160, side="right")

        # 10th Grade
        self.open_10th_grade_button = QPushButton("Open", self.cumulative_GPA_screen)
        self.open_10th_grade_button.clicked.connect(lambda: self.change_screen(self.YEAR_10_SCREEN))
        self.font_size(self.open_10th_grade_button, 30)
        self.center_widget(self.open_10th_grade_button, 310, side="left")

        # 11th Grade
        self.open_11th_grade_button = QPushButton("Open", self.cumulative_GPA_screen)
        self.open_11th_grade_button.clicked.connect(lambda: self.change_screen(self.YEAR_11_SCREEN))
        self.font_size(self.open_11th_grade_button, 30)
        self.center_widget(self.open_11th_grade_button, 310, side="right")

        # 12th Grade
        self.open_12th_grade_button = QPushButton("Open", self.cumulative_GPA_screen)
        self.open_12th_grade_button.clicked.connect(lambda: self.change_screen(self.YEAR_12_SCREEN))
        self.font_size(self.open_12th_grade_button, 30)
        self.center_widget(self.open_12th_grade_button, 460, side="left")

        # widgets for calculating GPA
        # button for calculating GPA
        self.cumulative_calculate_GPA_button = QPushButton("Calculate my GPA", self.cumulative_GPA_screen)
        self.cumulative_calculate_GPA_button.clicked.connect(lambda: self.calculate_my_GPA_func("Cumulative"))
        self.font_size(self.cumulative_calculate_GPA_button, 15)
        self.center_widget(self.cumulative_calculate_GPA_button, 460, side="right")

        # labels for displaying the GPA
        self.cumulative_unweighted_GPA_label = QLabel(f"Unweighted GPA: {self.unweighted_gpa}",
                                                      self.cumulative_GPA_screen)
        self.create_hover_help_text(self.cumulative_unweighted_GPA_label, "Your cumulative unweighted GPA")
        self.font_size(self.cumulative_unweighted_GPA_label, 15)
        self.cumulative_unweighted_GPA_label.move(350, 500)

        self.cumulative_weighted_GPA_label = QLabel(f"Weighted GPA: {self.weighted_gpa}", self.cumulative_GPA_screen)
        self.create_hover_help_text(self.cumulative_weighted_GPA_label, "Your cumulative weighted GPA")
        self.font_size(self.cumulative_weighted_GPA_label, 15)
        self.cumulative_weighted_GPA_label.move(360, 530)

    def create_year_x_screen(self, year: int, year_screen: QWidget):
        """This function creates the screen for each year's (8, 9, etc.) screen"""

        # back button
        self.create_back_button(year_screen, self.CUMULATIVE_GPA_SCREEN)

        top_label = QLabel(f"{year}th Grade", year_screen)
        self.font_size(top_label, 30)
        self.center_widget(top_label, 10)

        # creates labels over the line edits
        self.create_line_edit_descriptive_labels(year_screen)

        # buttons at bottom
        add_class_button = QPushButton("Add New Class", year_screen)
        add_class_button.clicked.connect(lambda: self.add_class_func(year_screen))
        self.font_size(add_class_button, 20)
        add_class_button.move(125, 540)

        delete_class_button = QPushButton("Delete Class", year_screen)
        delete_class_button.clicked.connect(lambda: self.delete_class_func(year_screen))
        self.font_size(delete_class_button, 20)
        delete_class_button.move(325, 540)

    def create_year_8_screen(self):
        """This function creates the elements for the 8th Grade screen, mainly the scroll area"""

        # create most of the screen
        self.create_year_x_screen(8, self.year_8_screen)

        # the names of the widgets for the scroll area are referenced later in the program.
        # Because of that, it is easier if they are defined here, not in the function with everything else
        self.year_8_scroll_area_QWidget = QWidget()
        self.year_8_scroll_area_QWidget.setFixedSize(370, 10000)
        self.year_8_scroll_area_QWidget.setObjectName("cumulative_scroll_area_QWidget")

        self.year_8_scroll_area = QScrollArea(self.year_8_screen)
        self.change_color_new(self.year_8_scroll_area, "QScrollArea")
        self.year_8_scroll_area.setWidget(self.year_8_scroll_area_QWidget)
        self.year_8_scroll_area.setWidgetResizable(True)
        self.year_8_scroll_area.setGeometry(115, 110, 390, 420)

    def create_year_9_screen(self):
        """This function creates the elements for the 9th Grade screen, mainly the scroll area"""

        # create most of the screen
        self.create_year_x_screen(9, self.year_9_screen)

        # the names of the widgets for the scroll area are referenced later in the program.
        # Because of that, it is easier if they are defined here, not in the function with everything else
        self.year_9_scroll_area_QWidget = QWidget()
        self.year_9_scroll_area_QWidget.setFixedSize(370, 10000)
        self.year_9_scroll_area_QWidget.setObjectName("cumulative_scroll_area_QWidget")

        self.year_9_scroll_area = QScrollArea(self.year_9_screen)
        self.change_color_new(self.year_9_scroll_area, "QScrollArea")
        self.year_9_scroll_area.setWidget(self.year_9_scroll_area_QWidget)
        self.year_9_scroll_area.setWidgetResizable(True)
        self.year_9_scroll_area.setGeometry(115, 110, 390, 420)

    def create_year_10_screen(self):
        """This function creates the elements for the 10th Grade screen, mainly the scroll area"""

        # create most of the screen
        self.create_year_x_screen(10, self.year_10_screen)

        # the names of the widgets for the scroll area are referenced later in the program.
        # Because of that, it is easier if they are defined here, not in the function with everything else
        self.year_10_scroll_area_QWidget = QWidget()
        self.year_10_scroll_area_QWidget.setFixedSize(370, 10000)
        self.year_10_scroll_area_QWidget.setObjectName("cumulative_scroll_area_QWidget")

        self.year_10_scroll_area = QScrollArea(self.year_10_screen)
        self.change_color_new(self.year_10_scroll_area, "QScrollArea")
        self.year_10_scroll_area.setWidget(self.year_10_scroll_area_QWidget)
        self.year_10_scroll_area.setWidgetResizable(True)
        self.year_10_scroll_area.setGeometry(115, 110, 390, 420)

    def create_year_11_screen(self):
        """This function creates the elements for the 11th Grade screen, mainly the scroll area"""

        # create most of the screen
        self.create_year_x_screen(11, self.year_11_screen)

        # the names of the widgets for the scroll area are referenced later in the program.
        # Because of that, it is easier if they are defined here, not in the function with everything else
        self.year_11_scroll_area_QWidget = QWidget()
        self.year_11_scroll_area_QWidget.setFixedSize(370, 10000)
        self.year_11_scroll_area_QWidget.setObjectName("cumulative_scroll_area_QWidget")

        self.year_11_scroll_area = QScrollArea(self.year_11_screen)
        self.change_color_new(self.year_11_scroll_area, "QScrollArea")
        self.year_11_scroll_area.setWidget(self.year_11_scroll_area_QWidget)
        self.year_11_scroll_area.setWidgetResizable(True)
        self.year_11_scroll_area.setGeometry(115, 110, 390, 420)

    def create_year_12_screen(self):
        """This function creates the elements for the 12th Grade screen, mainly the scroll area"""

        # create most of the screen
        self.create_year_x_screen(12, self.year_12_screen)

        # the names of the widgets for the scroll area are referenced later in the program.
        # Because of that, it is easier if they are defined here, not in the function with everything else
        self.year_12_scroll_area_QWidget = QWidget()
        self.year_12_scroll_area_QWidget.setFixedSize(370, 10000)
        self.year_12_scroll_area_QWidget.setObjectName("cumulative_scroll_area_QWidget")

        self.year_12_scroll_area = QScrollArea(self.year_12_screen)
        self.change_color_new(self.year_12_scroll_area, "QScrollArea")
        self.year_12_scroll_area.setWidget(self.year_12_scroll_area_QWidget)
        self.year_12_scroll_area.setWidgetResizable(True)
        self.year_12_scroll_area.setGeometry(115, 110, 390, 420)

    def add_class_func(self, screen):
        """This function adds a new class"""
        class_scope = "Cumulative"  # if the class will be cumulative or quarterly
        year = ""  # determined automatically for cumulative, based on user input for quarterly
        line_edits = scroll_area_QWidget = None  # line edits_ refers to the line_edits list, scroll_area_widget is the scroll_area_widget
        if screen == self.quarterly_GPA_screen:
            line_edits = self.quarterly_class_line_edits
            scroll_area_QWidget = self.quarterly_scroll_area_QWidget
            class_scope = "Quarterly"  # change the class_scope here but nowhere else
            # the year remains an empty string
        elif screen == self.year_8_screen:
            line_edits = self.year_8_class_line_edits
            scroll_area_QWidget = self.year_8_scroll_area_QWidget
            year = 8  # the year is the year of the screen
        elif screen == self.year_9_screen:
            line_edits = self.year_9_class_line_edits
            scroll_area_QWidget = self.year_9_scroll_area_QWidget
            year = 9
        elif screen == self.year_10_screen:
            line_edits = self.year_10_class_line_edits
            scroll_area_QWidget = self.year_10_scroll_area_QWidget
            year = 10
        elif screen == self.year_11_screen:
            line_edits = self.year_11_class_line_edits
            scroll_area_QWidget = self.year_11_scroll_area_QWidget
            year = 11
        elif screen == self.year_12_screen:
            line_edits = self.year_12_class_line_edits
            scroll_area_QWidget = self.year_12_scroll_area_QWidget
            year = 12

        y_offset = len(line_edits) * 30  # the y_offset for each class within the scroll_area is the amount of classes times 30

        # Create line edits
        # rather than setting it to the screen, the line_edits are set to the scroll area QWidget
        class_name_line_edit = QLineEdit(scroll_area_QWidget)
        # the Objectname is needed for input validation as unlike most line_edits,
        # the class name doesn't get any input validation
        class_name_line_edit.setObjectName("no_input_validation")
        grade_line_edit = QLineEdit(scroll_area_QWidget)
        grade_line_edit.setObjectName("grade_line_edit")  # there is specific input validation
        weight_combo_box = ComboBox(scroll_area_QWidget)  # notice this is the ComboBox the program made, not QComboBox
        credit_line_edit = QLineEdit(scroll_area_QWidget)
        credit_line_edit.setObjectName("credit_line_edit")  # there is specific input validation
        more_info_button = QPushButton("More", scroll_area_QWidget)

        # make the year combo box only for the quarterly screen
        if screen == self.quarterly_GPA_screen:
            year_combo_box = ComboBox(scroll_area_QWidget)
            year_combo_box.setObjectName("no_input_validation")
            self.change_color_new(year_combo_box, "ComboBox")  # because the widget isn't made at the start of the program, the colors must be changed
            for item in ["", "8", "9", "10", "11", "12"]:  # each year and a default string is added to the combo box
                year_combo_box.addItem(item)
            year_combo_box.show()
        else:
            year_combo_box = None  # this is done to prevent a useless error in PyCharm

        # making sure each new widget can be seen
        for widget, Type in [(class_name_line_edit, "QLineEdit"), (grade_line_edit, "QLineEdit"), (weight_combo_box, "ComboBox"),
                             (credit_line_edit, "QLineEdit"), (more_info_button, "QPushButton")]:
            self.change_color_new(widget, Type)

        # add options to the weight combo boxes
        for item in ["", "R", "H", "AP"]:
            weight_combo_box.addItem(item)

        # Set the positions of the line edits
        class_name_line_edit.setGeometry(0, y_offset, 150, 25)
        grade_line_edit.setGeometry(160, y_offset, 40, 25)
        weight_combo_box.setGeometry(210, y_offset, 50, 25)
        credit_line_edit.setGeometry(270, y_offset, 40, 25)
        if screen == self.quarterly_GPA_screen:  # only for the quarterly screen
            year_combo_box.setGeometry(320, y_offset, 40, 25)
            more_info_button.setGeometry(370, y_offset, 40, 25)
        else:
            more_info_button.setGeometry(320, y_offset, 40, 25)  # this has a different position than the quarterly screen

        # Keep track of the line edits
        if screen == self.quarterly_GPA_screen:  # includes the year_combo_box
            line_edits.append((self.class_id, class_name_line_edit, grade_line_edit, weight_combo_box,
                               credit_line_edit, year_combo_box, more_info_button))
        else:
            line_edits.append((self.class_id, class_name_line_edit, grade_line_edit, weight_combo_box,
                               credit_line_edit, more_info_button))

        # Show the new line edits
        class_name_line_edit.show()
        grade_line_edit.show()
        weight_combo_box.show()
        credit_line_edit.show()
        more_info_button.show()

        more_info_screen = QWidget()  # this is the screen where users can enter term grades for a more exact GPA
        self.stacked_widget.addWidget(more_info_screen)  # adding it to the stacked_widget
        self.change_color_new(more_info_screen, "QWidget")  # this wasn't created at the start of the program, so the colors must be changed
        MORE_INFO_ID = self.stacked_widget.count() - 1  # this will be used in the change_screen() function

        # creating an instance of the UserClass Python class for this class
        new_class = UserClass(class_id=self.class_id, scope=class_scope, screen=screen, MORE_INFO_ID=MORE_INFO_ID,
                              more_info_screen=more_info_screen, grade_line_edit=grade_line_edit,
                              class_name="", grade="", weight="", credit="", year=year,
                              Q1_weight=self.default_Q1_weight, Q2_weight=self.default_Q2_weight, E2_weight=self.default_E2_weight,
                              Q3_weight=self.default_Q3_weight, Q4_weight=self.default_Q4_weight, E4_weight=self.default_E4_weight,
                              first_time=True)
        self.user_classes.append(new_class)  # adding the new Python class to a list
        # when the more_info_button is pressed, the create_more_info_screen is created and the screen is changed
        more_info_button.clicked.connect(lambda: self.create_more_information_screen(MORE_INFO_ID))
        more_info_button.clicked.connect(lambda: self.change_screen(MORE_INFO_ID))

        # these next lines will create the screens for the more_term_information
        # these screens allow users to enter assignments for each term for an even more exact GPA
        # all of these screens will be scrollable
        # the screen for each term must be done manually as the names of the widgets will be used later

        # Q1
        more_info_screen_Q1 = QWidget()  # this is the main screen
        more_info_scroll_area_Q1_QWidget = QWidget()  # this is the scroll area QWidget that will encompass the entire screen
        more_info_scroll_area_Q1_QWidget.setFixedSize(580, 1070)  # set the size for the screen

        self.more_info_scroll_area_Q1 = QScrollArea(more_info_screen_Q1)  # the actual scroll area
        self.change_color_new(self.more_info_scroll_area_Q1, "QScrollArea")  # because the screen isn't created by default, the color must be changed
        self.more_info_scroll_area_Q1.setWidget(more_info_scroll_area_Q1_QWidget)
        self.more_info_scroll_area_Q1.setWidgetResizable(True)  # the user can scroll through the scroll area
        self.more_info_scroll_area_Q1.setGeometry(0, 0, 600, 600)  # the size of the screen before the user must scroll to see more

        # Q2
        more_info_screen_Q2 = QWidget()
        more_info_scroll_area_Q2_QWidget = QWidget()
        more_info_scroll_area_Q2_QWidget.setFixedSize(580, 1070)

        self.more_info_scroll_area_Q2 = QScrollArea(more_info_screen_Q2)
        self.change_color_new(self.more_info_scroll_area_Q2, "QScrollArea")
        self.more_info_scroll_area_Q2.setWidget(more_info_scroll_area_Q2_QWidget)
        self.more_info_scroll_area_Q2.setWidgetResizable(True)
        self.more_info_scroll_area_Q2.setGeometry(0, 0, 600, 600)

        # E2
        more_info_screen_E2 = QWidget()
        more_info_scroll_area_E2_QWidget = QWidget()
        more_info_scroll_area_E2_QWidget.setFixedSize(580, 1070)

        self.more_info_scroll_area_E2 = QScrollArea(more_info_screen_E2)
        self.change_color_new(self.more_info_scroll_area_E2, "QScrollArea")
        self.more_info_scroll_area_E2.setWidget(more_info_scroll_area_E2_QWidget)
        self.more_info_scroll_area_E2.setWidgetResizable(True)
        self.more_info_scroll_area_E2.setGeometry(0, 0, 600, 600)

        # Q3
        more_info_screen_Q3 = QWidget()
        more_info_scroll_area_Q3_QWidget = QWidget()
        more_info_scroll_area_Q3_QWidget.setFixedSize(580, 1070)

        self.more_info_scroll_area_Q3 = QScrollArea(more_info_screen_Q3)
        self.change_color_new(self.more_info_scroll_area_Q3 , "QScrollArea")
        self.more_info_scroll_area_Q3 .setWidget(more_info_scroll_area_Q3_QWidget)
        self.more_info_scroll_area_Q3 .setWidgetResizable(True)
        self.more_info_scroll_area_Q3 .setGeometry(0, 0, 600, 600)

        # Q4
        more_info_screen_Q4 = QWidget()
        more_info_scroll_area_Q4_QWidget = QWidget()
        more_info_scroll_area_Q4_QWidget.setFixedSize(580, 1070)

        self.more_info_scroll_area_Q4 = QScrollArea(more_info_screen_Q4)
        self.change_color_new(self.more_info_scroll_area_Q4, "QScrollArea")
        self.more_info_scroll_area_Q4.setWidget(more_info_scroll_area_Q4_QWidget)
        self.more_info_scroll_area_Q4.setWidgetResizable(True)
        self.more_info_scroll_area_Q4.setGeometry(0, 0, 600, 600)

        # E4
        more_info_screen_E4 = QWidget()
        more_info_scroll_area_E4_QWidget = QWidget()
        more_info_scroll_area_E4_QWidget.setFixedSize(580, 1070)

        self.more_info_scroll_area_E4 = QScrollArea(more_info_screen_E4)
        self.change_color_new(self.more_info_scroll_area_E4, "QScrollArea")
        self.more_info_scroll_area_E4.setWidget(more_info_scroll_area_E4_QWidget)
        self.more_info_scroll_area_E4.setWidgetResizable(True)
        self.more_info_scroll_area_E4.setGeometry(0, 0, 600, 600)

        # this puts the QWidgets just made into the UserClass instance
        # this will be used in the create_more_information_screen() function
        new_class.more_info_scroll_area_Q1_QWidget = more_info_scroll_area_Q1_QWidget
        new_class.more_info_scroll_area_Q2_QWidget = more_info_scroll_area_Q2_QWidget
        new_class.more_info_scroll_area_E2_QWidget = more_info_scroll_area_E2_QWidget
        new_class.more_info_scroll_area_Q3_QWidget = more_info_scroll_area_Q3_QWidget
        new_class.more_info_scroll_area_Q4_QWidget = more_info_scroll_area_Q4_QWidget
        new_class.more_info_scroll_area_E4_QWidget = more_info_scroll_area_E4_QWidget

        self.stacked_widget.addWidget(more_info_screen_Q1)  # adding the QWidget to the stacked Widget
        self.change_color_new(more_info_screen_Q1, "QWidget")  # changing the color
        MORE_INFO_ID_Q1 = self.stacked_widget.count() - 1  # when used in the change_screen() function, the ID will be the current length of stacked_widget - 1

        self.stacked_widget.addWidget(more_info_screen_Q2)
        self.change_color_new(more_info_screen_Q2, "QWidget")
        MORE_INFO_ID_Q2 = self.stacked_widget.count() - 1

        self.stacked_widget.addWidget(more_info_screen_E2)
        self.change_color_new(more_info_screen_E2, "QWidget")
        MORE_INFO_ID_E2 = self.stacked_widget.count() - 1

        self.stacked_widget.addWidget(more_info_screen_Q3)
        self.change_color_new(more_info_screen_Q3, "QWidget")
        MORE_INFO_ID_Q3 = self.stacked_widget.count() - 1

        self.stacked_widget.addWidget(more_info_screen_Q4)
        self.change_color_new(more_info_screen_Q4, "QWidget")
        MORE_INFO_ID_Q4 = self.stacked_widget.count() - 1

        self.stacked_widget.addWidget(more_info_screen_E4)
        self.change_color_new(more_info_screen_E4, "QWidget")
        MORE_INFO_ID_E4 = self.stacked_widget.count() - 1

        # saves the ID for stacked_widget to the instance of UserClass
        new_class.MORE_INFO_ID_Q1 = MORE_INFO_ID_Q1
        new_class.MORE_INFO_ID_Q2 = MORE_INFO_ID_Q2
        new_class.MORE_INFO_ID_E2 = MORE_INFO_ID_E2
        new_class.MORE_INFO_ID_Q3 = MORE_INFO_ID_Q3
        new_class.MORE_INFO_ID_Q4 = MORE_INFO_ID_Q4
        new_class.MORE_INFO_ID_E4 = MORE_INFO_ID_E4

        self.class_id += 1  # increases the class_id by 1
        self.input_validation()  # this is to ensure the error signs update as soon as the class it made
        # without this, it would take a noticeable amount of the time for the error signs to appear

    def delete_class_func(self, screen):
        """This function deletes a class"""
        line_edits = None  # this will be the list with the line edits
        if screen == self.quarterly_GPA_screen:
            line_edits = self.quarterly_class_line_edits
        elif screen == self.year_8_screen:
            line_edits = self.year_8_class_line_edits
        elif screen == self.year_9_screen:
            line_edits = self.year_9_class_line_edits
        elif screen == self.year_10_screen:
            line_edits = self.year_10_class_line_edits
        elif screen == self.year_11_screen:
            line_edits = self.year_11_class_line_edits
        elif screen == self.year_12_screen:
            line_edits = self.year_12_class_line_edits

        if line_edits:  # if there are any classes for that screen. If there aren't any classes, nothing happenes
            class_edits = line_edits.pop()  # remove the last class
            for class_ in reversed(self.user_classes):  # find the latest class of that screen
                if class_.screen == screen:
                    self.user_classes.remove(class_)  # remove that class from the list
                    break  # ensure that only one class is removes
            for widget in class_edits[1:]:  # not including the class_id
                widget.setParent(None)  # set the screen in None
                widget.deleteLater()  # delete the widget
            self.input_validation()  # this is to ensure the error signs update as soon as the class it made
            # without this, it would take a noticeable amount of the time for the error signs to appear

    def create_line_edit_descriptive_labels(self, screen):
        """This function creates the labels that go above the line edits and combo boxes on the GPA screens"""
        # creating the labels
        class_name_label = QLabel("Class Name", screen)
        grade_label = QLabel("Grade", screen)
        weight_label = QLabel("Weight", screen)
        credit_label = QLabel("Credit", screen)
        if screen == self.quarterly_GPA_screen:  # year is only on quarterly
            year_label = QLabel("Year", screen)
            self.font_size(year_label, 10)
            # help text to affirm that year is optional
            self.create_hover_help_text(year_label, "Enter the grade you were when you took the class. \n"
                                                    "This is optional and will only be used when making this class a cumulative class")
        more_label = QLabel("More", screen)  # above the more button

        # help text for each label
        for label, text in [(class_name_label, "Enter the name of the class"),
                            (grade_label, "Enter the grade you received in the class"),
                            (weight_label, "Enter the weight of the class. \n"
                                           "Weights of Honors/AP classes can be changed in the Settings"),
                            (credit_label, "Enter the credit of the class, usually proportional to length"),
                            (more_label, "This button gives allows you to enter term grades for a more exact GPA")]:
            self.font_size(label, 10)  # setting the font size
            self.create_hover_help_text(label, text)

        if screen == self.quarterly_GPA_screen:  # there's text on top, so this must be lower on the screen
            y = 120
        else:
            y = 80  # for cumulative

        if screen == self.quarterly_GPA_screen:  # placing the labels
            class_name_label.move(132, y)
            grade_label.move(252, y)
            weight_label.move(302, y)
            credit_label.move(362, y)
            year_label.move(412, y)
            more_label.move(462, y)
        else:
            class_name_label.move(155, y)  # placing the labels, different than quarterly
            grade_label.move(275, y)
            weight_label.move(325, y)
            credit_label.move(385, y)
            more_label.move(435, y)

    def change_GPA_scale_func(self):
        """This function changes the GPA scale"""
        if self.GPA_scale == 100.0:  # if the scale was 100.0
            self.GPA_scale = 4.0  # change to 4.0
            self.honors_weight = self.honors_weight_4  # change the weight used when calculating GPA
            self.AP_weight = self.AP_weight_4
        elif self.GPA_scale == 4.0:
            self.GPA_scale = 100.0
            self.honors_weight = self.honors_weight_100
            self.AP_weight = self.AP_weight_100
        self.change_GPA_scale_label_quarterly.setText(f"Scale: {self.GPA_scale}")  # change the text for the label on the Quarterly GPA screen
        self.change_GPA_scale_label_quarterly.adjustSize()  # change the size of the label
        self.change_GPA_scale_label_cumulative.setText(f"Scale: {self.GPA_scale}")  # change the text for the label on the Cumulative GPA screen
        self.change_GPA_scale_label_cumulative.adjustSize()  # change the size of the label

        self.input_validation()  # this is to ensure the error signs update as soon as the class it made
        # without this, it would take a noticeable amount of the time for the error signs to appear

    def update_class_data(self, show_error, from_export=False, scope=None):
        """This updates the class_data. The function is called at various points of the program,
        such as just before calculating GPA or when dynamically saving the program's data to SQL"""
        dont_show_error = False  # this won't show an additional error if a letter grade is used on the 100.0 scale
        if show_error:  # this will be used when the function is called from the Calculate my GPA button
            try:  # if there are any terms that aren't float but should be float, the except will be triggered
                if len(self.user_classes) == 0:  # if there are no classes
                    if not from_export:
                        QMessageBox.critical(self, "Calculating GPA error", "Please enter at least one class")
                    return "error"  # the GPA will not be calculated
                for user_class in self.user_classes:  # all classes
                    for screen in self.all_class_line_edits:  # all line edits
                        for class_ in screen[1]:  # for each class in the screen
                            if float(user_class.class_id) == float(class_[0]) and (user_class.scope == scope or scope == "Both"):  # if this is the correct class, also if it's on the correct scope
                                if class_[2].text() == class_[3].currentText() == class_[4].text() == "":
                                    # if all the relevant fields are empty, update the data but don't throw an error
                                    user_class.class_name = class_[1].text()  # update the class name
                                    user_class.grade = class_[2].text()  # this will be blank
                                    user_class.exact_grade = ""  # if there is an exact grade from the term grades, delete it
                                    user_class.weight = class_[3].currentText()  # this will be blank
                                    user_class.credit = class_[4].text()  # this will be blank
                                    if user_class.scope == "Quarterly":
                                        user_class.year = class_[5].currentText()  # this may not be blank
                                else:
                                    if class_[2].text() in self.letter_to_4:  # if the grade is a letter grade
                                        if self.GPA_scale == 100.0:  # letter grades can't be used on the 100.0 scale
                                            if not from_export:
                                                QMessageBox.critical(self, "Calculating GPA error", "Letter grades can not be used with the 100.0 scale")
                                            dont_show_error = True  # it won't show an additional error
                                            raise ValueError
                                    elif float(class_[2].text()) < 0 or float(class_[2].text()) > 100:  # if the grade is negative or above 100
                                        raise ValueError
                                    if class_[3].currentText() == "" or class_[4].text() == "" or float(class_[4].text()) < 0:
                                        raise ValueError # this will trigger if the weight or credit is invalid
                                    else:
                                        user_class.class_name = class_[1].text()  # saves the class name
                                        if user_class.exact_grade and round(float(user_class.exact_grade)) == float(class_[2].text()):
                                            user_class.grade = user_class.exact_grade  # if there is a grade from the term grades, use that (non-rounded)
                                        else:  # if there is no term grade or the user changed the grade generated from the term grade
                                            user_class.grade = class_[2].text()  # make the grade the text, not the term grade
                                            user_class.exact_grade = ""  # delete the term grade to avoid confusion
                                        if class_[3].currentText() == "R":  # if a regular class
                                            user_class.weight = 1
                                        elif class_[3].currentText() == "H":  # if a honors class
                                            user_class.weight = self.honors_weight
                                        elif class_[3].currentText() == "AP":  # if an AP class
                                            user_class.weight = self.AP_weight
                                        user_class.credit = class_[4].text()  # credit of the class
                                        if user_class.scope == "Quarterly":  # year of the class, only for quarterly
                                            user_class.year = class_[5].currentText()
            except ValueError:
                if not dont_show_error and not from_export:  # if there isn't an error message elsewhere
                    QMessageBox.critical(self, "Calculating GPA error", "Please enter in all fields correctly, including positive numbers and grades less than or equal to 100.")
                return "error"
        else:  # this is used for most cases besides the Calculate my GPA button
            for user_class in self.user_classes:
                for screen in self.all_class_line_edits:
                    for class_ in screen[1]:
                        if float(user_class.class_id) == float(class_[0]):
                            user_class.class_name = class_[1].text()
                            user_class.grade = class_[2].text()  # if the input is invalid, the program doesn't care (it won't cause an error)
                            user_class.weight = class_[3].currentText()
                            user_class.credit = class_[4].text()
                            if user_class.scope == "Quarterly":
                                user_class.year = class_[5].currentText()
        if from_export:  # this returns an error for exporting data if there are no classes for that scope
            new_classes = []
            for class_ in self.user_classes:
                if scope == "Both":
                    new_classes.append(class_)
                elif (class_.scope == scope or class_.scope == "Both") and class_.grade != "":
                    new_classes.append(class_)
            if not new_classes:
                return "error"

    def calculate_my_GPA_func(self, scope, from_export=False):
        runnable = self.update_class_data(show_error=True, from_export=from_export, scope=scope)
        if runnable == "error":  # if there isn't an error
            return "error"  # this is for exporting data
        else:
            new_classes = []
            for user_class in self.user_classes:
                if (user_class.scope == scope or user_class.scope == "Both") and user_class.grade != "":
                    new_classes.append(user_class)  # only classes in the specified scope
            if new_classes:  # if there is at least one class
                if float(self.GPA_scale) == 100.0:  # if 100.0 scale
                    # for each class, this appends the grade * credit to a list
                    unweighted_total_grade_list_100 = list(map(lambda user_class: float(user_class.grade) * float(user_class.credit), new_classes))
                    # for each class, this appends the grade * credit * weight to a list
                    weighted_total_grade_list_100 = list(map(lambda user_class: float(user_class.grade) * float(user_class.credit) * float(user_class.weight), new_classes))
                    # for each class, this appends the credit * 100 to a list
                    total_points_available_list_100 = list(map(lambda user_class: 100 * float(user_class.credit), new_classes))
                    # this calculates the GPA to 4 decimal places (what Monroe-Woodbury does)
                    self.unweighted_gpa = "{:.4f}".format(sum(unweighted_total_grade_list_100) / sum(total_points_available_list_100) * 100)
                    self.weighted_gpa = "{:.4f}".format(sum(weighted_total_grade_list_100) / sum(total_points_available_list_100) * 100)
                elif float(self.GPA_scale) == 4.0:  # if 4.0 scale
                    unweighted_total_grade_list_4 = []
                    weighted_total_grade_list_4 = []
                    total_points_available_list_4 = []
                    for user_class in new_classes:
                        if user_class.grade in self.letter_to_4:  # if the grade is a letter grade
                            # this appends the value (0-4) of the letter_grade * the class's credit to a list
                            unweighted_total_grade_list_4.append(self.letter_to_4[user_class.grade] * float(user_class.credit))
                            # this appends the value * credit * weight to a list
                            weighted_total_grade_list_4.append(self.letter_to_4[user_class.grade] * float(user_class.weight) * float(user_class.credit))
                            # thi appends the credit * 4 to a list
                            total_points_available_list_4.append(float(4) * float(user_class.credit))
                        else:
                            for key, value in self.grade_to_letter.items():  # iterates through a pre-made list
                                if round(float(user_class.grade)) in value:  # round is needed or else the program will freeze
                                    # appends the value of the grade (0-4) * credit to a ist
                                    unweighted_total_grade_list_4.append(float(self.letter_to_4[key]) * float(user_class.credit))
                                    # appends the value * credit * weight
                                    weighted_total_grade_list_4.append(float(self.letter_to_4[key]) * float(user_class.credit) * float(user_class.weight))
                                    # appends the credit * 4
                                    total_points_available_list_4.append(float(4) * float(user_class.credit))
                        # the calculates the GPA to 2 decimal places
                        self.unweighted_gpa = "{:.2f}".format(sum(unweighted_total_grade_list_4) / sum(total_points_available_list_4) * 4)
                        self.weighted_gpa = "{:.2f}".format(sum(weighted_total_grade_list_4) / sum(total_points_available_list_4) * 4)
                if scope == "Quarterly":  # the GPA will only be updated for the scope
                    self.quarterly_unweighted_GPA_label.setText(f"Unweighted GPA: {self.unweighted_gpa}")  # change the label
                    self.quarterly_unweighted_GPA_label.adjustSize()  # adjust the size of the label
                    self.quarterly_weighted_GPA_label.setText(f"Weighted GPA: {self.weighted_gpa}")
                    self.quarterly_weighted_GPA_label.adjustSize()
                elif scope == "Cumulative":
                    self.cumulative_unweighted_GPA_label.setText(f"Unweighted GPA: {self.unweighted_gpa}")
                    self.cumulative_unweighted_GPA_label.adjustSize()
                    self.cumulative_weighted_GPA_label.setText(f"Weighted GPA: {self.weighted_gpa}")
                    self.cumulative_weighted_GPA_label.adjustSize()
            else:  # if there are no classes
                QMessageBox.critical(self, "Calculating GPA error", "Please enter at least one class")

    def create_more_information_screen(self, id: int):
        """This creates the elements for more_information screens for each class"""
        self.update_class_data(show_error=False)  # updating the class data
        for Class in self.user_classes:
            if Class.MORE_INFO_ID == id:  # if this is the correct class
                # these next few lines create a back button. Because the variable with the index is not saved
                # in the UserClass instance, they must be manually sorted through
                if Class.screen == self.quarterly_GPA_screen:
                    self.create_back_button(Class.more_info_screen, self.QUARTERLY_GPA_SCREEN)
                elif Class.screen == self.year_8_screen:
                    self.create_back_button(Class.more_info_screen, self.YEAR_8_SCREEN)
                elif Class.screen == self.year_9_screen:
                    self.create_back_button(Class.more_info_screen, self.YEAR_9_SCREEN)
                elif Class.screen == self.year_10_screen:
                    self.create_back_button(Class.more_info_screen, self.YEAR_10_SCREEN)
                elif Class.screen == self.year_11_screen:
                    self.create_back_button(Class.more_info_screen, self.YEAR_11_SCREEN)
                elif Class.screen == self.year_12_screen:
                    self.create_back_button(Class.more_info_screen, self.YEAR_12_SCREEN)

                # top labels
                # display the class name
                more_info_top_class_name = QLabel(f"Class Name: {Class.class_name}", Class.more_info_screen)
                self.font_size(more_info_top_class_name, 15)
                self.center_widget(more_info_top_class_name, 10)

                # display the weight of the class
                more_info_top_weight = QLabel(f"Weight: {Class.weight}", Class.more_info_screen)
                self.font_size(more_info_top_weight, 15)
                self.center_widget(more_info_top_weight, 40)

                # display the credit of the class
                more_info_top_credit = QLabel(f"Credit: {Class.credit}", Class.more_info_screen)
                self.font_size(more_info_top_credit, 15)
                self.center_widget(more_info_top_credit, 70)

                # display the year that the class was taken. This is done automatically for cumulative and based on user input for quarterly
                more_info_top_year = QLabel(f"Year: {Class.year}", Class.more_info_screen)
                self.font_size(more_info_top_year, 15)
                self.center_widget(more_info_top_year, 100)

                # more text
                more_info_information_text = QLabel("The more information screen gives you a more exact GPA.\n "
                                                    "It does this by recording term grades rather than F4 grades.\n "
                                                    "Calculations use unrounded grades rather than rounded ones.",
                                                    Class.more_info_screen)
                more_info_information_text.setAlignment(Qt.AlignCenter)
                self.font_size(more_info_information_text, 10)
                self.center_widget(more_info_information_text, 150)

                # term grade calculator
                # top text for the area
                term_grade_area_top_text = QLabel("Term Grades", Class.more_info_screen)
                self.create_hover_help_text(term_grade_area_top_text, f"This menu allows you to enter your term grades for {Class.class_name} \n"
                                                                       "This allows for a more exact GPA")
                self.font_size(term_grade_area_top_text, 20)
                self.center_widget(term_grade_area_top_text, 225)

                # label on top of the line edits for the grade of each term
                term_grade_label = QLabel("Grade", Class.more_info_screen)
                self.create_hover_help_text(term_grade_label, "Enter the grade you received in the term. \n"
                                                              "If there is a term that you don't have a grade in, leave it blank. \n"
                                                              "Your grade will not factor in empty terms")
                self.font_size(term_grade_label, 10)
                term_grade_label.move(240, 270)

                # label on top of the line edits for the weight of each term
                term_weight_label = QLabel("Weight", Class.more_info_screen)
                self.create_hover_help_text(term_weight_label, "Enter the weight of the term. \n"
                                                               "The defaults can be changed in the settings, but they will only apply for future classes. \n"
                                                               "In addition, if a term grade is blank, the term weight will be zero")
                self.font_size(term_weight_label, 10)
                term_weight_label.move(290, 270)

                # this creates the labels for each term. They can be defined this way as they don't need to be referenced again
                for name, text, y in [("Q1_label", "Q1:", 300), ("Q2_label", "Q2:", 330),
                                      ("E2_label", "E2:", 360), ("Q3_label", "Q3:", 390),
                                      ("Q4_label", "Q4:", 420), ("E4_label", "E4:", 450)]:
                    name = QLabel(text, Class.more_info_screen)
                    self.font_size(name, 10)
                    name.move(210, y)
                    self.change_color_new(name, "QLabel")

                # making the line edits for each class
                Q1_grade_line_edit = QLineEdit(Class.more_info_screen)
                Q2_grade_line_edit = QLineEdit(Class.more_info_screen)
                E2_grade_line_edit = QLineEdit(Class.more_info_screen)
                Q3_grade_line_edit = QLineEdit(Class.more_info_screen)
                Q4_grade_line_edit = QLineEdit(Class.more_info_screen)
                E4_grade_line_edit = QLineEdit(Class.more_info_screen)

                # placing the line edits and changing their color
                for name, y in [(Q1_grade_line_edit, 300),
                                (Q2_grade_line_edit, 330),
                                (E2_grade_line_edit, 360),
                                (Q3_grade_line_edit, 390),
                                (Q4_grade_line_edit, 420),
                                (E4_grade_line_edit, 450)]:
                    name.setGeometry(240, y, 40, 20)
                    name.setObjectName("none_or_float")  # needed for input validation
                    self.change_color_new(name, "QLineEdit")

                if not Class.first_time:  # if this isn't the first time the more information screen has been opened, insert the text that was there previously
                    # this needs to be done as the screen is deleted everytime it is closed
                    for name, text in [(Q1_grade_line_edit, Class.Q1_grade_line_edit.text()),
                                       (Q2_grade_line_edit, Class.Q2_grade_line_edit.text()),
                                       (E2_grade_line_edit, Class.E2_grade_line_edit.text()),
                                       (Q3_grade_line_edit, Class.Q3_grade_line_edit.text()),
                                       (Q4_grade_line_edit, Class.Q4_grade_line_edit.text()),
                                       (E4_grade_line_edit, Class.E4_grade_line_edit.text())]:
                        name.setText(text)

                # add the line edits to the class. The [1] is needed and [0] is "term" for when the line_edits are iterated through
                Class.Q1_grade_line_edit = Q1_grade_line_edit
                Class.Q2_grade_line_edit = Q2_grade_line_edit
                Class.E2_grade_line_edit = E2_grade_line_edit
                Class.Q3_grade_line_edit = Q3_grade_line_edit
                Class.Q4_grade_line_edit = Q4_grade_line_edit
                Class.E4_grade_line_edit = E4_grade_line_edit

                # creating the weight lin edits
                Q1_weight_line_edit = QLineEdit(Class.more_info_screen)
                Q2_weight_line_edit = QLineEdit(Class.more_info_screen)
                E2_weight_line_edit = QLineEdit(Class.more_info_screen)
                Q3_weight_line_edit = QLineEdit(Class.more_info_screen)
                Q4_weight_line_edit = QLineEdit(Class.more_info_screen)
                E4_weight_line_edit = QLineEdit(Class.more_info_screen)

                # placing the weight line edits. The default text is the weight of that term
                for name, text, y in [(Q1_weight_line_edit, Class.Q1_weight, 300),
                                (Q2_weight_line_edit, Class.Q2_weight, 330),
                                (E2_weight_line_edit, Class.E2_weight, 360),
                                (Q3_weight_line_edit, Class.Q3_weight, 390),
                                (Q4_weight_line_edit, Class.Q4_weight, 420),
                                (E4_weight_line_edit, Class.E4_weight, 450)]:
                    name.setGeometry(290, y, 40, 20)
                    name.setText(str(text))
                    self.change_color_new(name, "QLineEdit")

                if not Class.first_time:
                    # like with grade_line_edits, this is needed as the screen is deleted every time it is closed
                    for name, text in [(Q1_weight_line_edit, Class.Q1_weight_line_edit.text()),
                                       (Q2_weight_line_edit, Class.Q2_weight_line_edit.text()),
                                       (E2_weight_line_edit, Class.E2_weight_line_edit.text()),
                                       (Q3_weight_line_edit, Class.Q3_weight_line_edit.text()),
                                       (Q4_weight_line_edit, Class.Q4_weight_line_edit.text()),
                                       (E4_weight_line_edit, Class.E4_weight_line_edit.text())]:
                        name.setText(text)

                # adding the weight_line_edits to the class
                Class.Q1_weight_line_edit = Q1_weight_line_edit
                Class.Q2_weight_line_edit = Q2_weight_line_edit
                Class.E2_weight_line_edit = E2_weight_line_edit
                Class.Q3_weight_line_edit = Q3_weight_line_edit
                Class.Q4_weight_line_edit = Q4_weight_line_edit
                Class.E4_weight_line_edit = E4_weight_line_edit

                # this creates buttons for more information about each term
                Q1_more_button = QPushButton("More", Class.more_info_screen)
                Q2_more_button = QPushButton("More", Class.more_info_screen)
                E2_more_button = QPushButton("More", Class.more_info_screen)
                Q3_more_button = QPushButton("More", Class.more_info_screen)
                Q4_more_button = QPushButton("More", Class.more_info_screen)
                E4_more_button = QPushButton("More", Class.more_info_screen)

                # this places all of the buttons
                for name, y, term in [(Q1_more_button, 300, "Q1"), (Q2_more_button, 330, "Q2"),
                                      (E2_more_button, 360, "E2"), (Q3_more_button, 390, "Q3"),
                                      (Q4_more_button, 420, "Q4"), (E4_more_button, 450, "E4")]:
                    self.font_size(name, 10)
                    name.setGeometry(340, y, 40, 20)
                    self.change_color_new(name, "QPushButton")
                temporary_class = Class  # this is used instead of Class as without it, the most recently created class was used, not the correct one

                # these lines connect each more_button to create the more_term_info screen.
                # The screen is deleted every time it is closed and is continuously called
                Q1_more_button.clicked.connect(lambda: self.create_more_term_information_screen(temporary_class, "Q1", temporary_class.more_info_scroll_area_Q1_QWidget))
                Q2_more_button.clicked.connect(lambda: self.create_more_term_information_screen(temporary_class, "Q2", temporary_class.more_info_scroll_area_Q2_QWidget))
                E2_more_button.clicked.connect(lambda: self.create_more_term_information_screen(temporary_class, "E2", temporary_class.more_info_scroll_area_E2_QWidget))
                Q3_more_button.clicked.connect(lambda: self.create_more_term_information_screen(temporary_class, "Q3", temporary_class.more_info_scroll_area_Q3_QWidget))
                Q4_more_button.clicked.connect(lambda: self.create_more_term_information_screen(temporary_class, "Q4", temporary_class.more_info_scroll_area_Q4_QWidget))
                E4_more_button.clicked.connect(lambda: self.create_more_term_information_screen(temporary_class, "E4", temporary_class.more_info_scroll_area_E4_QWidget))

                # these lines change the screen whenever the more button is clicked
                Q1_more_button.clicked.connect(lambda: self.change_screen(temporary_class.MORE_INFO_ID_Q1))
                Q2_more_button.clicked.connect(lambda: self.change_screen(temporary_class.MORE_INFO_ID_Q2))
                E2_more_button.clicked.connect(lambda: self.change_screen(temporary_class.MORE_INFO_ID_E2))
                Q3_more_button.clicked.connect(lambda: self.change_screen(temporary_class.MORE_INFO_ID_Q3))
                Q4_more_button.clicked.connect(lambda: self.change_screen(temporary_class.MORE_INFO_ID_Q4))
                E4_more_button.clicked.connect(lambda: self.change_screen(temporary_class.MORE_INFO_ID_E4))

                # this is the button to submit term grades
                term_grade_submit_button = QPushButton("Submit", Class.more_info_screen)
                term_grade_submit_button.clicked.connect(lambda: self.term_grade_submit_func(temporary_class))
                self.create_hover_help_text(term_grade_submit_button, "Click Submit when you are ready")
                self.font_size(term_grade_submit_button, 10)
                self.center_widget(term_grade_submit_button, 480)

                # changing the color of the new widgets
                for widget, Type in [(Class.more_info_screen, "QWidget"), (self.back_button, "QPushButton"), (more_info_top_class_name, "QLabel"),
                                     (more_info_top_weight, "QLabel"), (more_info_top_credit, "QLabel"),
                                     (more_info_top_year, "QLabel"), (more_info_information_text, "QLabel"),
                                     (term_grade_area_top_text, "QLabel"), (term_grade_label, "QLabel"), (term_weight_label, "QLabel"), (term_grade_submit_button, "QPushButton")]:
                    self.change_color_new(widget, Type)

                Class.first_time = False  # the previous information will be inputted each term the screen is made

                self.input_validation()  # this is to ensure the error signs update as soon as the class it made
                # without this, it would take a noticeable amount of the time for the error signs to appear

    def term_grade_submit_func(self, class_):
        """This function is called after the term grades are submitted"""

        # creating lists with all the grades and weights
        grades = [class_.Q1_grade_line_edit.text(), class_.Q2_grade_line_edit.text(), class_.E2_grade_line_edit.text(),
                  class_.Q3_grade_line_edit.text(), class_.Q4_grade_line_edit.text(), class_.E4_grade_line_edit.text()]
        weights = [class_.Q1_weight_line_edit.text(), class_.Q2_weight_line_edit.text(), class_.E2_weight_line_edit.text(),
                   class_.Q3_weight_line_edit.text(), class_.Q4_weight_line_edit.text(), class_.E4_weight_line_edit.text()]
        grades_weights_zip = (zip(grades, weights))
        # The next line ensures that each element in the zipped list is a list rather than a tuple.
        # This is necessary as the term must be mutable
        grades_weights = [list(term) for term in grades_weights_zip]
        for term in grades_weights:
            if term[0] != "" and term[1] == "":  # ensures that there is a weight for every term that has a grade
                QMessageBox.critical(self, "Term Grades Error", "You must have a weight for each term you have a grade for")
                break
            try:
                if term[0] != "" and term[1] != "":
                    float(term[0])  # sees if it's a float or not. If not, a ValueError will occur
                    float(term[1])
                    if float(term[0]) < 0 or float(term[1]) < 0:  # makes sure it's positive
                        raise ValueError
            except ValueError:
                # if they are not empty but they are not float, an error will be raised
                QMessageBox.critical(self, "Making Class Error", "Terms and percents must be positive numbers, with no % sign")
                break
        else:  # if no error
            for user_class in self.user_classes:
                if float(user_class.class_id) == float(class_.class_id):  # ensure we have the correct class

                    user_class.Q1_grade = grades[0]  # the first index of the Q1_grade is used as that is a list, ["term", "grade"].
                    user_class.Q2_grade = grades[1]
                    user_class.E2_grade = grades[2]
                    user_class.Q3_grade = grades[3]
                    user_class.Q4_grade = grades[4]
                    user_class.E4_grade = grades[5]

                    user_class.Q1_weight = weights[0]  # save the weights to the class
                    user_class.Q2_weight = weights[1]
                    user_class.E2_weight = weights[2]
                    user_class.Q3_weight = weights[3]
                    user_class.Q4_weight = weights[4]
                    user_class.E4_weight = weights[5]

                    # this list will be iterated through
                    term_grades = [["Q1", class_.Q1_grade], ["Q2", class_.Q2_grade], ["E2", class_.E2_grade],
                                   ["Q3", class_.Q3_grade], ["Q4", class_.Q4_grade], ["E4", class_.E4_grade]]

                    for term in grades_weights:  # see if there's an exact grade for a term
                        if term[0] != "":  # if the grade isn't empty
                            for term_name in ["Q1", "Q2", "E2", "Q3", "Q4", "E4"]:
                                class_.set_term(term_name)  # access the information for that term
                                if class_.current_term.exact_grade:  # if there's an exact grade
                                    for term_ in term_grades:
                                        if term_[0] == term_name:  # if the term grade is the same as the grade in the line_edit
                                            if float(term_[1]) == round(float(class_.current_term.exact_grade)):
                                                term_[1] = class_.current_term.exact_grade  # use the non-rounded exact grade
                                            else:  # if the grade is different, use the grade in the line_edit, not the term grade
                                                class_.current_term.exact_grade = ""

                    # if there was a change due to the presence of term grades, account for that
                    new_grades = [user_class.Q1_grade, user_class.Q2_grade, user_class.E2_grade,
                                 user_class.Q3_grade, user_class.Q4_grade, user_class.E4_grade]
                    new_grades_weights_zip = (zip(new_grades, weights))
                    new_grades_weights = [list(term) for term in new_grades_weights_zip]

                    grades = []
                    weights = []

                    for term in new_grades_weights:
                        if term[0] != "":  # ensures that the grade is not empty
                            grades.append(float(term[0]) * float(term[1]))
                            weights.append(float(term[1]))
                    try:  # determine the grade from the term grades
                        user_class.exact_grade = str(sum(grades) / sum(weights))
                        user_class.grade_line_edit.setText(str(round(float(user_class.exact_grade))))
                        QMessageBox.information(self, "Term Grades", "Class saved successfully")
                    except ZeroDivisionError:  # if there are no terms
                        QMessageBox.critical(self, "Term Grade Error", "Please enter in at least one term")

    def create_more_term_information_screen(self, user_class, term_to_set: str, screen):
        """This class creates the information for the more information screen for each term"""
        user_class.set_term(term_to_set)  # this allows the subclass in the UserClass instance to be accessed
        self.create_back_button(screen, user_class.MORE_INFO_ID)

        # these lines are to get the scroll_area for hover text
        scroll_area = None  # prevent a useless Pycharm error
        if term_to_set == "Q1":
            scroll_area = self.more_info_scroll_area_Q1
        elif term_to_set == "Q2":
            scroll_area = self.more_info_scroll_area_Q2
        elif term_to_set == "E2":
            scroll_area = self.more_info_scroll_area_E2
        elif term_to_set == "Q3":
            scroll_area = self.more_info_scroll_area_Q3
        elif term_to_set == "Q4":
            scroll_area = self.more_info_scroll_area_Q4
        elif term_to_set == "E4":
            scroll_area = self.more_info_scroll_area_E4

        weight = None  # make it look better in Pycharm
        grade = ""
        # these next few lines get the weight to be displayed at the top of the screen
        # it is based on inputs in the term grades calculator
        if str(term_to_set) == "Q1":
            weight = user_class.Q1_weight
        elif str(term_to_set) == "Q2":
            weight = user_class.Q2_weight
        elif str(term_to_set) == "E2":
            weight = user_class.E2_weight
        elif str(term_to_set) == "Q3":
            weight = user_class.Q3_weight
        elif str(term_to_set) == "Q4":
            weight = user_class.Q4_weight
        elif str(term_to_set) == "E4":
            weight = user_class.E4_weight

        # if there's an exact grade, it will be displayed, rounded to 6 decimal places
        # else, it will be determined based on what's inputted in the term grades calculator
        if user_class.current_term.exact_grade:
            grade = round(float(user_class.current_term.exact_grade), 6)
        else:
            if str(term_to_set) == "Q1":
                grade = user_class.Q1_grade_line_edit.text()
            elif str(term_to_set) == "Q2":
                grade = user_class.Q2_grade_line_edit.text()
            elif str(term_to_set) == "E2":
                grade = user_class.E2_grade_line_edit.text()
            elif str(term_to_set) == "Q3":
                grade = user_class.Q3_grade_line_edit.text()
            elif str(term_to_set) == "Q4":
                grade = user_class.Q4_grade_line_edit.text()
            elif str(term_to_set) == "E4":
                grade = user_class.E2_grade_line_edit.text()

        # top information
        # name of the class
        more_term_info_top_class_name = QLabel(f"Class Name: {user_class.class_name}", screen)
        self.font_size(more_term_info_top_class_name, 15)
        self.center_widget(more_term_info_top_class_name, 10)

        # name of the term
        more_term_info_top_term = QLabel(f"Term: {term_to_set}", screen)
        self.font_size(more_term_info_top_term, 15)
        self.center_widget(more_term_info_top_term, 40)

        # weight of the term
        more_term_info_top_term_weight = QLabel(f"Term Weight: {weight}", screen)
        self.font_size(more_term_info_top_term_weight, 15)
        self.center_widget(more_term_info_top_term_weight, 70)

        # exact grade of the term
        more_term_info_top_term_grade = QLabel(f"Term Grade: {grade}", screen)
        self.font_size(more_term_info_top_term_grade, 15)
        self.center_widget(more_term_info_top_term_grade, 100)

        # add grading categories
        grading_categories_top_text = QLabel("Grading Categories", screen)
        self.create_hover_help_text(grading_categories_top_text, "Enter each of the grading categories for this class. \n"
                                                                 "This will be the same across terms. \n"
                                                                 "If your class doesn't use special weighting, only enter one category. \n"
                                                                 "If a category isn't used in the assignments, it will be ignored", scroll_area=scroll_area)
        self.font_size(grading_categories_top_text, 20)
        self.center_widget(grading_categories_top_text, 160)

        # label above the category line edits
        category_name_label = QLabel("Name", screen)
        self.create_hover_help_text(category_name_label, "Enter the name of the category", scroll_area=scroll_area)
        self.font_size(category_name_label, 10)
        category_name_label.move(245, 200)

        # label above the weight line edits
        category_weight_label = QLabel("Weight", screen)
        self.create_hover_help_text(category_weight_label, "Enter the weight of the category", scroll_area=scroll_area)
        self.font_size(category_weight_label, 10)
        category_weight_label.move(350, 200)

        # scroll area for the categories
        category_scroll_area_QWidget = QWidget()
        category_scroll_area_QWidget.setFixedSize(200, 10000)

        category_scroll_area = QScrollArea(screen)
        category_scroll_area.setWidget(category_scroll_area_QWidget)
        category_scroll_area.setWidgetResizable(True)
        category_scroll_area.setGeometry(190, 225, 220, 180)  # you can fit 6 categories before scrolling down

        user_class.current_term.category_scroll_area_QWidget = category_scroll_area_QWidget  # saves the scroll_area_QWidget to the class

        # adding a new category
        add_category_button = QPushButton("New Category", screen)
        self.create_hover_help_text(add_category_button, "If you do not see any categories, scroll up in the category area", scroll_area=scroll_area)
        self.font_size(add_category_button, 10)
        add_category_button.move(205, 400)
        add_category_button.clicked.connect(lambda: self.add_category_func(user_class, screen))

        # deleting a category
        delete_category_button = QPushButton("Delete Category", screen)
        self.font_size(delete_category_button, 10)
        delete_category_button.move(305, 400)
        delete_category_button.clicked.connect(lambda: self.delete_category_func(user_class))

        # saving the categories
        save_categories_button = QPushButton("Save", screen)
        self.create_hover_help_text(save_categories_button, "Click save when you are ready", scroll_area=scroll_area)
        self.font_size(save_categories_button, 10)
        save_categories_button.move(280, 435)
        save_categories_button.clicked.connect(lambda: self.save_categories_func(user_class, error_to_show="Categories", old_term=term_to_set))

        # adding assignments
        # note that when the user scrolls all the way down, all the widgets for assignments will fit
        # in addition, the only widgets will be for assignments
        assignments_top_text = QLabel("Assignments", screen)
        self.create_hover_help_text(assignments_top_text, "Enter all of the assignments for just this term. \n"
                                                          "This includes the assignment name, category, points received, and points available. \n"
                                                          "Do not enter the grade (%) you got on the assignment anywhere", scroll_area=scroll_area)
        self.font_size(assignments_top_text, 20)
        self.center_widget(assignments_top_text, 480)

        # label above the category combo boxes
        assignment_category_label = QLabel("Category", screen)
        self.create_hover_help_text(assignment_category_label, "Enter the category that the assignment is in \n"
                                                               "If a category that you entered is not present, click save under the categories", scroll_area=scroll_area)
        self.font_size(assignment_category_label, 10)
        assignment_category_label.move(125, 537)

        # label above the name line edits
        assignment_name_label = QLabel("Name", screen)
        self.create_hover_help_text(assignment_name_label, "Enter the name of the assignment", scroll_area=scroll_area)
        self.font_size(assignment_name_label, 10)
        assignment_name_label.move(305, 537)

        # label above the points received line edits
        assignment_points_received_label = QLabel("Points\nReceived", screen)
        self.create_hover_help_text(assignment_points_received_label, "Enter the amount of points you received on this assignment \n"
                                                                      "Do not enter the grade you received (%) on the assignment anywhere", scroll_area=scroll_area)
        self.font_size(assignment_points_received_label, 10)
        assignment_points_received_label.setAlignment(Qt.AlignCenter)
        assignment_points_received_label.move(395, 520)

        # label above the points available line edits
        assignment_total_points_label = QLabel("Points\nAvailable", screen)
        self.create_hover_help_text(assignment_total_points_label, "Enter the amount of points available for this assignment \n"
                                                                      "Do not enter the grade you received (%) on the assignment anywhere", scroll_area=scroll_area)
        self.font_size(assignment_total_points_label, 10)
        assignment_total_points_label.setAlignment(Qt.AlignCenter)
        assignment_total_points_label.move(460, 520)

        # creating the assignments scroll area
        assignment_scroll_area_QWidget = QWidget()
        assignment_scroll_area_QWidget.setFixedSize(460, 10000)

        assignment_scroll_area = QScrollArea(screen)
        assignment_scroll_area.setWidget(assignment_scroll_area_QWidget)
        assignment_scroll_area.setWidgetResizable(True)
        assignment_scroll_area.setGeometry(50, 560, 480, 420)  # 14 assignments before you have to scroll

        user_class.current_term.assignment_scroll_area_QWidget = assignment_scroll_area_QWidget  # save the scroll area QWidget to the class

        if user_class.current_term.term_first_time:  # if first time, add a sample category
            self.add_category_func(user_class, screen)  # add a category
            user_class.current_term.term_first_time = False  # it won't be first time any more

            # insert information into the category just made
            user_class.current_term.category_line_edits[0][0].setText("Sample Category")
            user_class.current_term.category_line_edits[0][1].setText("100")
        else:  # because the screen is deleted everytime is it closed, old information must be re-entered
            old_category_line_edits = user_class.current_term.category_line_edits  # the previous list
            user_class.current_term.category_line_edits = []
            for category in old_category_line_edits:
                y_offset = len(user_class.current_term.category_line_edits) * 30  # number of categories * 30

                # making a category_name_line_edit for each old category
                category_name_line_edit = QLineEdit(user_class.current_term.category_scroll_area_QWidget)
                category_name_line_edit.setObjectName("any_input_needed")  # this is needed for input validation
                category_name_line_edit.setGeometry(0, y_offset, 150, 20)
                self.change_color_new(category_name_line_edit, "QLineEdit")

                # creating a weight_line_edit for each old category
                category_weight_line_edit = QLineEdit(user_class.current_term.category_scroll_area_QWidget)
                category_weight_line_edit.setGeometry(160, y_offset, 40, 20)
                self.change_color_new(category_weight_line_edit, "QLineEdit")

                category_name_line_edit.show()
                category_weight_line_edit.show()

                user_class.current_term.category_line_edits.append([category_name_line_edit, category_weight_line_edit])

                # inserting the old text back into the line edit
                category_name_line_edit.setText(category[0].text())
                category_weight_line_edit.setText(category[1].text())

            old_assignment_line_edits = user_class.current_term.assignment_line_edits
            user_class.current_term.assignment_line_edits = []
            for assignment in old_assignment_line_edits:
                y_offset = len(user_class.current_term.assignment_line_edits) * 30  # of assignments * 30

                # combo box
                assignment_category_combo_box = ComboBox(user_class.current_term.assignment_scroll_area_QWidget)
                assignment_category_combo_box.setObjectName("no_input_validation")
                assignment_category_combo_box.setGeometry(0, y_offset, 200, 20)
                self.change_color_new(assignment_category_combo_box, "ComboBox")

                # adding categories
                for category in user_class.categories:
                    assignment_category_combo_box.addItem(category[0])

                # assignment name
                assignment_name_line_edit = QLineEdit(user_class.current_term.assignment_scroll_area_QWidget)
                assignment_name_line_edit.setObjectName("no_input_validation")  # needed for input validation
                assignment_name_line_edit.setGeometry(210, y_offset, 120, 20)
                self.change_color_new(assignment_name_line_edit, "QLineEdit")

                # points received
                assignment_points_received_line_edit = QLineEdit(user_class.current_term.assignment_scroll_area_QWidget)
                assignment_points_received_line_edit.setGeometry(340, y_offset, 55, 20)
                self.change_color_new(assignment_points_received_line_edit, "QLineEdit")

                # points available
                assignment_points_total_line_edit = QLineEdit(user_class.current_term.assignment_scroll_area_QWidget)
                assignment_points_total_line_edit.setObjectName("assignments_screen")
                assignment_points_total_line_edit.setGeometry(405, y_offset, 55, 20)
                self.change_color_new(assignment_points_total_line_edit, "QLineEdit")

                assignment_category_combo_box.show()
                assignment_name_line_edit.show()
                assignment_points_received_line_edit.show()
                assignment_points_total_line_edit.show()

                # append the new widgets
                user_class.current_term.assignment_category_combo_boxes.append(assignment_category_combo_box)
                user_class.current_term.assignment_line_edits.append(
                    [assignment_category_combo_box, assignment_name_line_edit,
                     assignment_points_received_line_edit, assignment_points_total_line_edit])

                # insert old text into the widgets
                assignment_category_combo_box.setCurrentText(assignment[0].currentText())
                assignment_name_line_edit.setText(assignment[1].text())
                assignment_points_received_line_edit.setText(assignment[2].text())
                assignment_points_total_line_edit.setText(assignment[3].text())

        # add an assignment
        add_assignment_button = QPushButton("New Assignment", screen)
        self.create_hover_help_text(add_assignment_button, "If you do not see any assignments, scroll up in the assignment area", scroll_area=scroll_area)
        self.font_size(add_assignment_button, 10)
        add_assignment_button.move(200, 995)
        add_assignment_button.clicked.connect(lambda: self.add_assignment_func(user_class, screen))

        # delete an assignments
        delete_assignment_button = QPushButton("Delete Assignment", screen)
        self.font_size(delete_assignment_button, 10)
        delete_assignment_button.move(310, 995)
        delete_assignment_button.clicked.connect(lambda: self.delete_assignment_func(user_class))

        # save assignments
        save_assignments_button = QPushButton("Save", screen)
        self.create_hover_help_text(save_assignments_button, "Click Save when ready", scroll_area=scroll_area)
        self.font_size(save_assignments_button, 10)
        save_assignments_button.move(280, 1030)
        save_assignments_button.clicked.connect(lambda: self.save_assignments_func(user_class))

        # change the colors of the widgets created in this function
        for widget, Type in [(self.back_button, "QPushButton"), (more_term_info_top_class_name, "QLabel"),
                             (more_term_info_top_term, "QLabel"), (more_term_info_top_term_weight, "QLabel"),
                             (more_term_info_top_term_grade, "QLabel"),
                             (grading_categories_top_text, "QLabel"), (category_name_label, "QLabel"),
                             (category_weight_label, "QLabel"), (add_category_button, "QPushButton"),
                             (delete_category_button, "QPushButton"), (save_categories_button, "QPushButton"),
                             (assignments_top_text, "QLabel"), (assignment_category_label, "QLabel"),
                             (assignment_name_label, "QLabel"), (assignment_points_received_label, "QLabel"),
                             (assignment_total_points_label, "QLabel"), (add_assignment_button, "QPushButton"),
                             (delete_assignment_button, "QPushButton"), (save_assignments_button, "QPushButton"),]:
            self.change_color_new(widget, Type)

            # this saves the categories when the screen is opened. It will not show any QMessageBoxes
            self.save_categories_func(user_class, show_success=False)

            self.input_validation()  # this is to ensure the error signs update as soon as the class it made
            # without this, it would take a noticeable amount of the time for the error signs to appear

    def add_category_func(self, user_class, screen):  # the screen parameter is needed to prevent useless PyCharm errors. It doesn't do anything
        """This function adds a category"""
        y_offset = len(user_class.current_term.category_line_edits) * 30  # number of categories * 30
        category_name_line_edit = QLineEdit(user_class.current_term.category_scroll_area_QWidget)  # line edit for category name
        category_name_line_edit.setObjectName("any_input_needed")  # specific input validation
        category_name_line_edit.setGeometry(0, y_offset, 150, 20)  # change the size and place the line edit
        self.change_color_new(category_name_line_edit, "QLineEdit")  # change the color

        category_weight_line_edit = QLineEdit(user_class.current_term.category_scroll_area_QWidget)
        category_weight_line_edit.setGeometry(160, y_offset, 40, 20)
        self.change_color_new(category_weight_line_edit, "QLineEdit")

        category_name_line_edit.show()  # the line edits have to be shown as it's a new screen, not created from the start
        category_weight_line_edit.show()

        # keep track of the line edits
        user_class.current_term.category_line_edits.append([category_name_line_edit, category_weight_line_edit])

        self.input_validation()  # this is to ensure the error signs update as soon as the class it made
        # without this, it would take a noticeable amount of the time for the error signs to appear

    def delete_category_func(self, user_class):
        """This function deletes a category"""
        if user_class.current_term.category_line_edits:  # only works if there are categories on screen
            line_edits = user_class.current_term.category_line_edits.pop()  # pop from the list
            for edit in line_edits:
                edit.setParent(None)  # delete the line edits
                edit.deleteLater()
            self.input_validation()  # this is to ensure the error signs update as soon as the class it made
            # without this, it would take a noticeable amount of the time for the error signs to appear

    def save_categories_func(self, user_class, show_success=True, error_to_show=None, old_term=None):
        """This function saves the categories
        The show_success parameter is needed as if it's not being run from the button, there shouldn't be confirmation text
        The error_to_show parameter determines which error (Assignments or Categories) to show
        old_term is a string needed when saving categories across terms
        """
        temporary_categories = []  # store the categories

        for category in user_class.current_term.category_line_edits:
            try:  # if a weight isn't a float
                if not (category[0].text() == "" and category[1].text() == ""):
                    if float(category[1].text()) < 0:  # if a weight is negative
                        raise ValueError
                    else:  # append the category to the new list
                        temporary_categories.append([category[0].text(), category[1].text()])
            except ValueError:
                if error_to_show == "Categories":  # it's being run from the save categories button
                    QMessageBox.critical(self, "Make Categories Error", "Please enter in all fields correctly")
                elif error_to_show == "Assignments":  # it's being run from the save assignments button
                    QMessageBox.critical(self, "Saving Assignments Error", "Assignments were not saved as not all fields for categories were entered in correctly")
                return "error"  # prevent assignments from being saved

        # these lines are used to prevent duplicates
        category_names = [category[0] for category in temporary_categories]
        # if a category appears twice, it will be appended here
        duplicates = set([name for name in category_names if category_names.count(name) > 1])

        if len(category_names) == 0:  # if there are no categories
            if error_to_show == "Categories":
                QMessageBox.critical(self, "Making Categories Error", "Please enter at least one category")
            elif error_to_show == "Assignments":
                QMessageBox.critical(self, "Saving Assignments Error", "Assignments were not saved as there are no categories")
            return "error"

        if duplicates:  # if there are duplicate categories
            if error_to_show == "Categories":
                QMessageBox.critical(self, "Making Categories Error", "Categories can not have duplicate names")
            elif error_to_show == "Assignments":
                QMessageBox.critical(self, "Saving Assignments Error", "Assignments were not saved as there were duplicate categories")
            return "error"

        # the rest of the code will only occur if there have not been any errors
        user_class.categories = temporary_categories  # set the categories list to the new one
        old_line_edits = user_class.current_term.category_line_edits  # we will need this later

        if old_term:  # if it's from the button
            for term in ["Q1", "Q2", "E2", "Q3", "Q4", "E4"]:
                user_class.set_term(term)  # access information for that term
                user_class.current_term.term_first_time = False  # to prevent defaults from being entered
                user_class.current_term.category_line_edits = old_line_edits  # make it the same as categories are the same for the whole class
            user_class.set_term((old_term))  # return to the old term

        if show_success:  # if from the button
            QMessageBox.information(self, "Making Categories", "Categories saved successfully")
        if user_class.current_term.assignment_category_combo_boxes:  # if there are any assignments, update categories
            for combo_box in user_class.current_term.assignment_category_combo_boxes:
                last_index = combo_box.currentIndex()  # previous index
                combo_box.clear()  # remove options
                for category in user_class.categories:  # add options
                    combo_box.addItem(category[0])
                combo_box.setCurrentIndex(last_index)  # set to the last index

    def add_assignment_func(self, user_class, screen):  # the unused screen parameter is used to prevent a useless PyCharm error
        """This function adds an assignment"""
        y_offset = len(user_class.current_term.assignment_line_edits) * 30  # of assignments * 30

        # create the combo box to pick the categories
        assignment_category_combo_box = ComboBox(user_class.current_term.assignment_scroll_area_QWidget)
        assignment_category_combo_box.setObjectName("no_input_validation")  # no input validation for this combo box, it would be a problem with the categories instead
        assignment_category_combo_box.setGeometry(0, y_offset, 200, 20)  # change the size
        self.change_color_new(assignment_category_combo_box, "ComboBox")  # change the color

        for category in user_class.categories:  # add each category to the combo box
            assignment_category_combo_box.addItem(category[0])

        assignment_name_line_edit = QLineEdit(user_class.current_term.assignment_scroll_area_QWidget)
        assignment_name_line_edit.setObjectName("no_input_validation")  # the name doesn't need validation
        assignment_name_line_edit.setGeometry(210, y_offset, 120, 20)
        self.change_color_new(assignment_name_line_edit, "QLineEdit")

        # points received
        assignment_points_received_line_edit = QLineEdit(user_class.current_term.assignment_scroll_area_QWidget)
        assignment_points_received_line_edit.setGeometry(340, y_offset, 55, 20)
        self.change_color_new(assignment_points_received_line_edit, "QLineEdit")

        # points that could be earned
        assignment_points_total_line_edit = QLineEdit(user_class.current_term.assignment_scroll_area_QWidget)
        assignment_points_total_line_edit.setGeometry(405, y_offset, 55, 20)
        self.change_color_new(assignment_points_total_line_edit, "QLineEdit")

        # needed as this screen isn't created at the start of the program
        assignment_category_combo_box.show()
        assignment_name_line_edit.show()
        assignment_points_received_line_edit.show()
        assignment_points_total_line_edit.show()

        user_class.current_term.assignment_category_combo_boxes.append(assignment_category_combo_box)  # needed to reset them
        # needed to reset them
        user_class.current_term.assignment_line_edits.append([assignment_category_combo_box, assignment_name_line_edit,
                                                         assignment_points_received_line_edit, assignment_points_total_line_edit])
        self.input_validation()  # this is to ensure the error signs update as soon as the class it made
        # without this, it would take a noticeable amount of the time for the error signs to appear

    def delete_assignment_func(self, user_class):
        """This function deletes an assignment"""
        self.update_assignments_func(user_class)  # update the assignments
        if user_class.current_term.assignment_line_edits:  # if there are assignments
            line_edits = user_class.current_term.assignment_line_edits.pop()  # get rid of the line edits (and combo box)
            user_class.current_term.assignment_category_combo_boxes.pop()  # remove the combo box
            user_class.current_term.assignments.pop()  # get rid of the assignment
            for edit in line_edits:
                edit.setParent(None)  # delete the widgets
                edit.deleteLater()
        self.input_validation()  # this is to ensure the error signs update as soon as the class it made
        # without this, it would take a noticeable amount of the time for the error signs to appear

    def update_assignments_func(self, user_class):
        """This updates the assignments"""
        user_class.current_term.assignments.clear()  # clears all the assignments from the list
        for i, assignment in enumerate(user_class.current_term.assignment_line_edits):  # puts the assignments back in the list, now updated
            user_class.current_term.assignments.append(
                [assignment[0].currentText(), assignment[1].text(), assignment[2].text(), assignment[3].text()])

    def save_assignments_func(self, user_class):
        """This saves the assignments when the button is pressed"""
        save_categories = self.save_categories_func(user_class, show_success=False, error_to_show="Assignments")  # shows error from assignments
        self.update_assignments_func(user_class)  # updates the assignments
        if save_categories != "error":  # if there is no error
            try:  # if a value is incorrect
                grand_total_points_earned = []
                grand_total_points_available = []
                for category in user_class.categories:  # get the total points for each category
                    category_total_points_earned = []  # amount of points student earned in this category
                    category_total_points_available = []  # total amount of points for the category
                    for assignment in user_class.current_term.assignments:  # loop through the line edits
                        if not (assignment[2] == "" and assignment[3] == ""):  # if the grades are empty, ignore the term
                            if assignment[0] == category[0]:  # if the category names match. There can not be duplicate category names
                                category_total_points_earned.append(float(assignment[2]))  # append the points earned for this assignment
                                category_total_points_available.append(float(assignment[3]))  # append the points available for this assignment
                    if sum(category_total_points_available) != 0:  # if there are more than 0 points available
                        category_grade = sum(category_total_points_earned) / sum(category_total_points_available)
                        grand_total_points_earned.append(float(category_grade) * float(category[1]))  # append the weighted percentage to the list
                        grand_total_points_available.append(float(category[1]))  # append the weight
                if sum(grand_total_points_available) == 0:  # if the points available is zero
                    if sum(grand_total_points_earned) != 0:
                        final = 100  # there's extra credit but not regular grades
                    else:
                        raise ZeroDivisionError
                elif sum(grand_total_points_earned) < 0 or sum(grand_total_points_available) < 0:
                    raise ValueError  # if there's a negative
                else:
                    final = sum(grand_total_points_earned) / sum(grand_total_points_available) * 100
                if final > 100:  # prevent grades above 100
                    final = 100

                # update the line edits on the term grades calculator
                term_grade_line_edits = [["Q1", user_class.Q1_grade_line_edit], ["Q2", user_class.Q2_grade_line_edit], ["E2", user_class.E2_grade_line_edit],
                                         ["Q3", user_class.Q3_grade_line_edit], ["Q4", user_class.Q4_grade_line_edit], ["E4", user_class.E4_grade_line_edit]]

                for term in term_grade_line_edits:  # get the correct term
                    if term[0] == str(user_class.current_term_string):
                        term[1].setText(str(round(final)))
                    user_class.current_term.exact_grade = float(final)
                QMessageBox.information(self, "Saving Assignments", "Assignments saved successfully")
            except ValueError:  # if fields aren't float
                QMessageBox.critical(self, "Saving Assignments Error", "Please enter in all fields correctly, including a category and positive numbers for the points received and available")
            except ZeroDivisionError:  # if fields are empty
                QMessageBox.critical(self, "Saving Assignments Error", "Please enter in at least one assignment")

    def create_instructions_screen(self):
        """This function creates the elements for the Instructions menu"""

        # back button
        self.create_back_button(self.instructions_screen_scroll_area_QWidget, self.HOME_SCREEN)

        # top text
        self.instructions_top_text = QLabel("Instructions", self.instructions_screen_scroll_area_QWidget)
        self.font_size(self.instructions_top_text, 25)
        self.center_widget(self.instructions_top_text, 10)

        # basic GPA calculations
        self.calculating_GPA_basics_top_text = QLabel("Calculating GPA: Basics", self.instructions_screen_scroll_area_QWidget)
        self.font_size(self.calculating_GPA_basics_top_text, 20)
        self.center_widget(self.calculating_GPA_basics_top_text, 75)

        self.calculating_GPA_basics_text = QLabel("This program allows Monroe-Woodbury students to calculate their weighted and unweighted GPA. \n"
                                                  "For a simple experience, hit Calculate my GPA on the home screen, and then hit Quarterly/Annual. \n"
                                                  "Enter in the grade, credit, and weight of each class you are taking. \n"
                                                  "When ready, hit Calculate my GPA for your weighted and unweighted GPA \n\n"
                                                  "For a more comprehensive GPA, hit Cumulative GPA after hitting Calculate my GPA. \n"
                                                  "Enter in all the information for classes you have taken in high school\n"
                                                  "This includes high school classes in Middle School (Algebra I, Biology, Foreign Language) \n"
                                                  "When ready, hit Calculate my GPA on the cumulative screen \n"
                                                  "You will then see your cumulative weighted and unweighted GPA", self.instructions_screen_scroll_area_QWidget)
        self.calculating_GPA_basics_text.setAlignment(Qt.AlignCenter)
        self.font_size(self.calculating_GPA_basics_text, 10)
        self.center_widget(self.calculating_GPA_basics_text, 120)

        # more complex GPA calculations
        self.instructions_more_top_text = QLabel("Using the More button", self.instructions_screen_scroll_area_QWidget)
        self.font_size(self.instructions_more_top_text, 20)
        self.center_widget(self.instructions_more_top_text, 330)

        self.instructions_more_text = QLabel( "The More button next to each class allows to further customize each class. \n"
            "Clicking the More button will greet you to the term grades screen. \n"
            "This allows you to enter grades by the term, not just F4. \n"
            "You should also change term weights as necessary. \n"
            "Default term weights can be changed in the settings\n"
            "This would only make sense on the annual/cumulative level, not the Quarterly level. \n"
            "The purpose of the term grades screen is to allow for you to calculate a more precise GPA. \n "
            "When you submit the term grades, you will see a rounded grade based on your term grade, \n"
            "but your GPA will be more precise, calculated with the non-rounded grade. \n\n"
            "For an even more precise GPA, click More next to each term on the term grade screen \n"
            "Here, you can enter in the assignments for a term, allowing your GPA to be as exact as possible \n"
            "First, enter assignment categories for each class. These can be found in PowerSchool. \n"
            "If you have questions, ask your teacher. \n"
            "Your teacher may only have one category, in that case, only include one category. \n"
            "Then, for each term, enter in all the assignments for that term. \n"
            "Enter in the category, points received, and total points available. \n "
            "Do not enter the % you got on the assignment. \n"
            "From there, hit the submit button to save your assignments to the class. \n"
            "Your grade for that term will now be calculated based on assignment grades, giving a more GPA \n\n"
            "Remember that doing this optional. \n"
            "You can enter just the final grade of the class for a less exact GPA", self.instructions_screen_scroll_area_QWidget)
        self.instructions_more_text.setAlignment(Qt.AlignCenter)
        self.font_size(self.instructions_more_text, 10)
        self.center_widget(self.instructions_more_text, 375)

        # GPA scale information
        self.GPA_scale_instructions_top_text = QLabel("100.0 vs 4.0 Scale", self.instructions_screen_scroll_area_QWidget)
        self.font_size(self.GPA_scale_instructions_top_text, 20)
        self.center_widget(self.GPA_scale_instructions_top_text, 815)

        self.GPA_scale_instructions_text = QLabel("By default, this program uses a 100.0 Scale as that is what Monroe-Woodbury uses \n"
                                                  "However, many other schools uses a 4.0 Scale. \n"
                                                  "The user can change between the scales on both the Quarterly and Cumulative GPA screens \n"
                                                  "This can be useful for comparing GPAs to those of other schools. \n", self.instructions_screen_scroll_area_QWidget)
        self.GPA_scale_instructions_text.setAlignment(Qt.AlignCenter)
        self.font_size(self.GPA_scale_instructions_text, 10)
        self.center_widget(self.GPA_scale_instructions_text, 860)

        # Weighted GPA information
        self.weighted_GPA_information_top_text = QLabel("Weighted GPA", self.instructions_screen_scroll_area_QWidget)
        self.font_size(self.weighted_GPA_information_top_text, 20)
        self.center_widget(self.weighted_GPA_information_top_text, 960)

        self.weighted_GPA_information_text = QLabel("Your Weighted GPA accounts for increased difficulty of Honors and AP classes. \n"
                                                    "Monroe-Woodbury gives 1.03 weight to Honors classes and 1.05 weighted to AP classes. \n"
                                                    "This program has the 4.0 scale give 1.125 weight to Honors classes and 1.25 to AP classes. \n"
                                                    "The weight given to advanced classes can be changed in the settings found on the home screen. \n "
                                                    "The user can use this to compare their GPA to those of other schools.", self.instructions_screen_scroll_area_QWidget)
        self.weighted_GPA_information_text.setAlignment(Qt.AlignCenter)
        self.font_size(self.weighted_GPA_information_text, 10)
        self.center_widget(self.weighted_GPA_information_text, 1005)

        # SQL account system
        self.account_system_instructions_top_text = QLabel("Using the Account System", self.instructions_screen_scroll_area_QWidget)
        self.font_size(self.account_system_instructions_top_text, 20)
        self.center_widget(self.account_system_instructions_top_text, 1130)

        self.account_system_information_text = QLabel(
            "This program allows you to save your data with an account system. \n"
            "Click Account Settings from the home screen, and from there you can create an account. \n"
            "The information with the account system is no way related to Monroe-Woodbury. \n"
            "You should create an account like you would on other websites, not with your school information. \n"
            "Once you are logged in, your data will be saved to the account dynamically. \n"
            "When you use the login screen to log in at a later time, all of your previous data will be loaded in. \n"
            "This includes all the information about your classes, including information from the More screen. \n"
            "It also includes anything that you changed in the settings, as well as the scale (4.0 vs 100.0) used. \n"
            "Note that logging into an account will delete all data currently in the program \n"
            "In addition, logging out of an account will cause that data to be deleted. \n"
            "That data could only be found be logging back into the account", self.instructions_screen_scroll_area_QWidget)
        self.account_system_information_text.setAlignment(Qt.AlignCenter)
        self.font_size(self.account_system_information_text, 10)
        self.center_widget(self.account_system_information_text, 1175)

        # local data
        self.importing_local_data_instructions_top_text = QLabel("Importing Local Data", self.instructions_screen_scroll_area_QWidget)
        self.font_size(self.importing_local_data_instructions_top_text, 20)
        self.center_widget(self.importing_local_data_instructions_top_text, 1395)

        self.importing_local_data_instructions_text = QLabel("This program also saves your data locally. \n"
                                                             "This data can be accessed by clicking Import Local Data on the home screen. \n"
                                                             "Like with the account system, all the data in the program is saved locally \n"
                                                             "It is preferred that you use the account system to save your data as this method is less reliable \n"
                                                             "In addition, the account system is cross-platform, while this method is not \n\n",
                                                             self.instructions_screen_scroll_area_QWidget)
        self.importing_local_data_instructions_text.setAlignment(Qt.AlignCenter)
        self.font_size(self.importing_local_data_instructions_text, 10)
        self.center_widget(self.importing_local_data_instructions_text, 1430)

        self.export_data_instructions_top_text = QLabel("Exporting Data", self.instructions_screen_scroll_area_QWidget)
        self.font_size(self.export_data_instructions_top_text, 20)
        self.center_widget(self.export_data_instructions_top_text, 1555)

        self.exporting_data_instructions_text = QLabel("This program allows you to export your data through a PDF or Excel spreadsheet. \n"
                                                       "Once you have successfully calculated your GPA, you can click 'Export Data' on the home screen \n"
                                                       "From here, you can either create a PDF or an Excel spreadsheet. \n"
                                                       "You will be asked some information before being taken to the grade report. ",
                                                             self.instructions_screen_scroll_area_QWidget)
        self.exporting_data_instructions_text.setAlignment(Qt.AlignCenter)
        self.font_size(self.exporting_data_instructions_text, 10)
        self.center_widget(self.exporting_data_instructions_text, 1590)

    def create_FAQ_screen(self):
        """This function creates the elements for the Instructions menu"""

        # back button
        self.create_back_button(self.FAQ_screen_scroll_area_QWidget, self.HOME_SCREEN)

        # top text
        self.FAQ_top_text = QLabel("Frequently Asked Questions", self.FAQ_screen_scroll_area_QWidget)
        self.font_size(self.FAQ_top_text, 25)
        self.center_widget(self.FAQ_top_text, 10)

        # Question 1
        self.question_1 = QLabel("What is GPA and how is it calculated? \n\n"
                                 "GPA is the grade point average for all the classes for a given period. \n"
                                 "It is calculated based on the grade the student received, \n"
                                 "the credit (usually proportional to length) of the course, and for weighted GPA, weight.", self.FAQ_screen_scroll_area_QWidget)
        self.font_size(self.question_1, 10)
        self.question_1.move(30, 70)

        self.question_2 = QLabel("What is the difference between weighted and unweighted GPA? \n\n"
                                 "Unweighted GPA doesn't give extra weight for Honors and AP classes.\n"
                                 "Weighted GPA accounts for Honors and AP classes and gives extra weight to them.\n"
                                 "Weighted GPA is more common at Monroe-Woodbury.", self.FAQ_screen_scroll_area_QWidget)
        self.font_size(self.question_2, 10)
        self.question_2.move(30, 190)

        self.question_3 = QLabel("What should I do if a class is not Regular, Honors, or AP? \n\n"
                                 "For non-AP college classes (usually Dual Enrollment), you should check with your teacher \n"
                                 "as weighting is different for each class \n"
                                 "Pre-AP World History is Honors", self.FAQ_screen_scroll_area_QWidget)
        self.font_size(self.question_3, 10)
        self.question_3.move(30, 310)

        self.question_4 = QLabel("What is the difference between 100.0 and 4.0 GPA? \n\n"
                                 "Monroe-Woodbury uses 100.0 GPA, but many other schools use 4.0 GPA. \n"
                                 "Both are provided so M-W students can easily compare GPAs to students at other schools.", self.FAQ_screen_scroll_area_QWidget)
        self.font_size(self.question_4, 10)
        self.question_4.move(30, 430)

        self.question_5 = QLabel("What 8th Grade classes count for High School GPA? \n\n"
                                 "Only enter in Algebra I, Biology, and Foreign Language for 8th Grade.", self.FAQ_screen_scroll_area_QWidget)
        self.font_size(self.question_5, 10)
        self.question_5.move(30, 520)

        self.question_6 = QLabel("Where can I access the grades for classes I took in previous years? \n\n"
                                 "You can find grade from previous years on PowerSchool by going to grade history \n"
                                 "You can't access term grades or assignments, so you would only be able to enter final grades",
                                 self.FAQ_screen_scroll_area_QWidget)
        self.font_size(self.question_6, 10)
        self.question_6.move(30, 600)

        self.question_7 = QLabel("How can I save my data? \n\n"
                                 "You can save your data by making an account on the account settings screen. \n"
                                 "Logging back in will cause your previous data to reappear. \n"
                                 "Data is also saved locally and can be accessed by clicking Import Local Data on the home screen \n"
                                 "It is preferred that you use the account system as that is more reliable and cross-platform",
                                 self.FAQ_screen_scroll_area_QWidget)
        self.font_size(self.question_7, 10)
        self.question_7.move(30, 690)

        self.question_8 = QLabel("How can I export my data? \n\n"
                                 "You can export your data by going to the export data screen on the home page. \n"
                                 "From here, you can create a PDF or all of your Quarterly/Cumulative Classes. \n"
                                 "You can also create a PDF of individual classes \n"
                                 "You can also export your data through an Excel spreadsheet", self.FAQ_screen_scroll_area_QWidget)
        self.font_size(self.question_8, 10)
        self.question_8.move(30, 820)

        self.question_9 = QLabel("How can I report a bug for this program or ask additional questions? \n\n"
                                 "Bugs and additional questions can be sent to prasadsaha11@gmail.com.",
                                 self.FAQ_screen_scroll_area_QWidget)
        self.font_size(self.question_9, 10)
        self.question_9.move(30, 950)

    def create_settings_screen(self):
        """This function creates the elements for the Settings menu"""

        # back button
        self.create_back_button(self.settings_screen, self.HOME_SCREEN)

        # top text
        self.settings_top_text = QLabel("Settings", self.settings_screen)
        self.font_size(self.settings_top_text, 25)
        self.center_widget(self.settings_top_text, 10)

        # top text for changing class weight and default term weights
        self.change_class_weight_top_label = QLabel("Change Class Weight", self.settings_screen)
        self.create_hover_help_text(self.change_class_weight_top_label, "This changes the weight of honors and AP classes \n"
                                                                        "There are different weights for the 4.0 and 100.0 scale")
        self.font_size(self.change_class_weight_top_label, 15)
        self.center_widget(self.change_class_weight_top_label, 80)

        # default term weight top label
        self.change_default_term_weight_top_label = QLabel("Change Default Term Weights", self.settings_screen)
        self.create_hover_help_text(self.change_default_term_weight_top_label, "This changes the default weight of each term within the term grades calculator \n"
                                                                               "Changes here will not effect current classes")
        self.font_size(self.change_default_term_weight_top_label, 15)
        self.center_widget(self.change_default_term_weight_top_label, 280)

        # the labels can be made this way as they don't need to be accessed again
        for name, text, y in [("self.change_honors_100_weight_label", "Change Honors Weight (100.0):", 120),
                              ("self.change_AP_100_weight_label", "Change AP Weight (100.0):", 150),
                              ("self.change_honors_4_weight_label", "Change Honors Weight (4.0):", 180),
                              ("self.change_AP_4_weight_label", "Change AP Weight (4.0):", 210),
                              ("self.change_Q1_default_weight_label", "Quarter 1 Weight: ", 320),
                              ("self.change_Q2_default_weight_label", "Quarter 2 Weight: ", 350),
                              ("self.change_E2_default_weight_label", "Midterm Exam Weight: ", 380),
                              ("self.change_Q3_default_weight_label", "Quarter 3 Weight: ", 410),
                              ("self.change_Q4_default_weight_label", "Quarter 4 Weight: ", 440),
                              ("self.change_E4_default_weight_label", "Final Exam Weight: ", 470)
                              ]:
            name = QLabel(text, self.settings_screen)
            self.font_size(name, 10)
            name.move(330-name.sizeHint().width(), y)

        # making the line edits for changing honors and AP weight
        self.change_honors_100_weight_line_edit = QLineEdit(self.settings_screen)
        self.change_AP_100_weight_line_edit = QLineEdit(self.settings_screen)
        self.change_honors_4_weight_line_edit = QLineEdit(self.settings_screen)
        self.change_AP_4_weight_line_edit = QLineEdit(self.settings_screen)

        # making the line edits for default term weights
        self.change_Q1_default_weight_line_edit = QLineEdit(self.settings_screen)
        self.change_Q2_default_weight_line_edit = QLineEdit(self.settings_screen)
        self.change_E2_default_weight_line_edit = QLineEdit(self.settings_screen)
        self.change_Q3_default_weight_line_edit = QLineEdit(self.settings_screen)
        self.change_Q4_default_weight_line_edit = QLineEdit(self.settings_screen)
        self.change_E4_default_weight_line_edit = QLineEdit(self.settings_screen)

        for name, y, value in [(self.change_honors_100_weight_line_edit, 120, self.honors_weight_100),
                               (self.change_AP_100_weight_line_edit, 150, self.AP_weight_100),
                               (self.change_honors_4_weight_line_edit, 180, self.honors_weight_4),
                               (self.change_AP_4_weight_line_edit, 210, self.AP_weight_4),
                               (self.change_Q1_default_weight_line_edit, 320, self.default_Q1_weight),
                               (self.change_Q2_default_weight_line_edit, 350, self.default_Q2_weight),
                               (self.change_E2_default_weight_line_edit, 380, self.default_E2_weight),
                               (self.change_Q3_default_weight_line_edit, 410, self.default_Q3_weight),
                               (self.change_Q4_default_weight_line_edit, 440, self.default_Q4_weight),
                               (self.change_E4_default_weight_line_edit, 470, self.default_E4_weight)
                            ]:
            name.setGeometry(335, y, 50, 20)
            name.setText(str(value))  # set the text to the current value

        # submit button for changing honors and AP weights
        self.submit_change_class_weights_settings_button = QPushButton("Submit", self.settings_screen)
        self.create_hover_help_text(self.submit_change_class_weights_settings_button, "Click Submit when you are ready")
        self.font_size(self.submit_change_class_weights_settings_button, 10)
        self.center_widget(self.submit_change_class_weights_settings_button, 240)
        self.submit_change_class_weights_settings_button.clicked.connect(self.submit_change_class_weights_settings_func)

        # submit button for changing default term weights
        self.submit_changes_default_term_weight_button = QPushButton("Submit", self.settings_screen)
        self.create_hover_help_text(self.submit_changes_default_term_weight_button, "Click Submit when you are ready")
        self.font_size(self.submit_changes_default_term_weight_button, 10)
        self.center_widget(self.submit_changes_default_term_weight_button, 500)
        self.submit_changes_default_term_weight_button.clicked.connect(self.submit_changes_default_term_weight_func)

        # button for changing the colors
        self.change_colors_button = QPushButton("Change Colors", self.settings_screen)
        self.create_hover_help_text(self.change_colors_button, "This button allows you to change the colors of the program")
        self.font_size(self.change_colors_button, 15)
        self.center_widget(self.change_colors_button, 540)
        self.change_colors_button.clicked.connect(self.change_colors_func)

    def submit_change_class_weights_settings_func(self):
        """This function changes the weight of honors and AP classes"""
        try:  # detects non-float values
            values = [float(self.change_honors_100_weight_line_edit.text()), float(self.change_AP_100_weight_line_edit.text()),
                      float(self.change_honors_4_weight_line_edit.text()), float(self.change_AP_4_weight_line_edit.text())]
            for value in values:  # if a value is negative
                if value < 0:
                    raise ValueError

            # changes the weights
            self.honors_weight_100 = float(self.change_honors_100_weight_line_edit.text())
            self.AP_weight_100 = float(self.change_AP_100_weight_line_edit.text())
            self.honors_weight_4 = float(self.change_honors_4_weight_line_edit.text())
            self.AP_weight_4 = float(self.change_AP_4_weight_line_edit.text())

            # changes the weights used for calculating GPA
            if self.GPA_scale == 100.0:
                self.honors_weight = self.honors_weight_100
                self.AP_weight = self.AP_weight_100
            elif self.GPA_scale == 4.0:
                self.honors_weight = self.honors_weight_4
                self.AP_weight = self.AP_weight_4
            QMessageBox.information(self, "Changing Settings", "Class weights saved successfully")
        except ValueError:  # if there's an invalid input
            QMessageBox.critical(self, "Changing Settings Error", "Ensure that all values are positive numbers")

    def submit_changes_default_term_weight_func(self):
        """This function changes default term weights"""
        try:  # detects non-float
            values = [float(self.change_Q1_default_weight_line_edit.text()),
                      float(self.change_Q2_default_weight_line_edit.text()),
                      float(self.change_E2_default_weight_line_edit.text()),
                      float(self.change_Q3_default_weight_line_edit.text()),
                      float(self.change_Q4_default_weight_line_edit.text()),
                      float(self.change_E4_default_weight_line_edit.text())]
            for value in values:
                if value < 0:  # if negative
                    raise ValueError

            # changes default term weights. Note that this doesn't change current classes
            self.default_Q1_weight = float(self.change_Q1_default_weight_line_edit.text())
            self.default_Q2_weight = float(self.change_Q2_default_weight_line_edit.text())
            self.default_E2_weight = float(self.change_E2_default_weight_line_edit.text())
            self.default_Q3_weight = float(self.change_Q3_default_weight_line_edit.text())
            self.default_Q4_weight = float(self.change_Q4_default_weight_line_edit.text())
            self.default_E4_weight = float(self.change_E4_default_weight_line_edit.text())

            QMessageBox.information(self, "Changing Settings", "Settings saved successfully")
        except ValueError:  # if invalid input
            QMessageBox.critical(self, "Changing Settings Error", "Ensure that all values are positive numbers")

    def change_colors_func(self, first=False):
        """This function changes the colors of the program"""
        if not first:  # if it's being run from the button in the settings menu
            color_1_dialog = QColorDialog.getColor(QColor(self.color_1), self)  # first dialog
            if color_1_dialog.isValid():
                self.color_1 = color_1_dialog.name()

            color_2_dialog = QColorDialog.getColor(QColor(self.color_2), self)  # second dialog
            if color_2_dialog.isValid():
                self.color_2 = color_2_dialog.name()

        for label in self.findChildren(QLabel):  # change the colors of the labels
                label.setStyleSheet(f"""
                color: {self.color_2};
            """)

        for line_edit in self.findChildren(QLineEdit):  # change the colors of the line edits
                line_edit.setStyleSheet(f"""
                background-color: {self.color_1};
                color: {self.color_2};
                border: 1px solid {self.color_2};
            """)

        for button in self.findChildren(QPushButton):  # change the color of the buttons, including when they are pressed
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.color_1};
                    color: {self.color_2};
                    border: 1px solid {self.color_2};
                    padding: 3px;
                }}
                QPushButton:pressed {{
                    background-color: {self.color_2};
                    color: {self.color_1}
                }}
            """)

        ''''
        for combo_box in self.findChildren(ComboBox):
            combo_box.setStyleSheet(f"""
                QComboBox QAbstractItemView:item:hover {{ background-color: {self.color_1}; }}
                /* Include the default QComboBox styling */
                QComboBox {{
                    background-color: {self.color_1};
                    color: {self.color_2};
                    border: 1px solid {self.color_2};
                }}
            """)
            '''
        for index in range(self.stacked_widget.count()):  # change the color of all backgrounds
            screen = self.stacked_widget.widget(index)
            screen.setStyleSheet(f"background-color: {self.color_1}")

    def change_color_new(self, widget, type_=""):
        """Whenever a new widget is made, this function is called to change the colors of that widget"""
        if type_ == "QWidget":  # changes the background color
            widget.setStyleSheet(f"background-color: {self.color_1}")
        elif type_ == "QLabel":  # for labels
            widget.setStyleSheet(f"""color: {self.color_2};""")
        elif type_ == "QPushButton":  # for buttons
            widget.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.color_1};
                    color: {self.color_2};
                    border: 1px solid {self.color_2};
                    padding: 3px;
                }}
                QPushButton:pressed {{
                    background-color: {self.color_2};
                    color: {self.color_1}
                }}
            """)
        elif type_ == "QScrollArea":  # for scroll aras
            widget.setStyleSheet(f"""
            background-color: {self.color_1};
            color: {self.color_2};
            QScrollBar:vertical {{
            background-color: orange;
        }}""")
            '''
        elif Type == "ComboBox":
            widget.setStyleSheet(f"""
                QComboBox QAbstractItemView:item:hover {{ background-color: {self.color_1}; }}
                /* Include the default QComboBox styling */
                QComboBox {{
                    background-color: {self.color_1};
                    color: {self.color_2};
                    border: 1px solid {self.color_2};
                }}
            """)
            '''
        else:  # line_edit, Combobox
            widget.setStyleSheet(f"""
                    background-color: {self.color_1};
                    color: {self.color_2};
                    border: 1px solid {self.color_2};
                """)

    def create_account_settings_screen(self):
        """This function creates the elements for the account settings screen"""

        # back button
        self.create_back_button(self.account_settings_homepage, self.HOME_SCREEN)

        # the text at the top of the login screen
        self.login_top_text = QLabel("You are logged out", self.account_settings_homepage)
        self.font_size(self.login_top_text, 20)
        self.center_widget(self.login_top_text, 20)

        # the text at the top of the login screen
        self.login_top_text_2 = QLabel("Create an account to access your data at a later time", self.account_settings_homepage)
        self.font_size(self.login_top_text_2, 15)
        self.center_widget(self.login_top_text_2, 60)

        # this opens the create account screen
        self.open_create_account_screen = QPushButton("Create Account", self.account_settings_homepage)
        self.open_create_account_screen.clicked.connect(lambda: self.change_screen(self.CREATE_ACCOUNT_SCREEN))
        self.create_hover_help_text(self.open_create_account_screen, "This is not related to your school information")
        self.font_size(self.open_create_account_screen, 20)
        self.center_widget(self.open_create_account_screen, 100)

        # this opens the login screen
        self.open_login_screen = QPushButton("Log in", self.account_settings_homepage)
        self.open_login_screen.clicked.connect(lambda: self.change_screen(self.LOGIN_SCREEN))
        self.create_hover_help_text(self.open_login_screen, "This is not related to your school information")
        self.font_size(self.open_login_screen, 20)
        self.center_widget(self.open_login_screen, 160)

    def create_create_account_screen(self):
        """This function creates the elements for the create account screen"""

        # back button
        self.create_back_button(self.create_account_screen, self.ACCOUNT_SETTINGS_HOMEPAGE)

        # top text
        self.create_account_top_text_1 = QLabel("Create New Account", self.create_account_screen)
        self.font_size(self.create_account_top_text_1, 20)
        self.center_widget(self.create_account_top_text_1, 20)

        # ensures that the user knows login information
        self.create_account_top_text_2 = QLabel("The information on this screen is in no way related "
                                                "to your Monroe-Woodbury school information", self.create_account_screen)
        self.font_size(self.create_account_top_text_2, 10)
        self.center_widget(self.create_account_top_text_2, 60)

        # labels
        # username - must be at least 6 characters
        self.create_account_username_label = QLabel("Username: ", self.create_account_screen)
        self.create_hover_help_text(self.create_account_username_label, "Must be at least 6 characters")
        self.font_size(self.create_account_username_label, 10)
        self.create_account_username_label.move(270 - self.create_account_username_label.sizeHint().width() - 2, 100)

        # password - must be at least 6 characters and at least one number, special symbol, and capital letter
        self.create_account_password_label = QLabel("Password: ", self.create_account_screen)
        self.create_hover_help_text(self.create_account_password_label, "Must have at least 6 characters and include at least \n"
                                                                        "one number, special symbol, and capital letter")
        self.font_size(self.create_account_password_label, 10)
        self.create_account_password_label.move(270 - self.create_account_password_label.sizeHint().width() - 2, 130)

        # confirm password
        self.create_account_confirm_password_label = QLabel("Confirm Password: ", self.create_account_screen)
        self.create_hover_help_text(self.create_account_confirm_password_label, "Be sure that the passwords match")
        self.font_size(self.create_account_confirm_password_label, 10)
        self.create_account_confirm_password_label.move(270 - self.create_account_confirm_password_label.sizeHint().width() - 2, 160)

        # email - optional but must be valid
        self.create_account_email_label = QLabel("Email (optional): ", self.create_account_screen)
        self.create_hover_help_text(self.create_account_email_label, "Must be a valid email. This is optional.")
        self.font_size(self.create_account_email_label, 10)
        self.create_account_email_label.move(270 - self.create_account_email_label.sizeHint().width() - 2, 190)

        # line edits
        # username
        self.create_account_username_line_edit = QLineEdit(self.create_account_screen)
        self.create_account_username_line_edit.setObjectName("6_chars_needed")  # for input validation
        self.font_size(self.create_account_username_line_edit, 10)
        self.create_account_username_line_edit.setGeometry(270, 100, 100, 20)

        # password
        self.create_account_password_line_edit = QLineEdit(self.create_account_screen)
        self.create_account_password_line_edit.setEchoMode(QLineEdit.Password)  # it will be hidden
        self.create_account_password_line_edit.setObjectName("password")  # for input validation to help the user
        self.font_size(self.create_account_password_line_edit, 10)
        self.create_account_password_line_edit.setGeometry(270, 130, 100, 20)

        # confirm password
        self.create_account_confirm_password_line_edit = QLineEdit(self.create_account_screen)
        self.create_account_confirm_password_line_edit.setEchoMode(QLineEdit.Password)  # it will be hidden
        self.create_account_confirm_password_line_edit.setObjectName("password")  # for input validation to help the user
        self.font_size(self.create_account_confirm_password_line_edit, 10)
        self.create_account_confirm_password_line_edit.setGeometry(270, 160, 100, 20)

        # email
        self.create_account_email_line_edit = QLineEdit(self.create_account_screen)
        self.create_account_email_line_edit.setObjectName("email_line_edit")  # for input validation - must be empty or valid
        self.font_size(self.create_account_email_line_edit, 10)
        self.create_account_email_line_edit.setGeometry(270, 190, 100, 20)

        # buttons for showing password
        self.show_first_password_create_account_button = QPushButton("Show", self.create_account_screen)
        self.create_hover_help_text(self.show_first_password_create_account_button, "Show/Hide password")
        self.show_first_password_create_account_button.clicked.connect(lambda: self.password_visibility(self.create_account_password_line_edit, self.show_first_password_create_account_button))
        self.show_first_password_create_account_button.setGeometry(375, 130, 40, 20)

        self.show_confirm_password_create_account_button = QPushButton("Show", self.create_account_screen)
        self.create_hover_help_text(self.show_confirm_password_create_account_button, "Show/Hide password")
        self.show_confirm_password_create_account_button.clicked.connect(lambda: self.password_visibility(self.create_account_confirm_password_line_edit, self.show_confirm_password_create_account_button))
        self.show_confirm_password_create_account_button.setGeometry(375, 160, 40, 20)

        # submit button
        self.create_account_submit_button = QPushButton("Submit", self.create_account_screen)
        self.create_account_submit_button.clicked.connect(self.create_account_submit_func)
        self.create_hover_help_text(self.create_account_submit_button, "When ready, hit this button to create your account")
        self.font_size(self.create_account_submit_button, 15)
        self.center_widget(self.create_account_submit_button, 230)

        # login instead
        self.switch_to_login_button = QPushButton("Already have an account?", self.create_account_screen)
        self.switch_to_login_button.clicked.connect(lambda: self.change_screen(self.LOGIN_SCREEN))
        self.create_hover_help_text(self.switch_to_login_button, "Access the login screen")
        self.font_size(self.switch_to_login_button, 10)
        self.center_widget(self.switch_to_login_button, 300)

    def valid_password(self, password):
        """This function determines if a password is valid"""
        has_digit = re.search(r'\d', password)  # Check for at least one digit
        has_special_char = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)  # Check for at least one special character
        has_uppercase = re.search(r'[A-Z]', password)  # Check for at least one uppercase letter

        return has_digit and has_special_char and has_uppercase  # if all True, then True, if one is False, then False

    def create_account_submit_func(self):
        usernames = []  # all usernames in the database
        db_username = "SELECT username FROM user_data"
        my_cursor.execute(db_username)
        for name in my_cursor:
            usernames.append(name)
        formatted_usernames = [name[0] for name in usernames]  # getting the usernames

        if self.create_account_username_line_edit.text() in formatted_usernames:
            # if username already taken
            QMessageBox.critical(self, "Creating Account Error", "Username already taken")
        elif len(self.create_account_username_line_edit.text()) < 6 or len(self.create_account_password_line_edit.text()) < 6:
            # if username/password is too short
            QMessageBox.critical(self, "Creating Account Error", "Username and password must be at least 6 letters")
        elif not self.valid_password(self.create_account_password_line_edit.text()):
            # if password is invalid
            QMessageBox.critical(self, "Creating Account Error", "Password must have at least 6 letters, at least one number, "
                                                                 "at least one special symbol, and at least one capital letter")
        elif self.create_account_password_line_edit.text() != self.create_account_confirm_password_line_edit.text():
            # if passwords don't match
            QMessageBox.critical(self, "Creating Account Error", "Passwords do not match")
        elif self.create_account_email_line_edit.text() != "" and re.match(self.email_pattern, self.create_account_email_line_edit.text()) is None:
            # if email is given but invalid
            QMessageBox.critical(self, "Creating Account Error", "Invalid email")
        else:
            # puts the new account in the database
            my_cursor.execute("INSERT INTO user_data(username, password, email) VALUES (%s, %s, %s)",
                              (self.create_account_username_line_edit.text(), self.create_account_password_line_edit.text(), self.create_account_email_line_edit.text()))
            db.commit()

            query = "SELECT userID, username, password, email FROM user_data ORDER BY userID DESC LIMIT 1"
            my_cursor.execute(query)  # putting the information into the program
            for i in my_cursor:
                self.account_id = i[0]
                self.username = i[1]
                self.password = i[2]
                self.email = i[3]

            QMessageBox.information(self, "Creating Account", "Account Created successfully")
            self.logged_in = True

            self.change_screen(self.LOGGED_IN_SCREEN)  # changing the screen
            # changes the destination of account settings button
            self.account_settings_button.clicked.connect(lambda: self.change_screen(self.LOGGED_IN_SCREEN))

            # changing the top text on the logged in screen
            self.logged_in_screen_top_text.setText(f"Logged in as: {self.username}")
            self.logged_in_screen_top_text.adjustSize()
            self.center_widget(self.logged_in_screen_top_text, 20)

            # start dynamic backup
            thread_SQL_data = threading.Thread(target=self.SQL_dynamic_backup, daemon=True)
            thread_SQL_data.start()

    def create_login_screen(self):
        """This function creates the elements for the login screen"""

        # back button
        self.create_back_button(self.login_screen, self.ACCOUNT_SETTINGS_HOMEPAGE)

        # top text
        self.login_top_text_1 = QLabel("Login", self.login_screen)
        self.font_size(self.login_top_text_1, 20)
        self.center_widget(self.login_top_text_1, 20)

        self.login_top_text_2 = QLabel("The information on this screen is in no way related to Monroe-Woodbury", self.login_screen)
        self.font_size(self.login_top_text_2, 10)
        self.center_widget(self.login_top_text_2, 60)

        # labels
        self.login_username_label = QLabel("Username/Email: ", self.login_screen)
        self.create_hover_help_text(self.login_username_label, "No requirements other than being at least 6 characters")
        self.font_size(self.login_username_label, 10)
        self.login_username_label.move(165, 100)

        self.login_password_label = QLabel("Password: ", self.login_screen)
        self.create_hover_help_text(self.login_password_label, "Must have at least 6 characters and include at least \n "
                                                               "one number, special symbol, and capital letter")
        self.font_size(self.login_password_label, 10)
        self.login_password_label.move(205, 130)

        # line edits
        self.login_username_line_edit = QLineEdit(self.login_screen)
        self.login_username_line_edit.setObjectName("6_chars_needed")  # input validation
        self.font_size(self.login_username_line_edit, 10)
        self.login_username_line_edit.setGeometry(270, 100, 100, 20)

        self.login_password_line_edit = QLineEdit(self.login_screen)
        self.login_password_line_edit.setEchoMode(QLineEdit.Password)  # hide the password
        self.login_password_line_edit.setObjectName("password")  # input validation
        self.font_size(self.login_password_line_edit, 10)
        self.login_password_line_edit.setGeometry(270, 130, 100, 20)

        # button for showing the password
        self.show_login_password_button = QPushButton("Show", self.login_screen)
        self.show_login_password_button.clicked.connect(lambda: self.password_visibility(self.login_password_line_edit, self.show_login_password_button))
        self.create_hover_help_text(self.show_login_password_button, "Show/Hide Password")
        self.show_login_password_button.setGeometry(375, 130, 40, 20)

        # submit button
        self.login_submit_button = QPushButton("Submit", self.login_screen)
        self.login_submit_button.clicked.connect(self.login_submit_func)
        self.create_hover_help_text(self.login_submit_button, "When ready, hit this button to log in")
        self.font_size(self.login_submit_button, 15)
        self.center_widget(self.login_submit_button, 200)

        # create account instead
        self.switch_to_create_account_button = QPushButton("Don't have an account?", self.login_screen)
        self.switch_to_create_account_button.clicked.connect(lambda: self.change_screen(self.CREATE_ACCOUNT_SCREEN))
        self.create_hover_help_text(self.switch_to_create_account_button, "Access the create account screen")
        self.font_size(self.switch_to_create_account_button, 10)
        self.center_widget(self.switch_to_create_account_button, 270)

        # forget password
        self.forgot_password_button = QPushButton("Forgot password?", self.login_screen)
        self.forgot_password_button.clicked.connect(lambda: self.change_screen(self.FORGOT_PASSWORD_SCREEN))
        self.create_hover_help_text(self.forgot_password_button, "Click here if you forgot your password")
        self.font_size(self.forgot_password_button, 10)
        self.center_widget(self.forgot_password_button, 305)

    def password_visibility(self, line_edit, button):
        """This function controls if the password is visibility based off user input"""
        if line_edit.echoMode() == QLineEdit.Password:  # if the password is hidden
            line_edit.setEchoMode(QLineEdit.Normal)  # turn it to normal
            button.setText("Hide")  # change the text
        else:
            line_edit.setEchoMode(QLineEdit.Password)
            button.setText("Show")

    def login_submit_func(self):
        """This function inserts old data into the program
        Note that the information in this function is similar to other functions,
        but combining them into one function seemed to harm performance time"""
        self.update_class_data(show_error=False)
        usernames = []  # getting usernames from the database
        db_username = "SELECT username FROM user_data"
        my_cursor.execute(db_username)
        for name in my_cursor:
            usernames.append(name)
        formatted_usernames = [name[0] for name in usernames]

        if self.login_username_line_edit.text() in formatted_usernames:  # if username is valid
            query1 = f"SELECT password FROM user_data WHERE username = %s"  # finding the password
            my_cursor.execute(query1, (self.login_username_line_edit.text(),))
            for i in my_cursor:
                password = i[0]
            if self.login_password_line_edit.text() == password:  # if password is valid
                answer = QMessageBox.question(self, "Login", "Logging into an account will delete any data you currently have in the program. Are you sure that you would like to continue?")
                if answer == QMessageBox.Yes:  # if no, nothing happens
                    self.delete_all_data()  # deletes all data in the program

                    query2 = f"SELECT * FROM user_data WHERE username = %s"  # get user data
                    my_cursor.execute(query2, (self.login_username_line_edit.text(), ))

                    # this iterates through all user data
                    for i in my_cursor:
                        # i refers to the data, and looks like
                        # (255, 'digmines9999', 'Digmines3!', '', '100.0', '1.03', '1.25', '1.125', '1.25',
                        # '1.03', '1.05', '21.25', '21.25', '5', '21.25', '21.25', '10', 'black', 'white')
                        self.account_id = i[0]
                        self.username = i[1]
                        self.password = i[2]
                        self.email = i[3]
                        self.GPA_scale = float(i[4])  # float is to ensure that the type of variable isn't a problem
                        self.honors_weight_100 = float(i[5])
                        self.AP_weight_100 = float(i[6])
                        self.honors_weight_4 = float(i[7])
                        self.AP_weight_100 = float(i[8])
                        self.honors_weight = float(i[9])
                        self.AP_weight = float(i[10])
                        self.default_Q1_weight = i[11]
                        self.default_Q2_weight = i[12]
                        self.default_E2_weight = i[13]
                        self.default_Q3_weight = i[14]
                        self.default_Q4_weight = i[15]
                        self.default_E4_weight = i[16]
                        self.color_1 = i[17]
                        self.color_2 = i[18]

                        # changing the labels for GPA scale
                        self.change_GPA_scale_label_quarterly.setText(f"Scale: {self.GPA_scale}")
                        self.change_GPA_scale_label_quarterly.adjustSize()
                        self.change_GPA_scale_label_cumulative.setText(f"Scale: {self.GPA_scale}")
                        self.change_GPA_scale_label_cumulative.adjustSize()

                        # inserting in the correct values for the settings
                        self.change_honors_100_weight_line_edit.setText(str(i[5]))
                        self.change_AP_100_weight_line_edit.setText(str(i[6]))
                        self.change_honors_4_weight_line_edit.setText(str(i[7]))
                        self.change_AP_4_weight_line_edit.setText(str(i[8]))

                        self.change_Q1_default_weight_line_edit.setText(str(i[11]))
                        self.change_Q2_default_weight_line_edit.setText(str(i[12]))
                        self.change_E2_default_weight_line_edit.setText(str(i[13]))
                        self.change_Q3_default_weight_line_edit.setText(str(i[14]))
                        self.change_Q4_default_weight_line_edit.setText(str(i[15]))
                        self.change_E4_default_weight_line_edit.setText(str(i[16]))

                        self.change_colors_func(first=True)  # changing the colors, not showing the message boxes

                    query3 = "SELECT * FROM class_data WHERE userID = %s"  # all of the class data
                    my_cursor.execute(query3, (self.account_id,))

                    for class_ in my_cursor:
                        screen_name = class_[3]  # getting the string screen_name
                        if screen_name.startswith("self."):  # parsing the screen name
                            screen_name = screen_name[len("self."):]
                        screen = getattr(self, screen_name)
                        line_edits = scroll_area_widget = None  # prevent a Pycharm error

                        # setting the scroll_area and line edits based on the screen of the class
                        if screen == self.quarterly_GPA_screen:
                            line_edits = self.quarterly_class_line_edits
                            scroll_area_widget = self.quarterly_scroll_area_QWidget
                        elif screen == self.year_8_screen:
                            line_edits = self.year_8_class_line_edits
                            scroll_area_widget = self.year_8_scroll_area_QWidget
                        elif screen == self.year_9_screen:
                            line_edits = self.year_9_class_line_edits
                            scroll_area_widget = self.year_9_scroll_area_QWidget
                        elif screen == self.year_10_screen:
                            line_edits = self.year_10_class_line_edits
                            scroll_area_widget = self.year_10_scroll_area_QWidget
                        elif screen == self.year_11_screen:
                            line_edits = self.year_11_class_line_edits
                            scroll_area_widget = self.year_11_scroll_area_QWidget
                        elif screen == self.year_12_screen:
                            line_edits = self.year_12_class_line_edits
                            scroll_area_widget = self.year_12_scroll_area_QWidget

                        y_offset = len(line_edits) * 30  # number of classes * 30

                        # Create line edits
                        class_name_line_edit = QLineEdit(scroll_area_widget)
                        class_name_line_edit.setObjectName("no_input_validation")  # for input validation
                        grade_line_edit = QLineEdit(scroll_area_widget)
                        grade_line_edit.setObjectName("grade_line_edit")  # for input validation
                        weight_combo_box = ComboBox(scroll_area_widget)
                        credit_line_edit = QLineEdit(scroll_area_widget)
                        credit_line_edit.setObjectName("credit_line_edit")  # for input validation
                        more_info_button = QPushButton("More", scroll_area_widget)

                        if screen == self.quarterly_GPA_screen:  # creating the year combo box, only for quarterly
                            year_combo_box = ComboBox(scroll_area_widget)
                            year_combo_box.setObjectName("no_input_validation")  # no input validation as year is optional
                            self.change_color_new(year_combo_box, "ComboBox")
                            for item in ["", "8", "9", "10", "11", "12"]:
                                year_combo_box.addItem(item)
                            year_combo_box.show()  # this is needed as the widget isn't here at the start of the program

                        for widget, Type in [(class_name_line_edit, "QLineEdit"), (grade_line_edit, "QLineEdit"),
                                             (weight_combo_box, "ComboBox"),
                                             (credit_line_edit, "QLineEdit"), (more_info_button, "QPushButton"),
                                             ]:
                            self.change_color_new(widget, Type)  # changing the color of the new widgets

                        # add options to the combo boxes
                        for item in ["", "R", "H", "AP"]:
                            weight_combo_box.addItem(item)

                        # Set the positions of the line edits within the scroll area
                        class_name_line_edit.setGeometry(0, y_offset, 150, 25)
                        grade_line_edit.setGeometry(160, y_offset, 40, 25)
                        weight_combo_box.setGeometry(210, y_offset, 50, 25)
                        credit_line_edit.setGeometry(270, y_offset, 40, 25)
                        if screen == self.quarterly_GPA_screen:  # has year_combo_box
                            year_combo_box.setGeometry(320, y_offset, 40, 25)
                            more_info_button.setGeometry(370, y_offset, 40, 25)
                        else:
                            more_info_button.setGeometry(320, y_offset, 40, 25)

                        class_name_line_edit.setText(class_[4])  # getting the old text
                        grade_line_edit.setText(class_[5])
                        weight_combo_box.setCurrentText(class_[6])
                        credit_line_edit.setText(class_[7])

                        # Keep track of the line edits
                        if screen == self.quarterly_GPA_screen:
                            line_edits.append((class_[0], class_name_line_edit, grade_line_edit, weight_combo_box,
                                               credit_line_edit, year_combo_box, more_info_button))
                            year_combo_box.setCurrentText(class_[8])  # only for quarterly
                        else:
                            line_edits.append((class_[0], class_name_line_edit, grade_line_edit, weight_combo_box,
                                               credit_line_edit, more_info_button))

                        # Show the new line edits
                        class_name_line_edit.show()
                        grade_line_edit.show()
                        weight_combo_box.show()
                        credit_line_edit.show()
                        more_info_button.show()

                        # more info screen
                        more_info_screen = QWidget()
                        self.stacked_widget.addWidget(more_info_screen)
                        self.change_color_new(more_info_screen, "QWidget")
                        MORE_INFO_ID = self.stacked_widget.count() - 1

                        # make a new instance of UserClass
                        new_class = UserClass(class_id=class_[0], scope=class_[2], screen=screen,
                                              MORE_INFO_ID=MORE_INFO_ID,
                                              more_info_screen=more_info_screen, grade_line_edit=grade_line_edit,
                                              class_name=class_[4], grade=class_[5],
                                              weight=class_[6],
                                              credit=class_[7], year=class_[8],
                                              Q1_weight=class_[9], Q2_weight=class_[10],
                                              E2_weight=class_[11],
                                              Q3_weight=class_[12], Q4_weight=class_[13],
                                              E4_weight=class_[14], exact_grade=class_[15],
                                              first_time=class_[16])
                        self.class_id = int(class_[0])  # this will be overriden until the last row
                        new_class.Q1_grade = class_[17]  # the term grades based on old data
                        new_class.Q2_grade = class_[18]
                        new_class.E2_grade = class_[19]
                        new_class.Q3_grade = class_[20]
                        new_class.Q4_grade = class_[21]
                        new_class.E4_grade = class_[22]

                        self.user_classes.append(new_class)  # appends the class to the user_classes list
                        # connects the more info button to the correct screen
                        more_info_button.clicked.connect(lambda: self.create_more_information_screen(MORE_INFO_ID))
                        more_info_button.clicked.connect(lambda: self.change_screen(MORE_INFO_ID))

                        # Q1 more info screen
                        more_info_screen_Q1 = QWidget()  # this is the main screen
                        more_info_scroll_area_Q1_QWidget = QWidget()  # this is the scroll area QWidget that will encompass the entire screen
                        more_info_scroll_area_Q1_QWidget.setFixedSize(580, 1070)  # set the size for the screen

                        self.more_info_scroll_area_Q1 = QScrollArea(more_info_screen_Q1)  # the actual scroll area
                        self.change_color_new(self.more_info_scroll_area_Q1, "QScrollArea")  # because the screen isn't created by default, the color must be changed
                        self.more_info_scroll_area_Q1.setWidget(more_info_scroll_area_Q1_QWidget)
                        self.more_info_scroll_area_Q1.setWidgetResizable(True)  # the user can scroll through the scroll area
                        self.more_info_scroll_area_Q1.setGeometry(0, 0, 600, 600)  # the size of the screen before the user must scroll to see more

                        # Q2
                        more_info_screen_Q2 = QWidget()
                        more_info_scroll_area_Q2_QWidget = QWidget()
                        more_info_scroll_area_Q2_QWidget.setFixedSize(580, 1070)

                        self.more_info_scroll_area_Q2 = QScrollArea(more_info_screen_Q2)
                        self.change_color_new(self.more_info_scroll_area_Q2, "QScrollArea")
                        self.more_info_scroll_area_Q2.setWidget(more_info_scroll_area_Q2_QWidget)
                        self.more_info_scroll_area_Q2.setWidgetResizable(True)
                        self.more_info_scroll_area_Q2.setGeometry(0, 0, 600, 600)

                        # E2
                        more_info_screen_E2 = QWidget()
                        more_info_scroll_area_E2_QWidget = QWidget()
                        more_info_scroll_area_E2_QWidget.setFixedSize(580, 1070)

                        self.more_info_scroll_area_E2 = QScrollArea(more_info_screen_E2)
                        self.change_color_new(self.more_info_scroll_area_E2, "QScrollArea")
                        self.more_info_scroll_area_E2.setWidget(more_info_scroll_area_E2_QWidget)
                        self.more_info_scroll_area_E2.setWidgetResizable(True)
                        self.more_info_scroll_area_E2.setGeometry(0, 0, 600, 600)

                        # Q3
                        more_info_screen_Q3 = QWidget()
                        more_info_scroll_area_Q3_QWidget = QWidget()
                        more_info_scroll_area_Q3_QWidget.setFixedSize(580, 1070)

                        self.more_info_scroll_area_Q3 = QScrollArea(more_info_screen_Q3)
                        self.change_color_new(self.more_info_scroll_area_Q3, "QScrollArea")
                        self.more_info_scroll_area_Q3.setWidget(more_info_scroll_area_Q3_QWidget)
                        self.more_info_scroll_area_Q3.setWidgetResizable(True)
                        self.more_info_scroll_area_Q3.setGeometry(0, 0, 600, 600)

                        # Q4
                        more_info_screen_Q4 = QWidget()
                        more_info_scroll_area_Q4_QWidget = QWidget()
                        more_info_scroll_area_Q4_QWidget.setFixedSize(580, 1070)

                        self.more_info_scroll_area_Q4 = QScrollArea(more_info_screen_Q4)
                        self.change_color_new(self.more_info_scroll_area_Q4, "QScrollArea")
                        self.more_info_scroll_area_Q4.setWidget(more_info_scroll_area_Q4_QWidget)
                        self.more_info_scroll_area_Q4.setWidgetResizable(True)
                        self.more_info_scroll_area_Q4.setGeometry(0, 0, 600, 600)

                        # E4
                        more_info_screen_E4 = QWidget()
                        more_info_scroll_area_E4_QWidget = QWidget()
                        more_info_scroll_area_E4_QWidget.setFixedSize(580, 1070)

                        self.more_info_scroll_area_E4 = QScrollArea(more_info_screen_E4)
                        self.change_color_new(self.more_info_scroll_area_E4, "QScrollArea")
                        self.more_info_scroll_area_E4.setWidget(more_info_scroll_area_E4_QWidget)
                        self.more_info_scroll_area_E4.setWidgetResizable(True)
                        self.more_info_scroll_area_E4.setGeometry(0, 0, 600, 600)

                        # adding the scroll area QWidgets to the UserClass instance
                        new_class.more_info_scroll_area_Q1_QWidget = more_info_scroll_area_Q1_QWidget
                        new_class.more_info_scroll_area_Q2_QWidget = more_info_scroll_area_Q2_QWidget
                        new_class.more_info_scroll_area_E2_QWidget = more_info_scroll_area_E2_QWidget
                        new_class.more_info_scroll_area_Q3_QWidget = more_info_scroll_area_Q3_QWidget
                        new_class.more_info_scroll_area_Q4_QWidget = more_info_scroll_area_Q4_QWidget
                        new_class.more_info_scroll_area_E4_QWidget = more_info_scroll_area_E4_QWidget

                        self.stacked_widget.addWidget(more_info_screen_Q1)  # adding the widget to the stacked widget
                        self.change_color_new(more_info_screen_Q1, "QWidget")  # changing the color
                        MORE_INFO_ID_Q1 = self.stacked_widget.count() - 1  # getting the ID for changing the screen

                        self.stacked_widget.addWidget(more_info_screen_Q2)
                        self.change_color_new(more_info_screen_Q2, "QWidget")
                        MORE_INFO_ID_Q2 = self.stacked_widget.count() - 1

                        self.stacked_widget.addWidget(more_info_screen_E2)
                        self.change_color_new(more_info_screen_E2, "QWidget")
                        MORE_INFO_ID_E2 = self.stacked_widget.count() - 1

                        self.stacked_widget.addWidget(more_info_screen_Q3)
                        self.change_color_new(more_info_screen_Q3, "QWidget")
                        MORE_INFO_ID_Q3 = self.stacked_widget.count() - 1

                        self.stacked_widget.addWidget(more_info_screen_Q4)
                        self.change_color_new(more_info_screen_Q4, "QWidget")
                        MORE_INFO_ID_Q4 = self.stacked_widget.count() - 1

                        self.stacked_widget.addWidget(more_info_screen_E4)
                        self.change_color_new(more_info_screen_E4, "QWidget")
                        MORE_INFO_ID_E4 = self.stacked_widget.count() - 1

                        # adding the IDs to the new UserClass instance
                        new_class.MORE_INFO_ID_Q1 = MORE_INFO_ID_Q1
                        new_class.MORE_INFO_ID_Q2 = MORE_INFO_ID_Q2
                        new_class.MORE_INFO_ID_E2 = MORE_INFO_ID_E2
                        new_class.MORE_INFO_ID_Q3 = MORE_INFO_ID_Q3
                        new_class.MORE_INFO_ID_Q4 = MORE_INFO_ID_Q4
                        new_class.MORE_INFO_ID_E4 = MORE_INFO_ID_E4

                        # the grade line edits
                        Q1_grade_line_edit = QLineEdit(new_class.more_info_screen)
                        Q2_grade_line_edit = QLineEdit(new_class.more_info_screen)
                        E2_grade_line_edit = QLineEdit(new_class.more_info_screen)
                        Q3_grade_line_edit = QLineEdit(new_class.more_info_screen)
                        Q4_grade_line_edit = QLineEdit(new_class.more_info_screen)
                        E4_grade_line_edit = QLineEdit(new_class.more_info_screen)

                        # setting the size, text, ad color
                        for name, text, y in [(Q1_grade_line_edit, new_class.Q1_grade, 300),
                                              (Q2_grade_line_edit, new_class.Q2_grade, 330),
                                              (E2_grade_line_edit, new_class.E2_grade, 360),
                                              (Q3_grade_line_edit, new_class.Q3_grade, 390),
                                              (Q4_grade_line_edit, new_class.Q4_grade, 420),
                                              (E4_grade_line_edit, new_class.E4_grade, 450)]:
                            name.setGeometry(90, y, 40, 20)
                            name.setText(str(text))
                            self.change_color_new(name, "QLineEdit")

                        # adding them to the UserClass instance
                        new_class.Q1_grade_line_edit = Q1_grade_line_edit
                        new_class.Q2_grade_line_edit = Q2_grade_line_edit
                        new_class.E2_grade_line_edit = E2_grade_line_edit
                        new_class.Q3_grade_line_edit = Q3_grade_line_edit
                        new_class.Q4_grade_line_edit = Q4_grade_line_edit
                        new_class.E4_grade_line_edit = E4_grade_line_edit

                        # the weight line edits
                        Q1_weight_line_edit = QLineEdit(new_class.more_info_screen)
                        Q2_weight_line_edit = QLineEdit(new_class.more_info_screen)
                        E2_weight_line_edit = QLineEdit(new_class.more_info_screen)
                        Q3_weight_line_edit = QLineEdit(new_class.more_info_screen)
                        Q4_weight_line_edit = QLineEdit(new_class.more_info_screen)
                        E4_weight_line_edit = QLineEdit(new_class.more_info_screen)

                        # setting the size, text, and color
                        for name, text, y in [(Q1_weight_line_edit, new_class.Q1_weight, 300),
                                              (Q2_weight_line_edit, new_class.Q2_weight, 330),
                                              (E2_weight_line_edit, new_class.E2_weight, 360),
                                              (Q3_weight_line_edit, new_class.Q3_weight, 390),
                                              (Q4_weight_line_edit, new_class.Q4_weight, 420),
                                              (E4_weight_line_edit, new_class.E4_weight, 450)]:
                            name.setGeometry(140, y, 40, 20)
                            name.setText(str(text))
                            self.change_color_new(name, "QLineEdit")

                        # adding them to the UserClass instance
                        new_class.Q1_weight_line_edit = Q1_weight_line_edit
                        new_class.Q2_weight_line_edit = Q2_weight_line_edit
                        new_class.E2_weight_line_edit = E2_weight_line_edit
                        new_class.Q3_weight_line_edit = Q3_weight_line_edit
                        new_class.Q4_weight_line_edit = Q4_weight_line_edit
                        new_class.E4_weight_line_edit = E4_weight_line_edit

                        new_class.categories = ast.literal_eval(class_[23])  # the categories for the assignments page

                        new_class.Q1.term_first_time = class_[24]  # if this is the first time the screen is opened
                        new_class.Q1.assignments = ast.literal_eval(class_[25])  # assignment information
                        new_class.Q1.exact_grade = class_[26]  # the exact grade

                        new_class.Q2.term_first_time = class_[27]
                        new_class.Q2.assignments = ast.literal_eval(class_[28])
                        new_class.Q2.exact_grade = class_[29]

                        new_class.E2.term_first_time = class_[30]
                        new_class.E2.assignments = ast.literal_eval(class_[31])
                        new_class.E2.exact_grade = class_[32]

                        new_class.Q3.term_first_time = class_[33]
                        new_class.Q3.assignments = ast.literal_eval(class_[34])
                        new_class.Q3.exact_grade = class_[35]

                        new_class.Q4.term_first_time = class_[36]
                        new_class.Q4.assignments = ast.literal_eval(class_[37])
                        new_class.Q4.exact_grade = class_[38]

                        new_class.E4.term_first_time = class_[39]
                        new_class.E4.assignments = ast.literal_eval(class_[40])
                        new_class.E4.exact_grade = class_[41]

                        # putting the widgets on each screen
                        for term in [new_class.Q1, new_class.Q2, new_class.E2,
                                     new_class.Q3, new_class.Q4, new_class.E4]:
                            for category in new_class.categories:  # for each category
                                y_offset = len(term.category_line_edits) * 30  # of categories * 30

                                category_name_line_edit = QLineEdit(term.category_scroll_area_QWidget)  # category name
                                category_name_line_edit.setObjectName("any_input_needed")  # for input validation
                                category_name_line_edit.setGeometry(0, y_offset, 150, 20)
                                self.change_color_new(category_name_line_edit, "QLineEdit")

                                category_weight_line_edit = QLineEdit(term.category_scroll_area_QWidget)  # category weight
                                category_weight_line_edit.setGeometry(160, y_offset, 40, 20)
                                self.change_color_new(category_weight_line_edit, "QLineEdit")

                                term.category_line_edits.append([category_name_line_edit, category_weight_line_edit])

                                category_name_line_edit.setText(category[0])  # insert the old text
                                category_weight_line_edit.setText(category[1])

                            for assignment in term.assignments:  # for each assignment
                                y_offset = len(term.assignment_line_edits) * 30  # of assignments * 30

                                assignment_category_combo_box = ComboBox(term.assignment_scroll_area_QWidget)  # category combo box
                                assignment_category_combo_box.setObjectName("no_input_validation")  # for input validation
                                assignment_category_combo_box.setGeometry(0, y_offset, 200, 20)
                                self.change_color_new(assignment_category_combo_box, "ComboBox")

                                for category in new_class.categories:
                                    assignment_category_combo_box.addItem(category[0])

                                assignment_name_line_edit = QLineEdit(term.assignment_scroll_area_QWidget)
                                assignment_name_line_edit.setObjectName("no_input_validation")  # doesn't need input validation
                                assignment_name_line_edit.setGeometry(210, y_offset, 120, 20)
                                self.change_color_new(assignment_name_line_edit, "QLineEdit")

                                assignment_points_received_line_edit = QLineEdit(term.assignment_scroll_area_QWidget)
                                assignment_points_received_line_edit.setGeometry(340, y_offset, 55, 20)
                                self.change_color_new(assignment_points_received_line_edit, "QLineEdit")

                                assignment_points_total_line_edit = QLineEdit(term.assignment_scroll_area_QWidget)
                                assignment_points_total_line_edit.setGeometry(405, y_offset, 55, 20)
                                self.change_color_new(assignment_points_total_line_edit, "QLineEdit")

                                term.assignment_category_combo_boxes.append(assignment_category_combo_box)
                                term.assignment_line_edits.append(  # putting the line_edits into the list
                                    [assignment_category_combo_box, assignment_name_line_edit,
                                     assignment_points_received_line_edit, assignment_points_total_line_edit])

                                # setting the text based off of old data
                                assignment_category_combo_box.setCurrentText(assignment[0])
                                assignment_name_line_edit.setText(assignment[1])
                                assignment_points_received_line_edit.setText(assignment[2])
                                assignment_points_total_line_edit.setText(assignment[3])

                    # change the screen
                    self.change_screen(self.LOGGED_IN_SCREEN)
                    self.account_settings_button.clicked.connect(lambda: self.change_screen(self.LOGGED_IN_SCREEN))

                    # change the text on the login screen
                    self.logged_in_screen_top_text.setText(f"Logged in as: {self.username}")
                    self.logged_in_screen_top_text.adjustSize()
                    self.center_widget(self.logged_in_screen_top_text, 20)

                    # start dynamic backup
                    thread_SQL_data = threading.Thread(target=self.SQL_dynamic_backup, daemon=True)
                    thread_SQL_data.start()

                    self.logged_in = True
                    QMessageBox.information(self, "Login", "Login Success!")
            else:  # if the password is invalid
                QMessageBox.critical(self, "Login Failure", "Invalid password")
        else:  # if the username isn't in the database
            QMessageBox.critical(self, "Login Failure", "Invalid username")

    def create_forgot_password_screen(self):
        """This function creates the elements for the forgot password screen"""

        # back button
        self.create_back_button(self.forgot_password_screen, self.LOGIN_SCREEN)

        # top text
        self.forgot_password_top_text = QLabel("Forgot Password", self.forgot_password_screen)
        self.font_size(self.forgot_password_top_text, 25)
        self.center_widget(self.forgot_password_top_text, 10)

        # text
        self.forgot_password_text = QLabel("If you had an email with your account, enter it below:", self.forgot_password_screen)
        self.font_size(self.forgot_password_text, 15)
        self.center_widget(self.forgot_password_text, 100)

        # line edit
        self.forgot_password_line_edit = QLineEdit(self.forgot_password_screen)
        self.forgot_password_line_edit.setObjectName("email_line_edit")
        self.forgot_password_line_edit.setGeometry(250, 130, 100, 25)

        # submit button
        self.forgot_password_submit_button = QPushButton("Submit", self.forgot_password_screen)
        self.forgot_password_submit_button.clicked.connect(self.forgot_password_submit_func)
        self.font_size(self.forgot_password_submit_button, 15)
        self.center_widget(self.forgot_password_submit_button, 170)

    def forgot_password_submit_func(self):
        """This displays a message box after submitting a forgotten password"""
        if re.match(self.email_pattern, self.forgot_password_line_edit.text()) is None:
            QMessageBox.critical(self, "Forgot Password Failure", "Email is invalid")
        else:
            QMessageBox.information(self, "Forgot Password", "An email will be sent with further information")

    def create_logged_in_screen(self):
        """This function creates the elements for the logged in screen"""

        # back button
        self.create_back_button(self.logged_in_screen, self.HOME_SCREEN)

        self.logged_in_screen_top_text = QLabel(f"Logged in as: {self.username}", self.logged_in_screen)
        self.font_size(self.logged_in_screen_top_text, 20)
        self.center_widget(self.logged_in_screen_top_text, 20)

        # text to inform the user about dynamic backup
        self.dynamic_backup_info = QLabel("Now that you are logged in, your data will be backed up dynamically. \n"
                                          "You can retrieve your data by logging back into your account", self.logged_in_screen)
        self.dynamic_backup_info.setAlignment(Qt.AlignCenter)
        self.font_size(self.dynamic_backup_info, 14)
        self.center_widget(self.dynamic_backup_info, 80)

        # log the user out
        self.log_out_button = QPushButton("Log Out", self.logged_in_screen)
        self.log_out_button.clicked.connect(self.log_out_func)
        self.font_size(self.log_out_button, 20)
        self.center_widget(self.log_out_button, 250)

    def log_out_func(self):
        """This function logs the user out"""
        answer = QMessageBox.question(self, "Logging out", "Are you sure that you would like to log out? All data in this program will be lost unless you log back in")
        if answer == QMessageBox.Yes:
            self.account_id = None  # sets a lot of information to None
            self.username = None
            self.logged_in = False
            self.change_screen(self.ACCOUNT_SETTINGS_HOMEPAGE)  # back to the home page for account settings
            # when the account settings button from the home screen is clicked, it goes to the home page for account settings
            self.account_settings_button.clicked.connect(lambda: self.change_screen(self.ACCOUNT_SETTINGS_HOMEPAGE))

            # clears the line edits in account data
            for line_edit in [self.login_password_line_edit, self.login_username_line_edit,
                              self.create_account_email_line_edit, self.create_account_username_line_edit,
                              self.create_account_password_line_edit, self.create_account_confirm_password_line_edit]:
                line_edit.clear()

            self.delete_all_data()  # deletes the current data
            self.SQL_dynamic_backup(final_run=True)  # backups the data

    def delete_all_data(self):
        """This functions deletes all data in the program"""
        while self.user_classes:  # while classes remain
            for screen in [self.quarterly_GPA_screen, self.year_8_screen, self.year_9_screen,
                           self.year_10_screen, self.year_11_screen, self.year_12_screen]:
                self.delete_class_func(screen)  # delete the class with the already made function

        # reset GPA information, including labels
        self.unweighted_gpa = ""
        self.weighted_gpa = ""
        self.quarterly_unweighted_GPA_label.setText(f"Unweighted GPA: ")
        self.quarterly_unweighted_GPA_label.adjustSize()
        self.quarterly_weighted_GPA_label.setText(f"Weighted GPA: ")
        self.quarterly_weighted_GPA_label.adjustSize()
        self.cumulative_unweighted_GPA_label.setText(f"Unweighted GPA: ")
        self.cumulative_unweighted_GPA_label.adjustSize()
        self.cumulative_weighted_GPA_label.setText(f"Weighted GPA: ")
        self.cumulative_weighted_GPA_label.adjustSize()

        # reset the GPA scale
        self.GPA_scale = 100.0
        self.change_GPA_scale_label_quarterly.setText(f"Scale: {self.GPA_scale}")
        self.change_GPA_scale_label_quarterly.adjustSize()
        self.change_GPA_scale_label_cumulative.setText(f"Scale: {self.GPA_scale}")
        self.change_GPA_scale_label_cumulative.adjustSize()

        # reset the weight of honors and AP classes
        self.honors_weight_100 = 1.03
        self.AP_weight_100 = 1.05
        self.honors_weight_4 = 1.125
        self.AP_weight_4 = 1.25
        self.honors_weight = self.honors_weight_100
        self.AP_weight = self.AP_weight_100
        self.change_honors_100_weight_line_edit.setText(str(self.honors_weight_100))
        self.change_AP_100_weight_line_edit.setText(str(self.AP_weight_100))
        self.change_honors_4_weight_line_edit.setText(str(self.honors_weight_4))
        self.change_AP_4_weight_line_edit.setText(str(self.AP_weight_4))

        # rest default term weights
        self.default_Q1_weight = 21.25
        self.default_Q2_weight = 21.25
        self.default_E2_weight = 5
        self.default_Q3_weight = 21.25
        self.default_Q4_weight = 21.25
        self.default_E4_weight = 10

        self.change_Q1_default_weight_line_edit.setText(str(self.default_Q1_weight))
        self.change_Q2_default_weight_line_edit.setText(str(self.default_Q2_weight))
        self.change_E2_default_weight_line_edit.setText(str(self.default_E2_weight))
        self.change_Q3_default_weight_line_edit.setText(str(self.default_Q3_weight))
        self.change_Q4_default_weight_line_edit.setText(str(self.default_Q4_weight))
        self.change_E4_default_weight_line_edit.setText(str(self.default_E4_weight))

        # reset the colors
        self.color_1 = "black"
        self.color_2 = "white"
        self.change_colors_func(first=True)

    def import_local_data_func(self):
        class_data_file = open('gpa_calculator_class_data.csv', mode='r')
        class_data_reader = csv.reader(class_data_file)
        user_data_file = open('gpa_calculator_user_data.csv', mode='r')
        user_data_reader = csv.reader(user_data_file)

        if os.path.getsize('gpa_calculator_class_data.csv') == 0:  # the user_data is used as it will never be empty
            QMessageBox.critical(self, "Loading Data Error", "You have no data to import")
        else:
            confirm = QMessageBox.question(self, "Loading Data", "Are you sure that you would like to import your previous data? "
                                                                 "Any current data you have in the program will be lost."
                                                                 "In addition, if you were logged in previously, you will not automatically be logged in")
            if confirm == QMessageBox.Yes:
                try:
                    self.delete_all_data()
                    for class_ in class_data_reader:
                        screen_name = class_[2]
                        if screen_name.startswith("self."):
                            screen_name = screen_name[len("self."):]
                        screen = getattr(self, screen_name)
                        line_edits = scroll_area_widget = None

                        if screen == self.quarterly_GPA_screen:
                            line_edits = self.quarterly_class_line_edits
                            scroll_area_widget = self.quarterly_scroll_area_QWidget
                        elif screen == self.year_8_screen:
                            line_edits = self.year_8_class_line_edits
                            scroll_area_widget = self.year_8_scroll_area_QWidget
                        elif screen == self.year_9_screen:
                            line_edits = self.year_9_class_line_edits
                            scroll_area_widget = self.year_9_scroll_area_QWidget
                        elif screen == self.year_10_screen:
                            line_edits = self.year_10_class_line_edits
                            scroll_area_widget = self.year_10_scroll_area_QWidget
                        elif screen == self.year_11_screen:
                            line_edits = self.year_11_class_line_edits
                            scroll_area_widget = self.year_11_scroll_area_QWidget
                        elif screen == self.year_12_screen:
                            line_edits = self.year_12_class_line_edits
                            scroll_area_widget = self.year_12_scroll_area_QWidget

                        y_offset = len(line_edits) * 30

                        # Create line edits
                        class_name_line_edit = QLineEdit(scroll_area_widget)
                        class_name_line_edit.setObjectName("no_input_validation")
                        grade_line_edit = QLineEdit(scroll_area_widget)
                        grade_line_edit.setObjectName("grade_line_edit")
                        weight_combo_box = ComboBox(scroll_area_widget)
                        credit_line_edit = QLineEdit(scroll_area_widget)
                        credit_line_edit.setObjectName("credit_line_edit")
                        more_info_button = QPushButton("More", scroll_area_widget)

                        if screen == self.quarterly_GPA_screen:
                            year_combo_box = ComboBox(scroll_area_widget)
                            year_combo_box.setObjectName("no_input_validation")
                            self.change_color_new(year_combo_box, "ComboBox")
                            for item in ["", "8", "9", "10", "11", "12"]:
                                year_combo_box.addItem(item)
                            year_combo_box.show()

                        for widget, Type in [(class_name_line_edit, "QLineEdit"), (grade_line_edit, "QLineEdit"),
                                             (weight_combo_box, "ComboBox"),
                                             (credit_line_edit, "QLineEdit"), (more_info_button, "QPushButton"),
                                             ]:
                            self.change_color_new(widget, Type)

                        # add options to the combo boxes
                        for item in ["", "R", "H", "AP"]:
                            weight_combo_box.addItem(item)

                        # Set the positions of the line edits
                        class_name_line_edit.setGeometry(0, y_offset, 150, 25)
                        grade_line_edit.setGeometry(160, y_offset, 40, 25)
                        weight_combo_box.setGeometry(210, y_offset, 50, 25)
                        credit_line_edit.setGeometry(270, y_offset, 40, 25)
                        if screen == self.quarterly_GPA_screen:
                            year_combo_box.setGeometry(320, y_offset, 40, 25)
                            more_info_button.setGeometry(370, y_offset, 40, 25)
                        else:
                            more_info_button.setGeometry(320, y_offset, 40, 25)

                        class_name_line_edit.setText(class_[3])
                        grade_line_edit.setText(class_[4])
                        weight_combo_box.setCurrentText(class_[5])
                        credit_line_edit.setText(class_[6])

                        # Keep track of the line edits
                        if screen == self.quarterly_GPA_screen:
                            line_edits.append((class_[0], class_name_line_edit, grade_line_edit, weight_combo_box,
                                               credit_line_edit, year_combo_box, more_info_button))
                            year_combo_box.setCurrentText(class_[7])
                        else:
                            line_edits.append((class_[0], class_name_line_edit, grade_line_edit, weight_combo_box,
                                               credit_line_edit, more_info_button))

                        # Show the new line edits
                        class_name_line_edit.show()
                        grade_line_edit.show()
                        weight_combo_box.show()
                        credit_line_edit.show()
                        more_info_button.show()

                        more_info_screen = QWidget()
                        self.stacked_widget.addWidget(more_info_screen)
                        self.change_color_new(more_info_screen, "QWidget")
                        MORE_INFO_ID = self.stacked_widget.count() - 1

                        new_class = UserClass(class_id=class_[0], scope=class_[1], screen=screen,
                                              MORE_INFO_ID=MORE_INFO_ID,
                                              more_info_screen=more_info_screen, grade_line_edit=grade_line_edit,
                                              class_name=class_[3], grade=class_[4], weight=class_[5],
                                              credit=class_[6], year=class_[7],
                                              Q1_weight=class_[8], Q2_weight=class_[9],
                                              E2_weight=class_[10],
                                              Q3_weight=class_[11], Q4_weight=class_[12],
                                              E4_weight=class_[13], exact_grade=class_[14],
                                              first_time=class_[15],
                                              )

                        for line_edit in self.findChildren(QLineEdit):
                            if line_edit.parent() == new_class.more_info_screen:
                                line_edit.setParent(None)
                                line_edit.deleteLater()

                        self.class_id = int(class_[0])  # this will be overriden until the last row
                        new_class.Q1_grade = class_[16]
                        new_class.Q2_grade = class_[17]
                        new_class.E2_grade = class_[18]
                        new_class.Q3_grade = class_[19]
                        new_class.Q4_grade = class_[20]
                        new_class.E4_grade = class_[21]

                        self.user_classes.append(new_class)
                        more_info_button.clicked.connect(lambda: self.create_more_information_screen(MORE_INFO_ID))
                        more_info_button.clicked.connect(lambda: self.change_screen(MORE_INFO_ID))

                        more_info_screen_Q1 = QWidget()
                        more_info_scroll_area_Q1_QWidget = QWidget()
                        more_info_scroll_area_Q1_QWidget.setFixedSize(580, 1070)

                        self.more_info_scroll_area_Q1 = QScrollArea(more_info_screen_Q1)
                        self.change_color_new(self.more_info_scroll_area_Q1, "QScrollArea")
                        self.more_info_scroll_area_Q1.setWidget(more_info_scroll_area_Q1_QWidget)
                        self.more_info_scroll_area_Q1.setWidgetResizable(True)
                        self.more_info_scroll_area_Q1.setGeometry(0, 0, 600, 600)

                        more_info_screen_Q2 = QWidget()
                        more_info_scroll_area_Q2_QWidget = QWidget()
                        more_info_scroll_area_Q2_QWidget.setFixedSize(580, 1070)

                        self.more_info_scroll_area_Q2 = QScrollArea(more_info_screen_Q2)
                        self.change_color_new(self.more_info_scroll_area_Q2, "QScrollArea")
                        self.more_info_scroll_area_Q2.setWidget(more_info_scroll_area_Q2_QWidget)
                        self.more_info_scroll_area_Q2.setWidgetResizable(True)
                        self.more_info_scroll_area_Q2.setGeometry(0, 0, 600, 600)

                        more_info_screen_E2 = QWidget()
                        more_info_scroll_area_E2_QWidget = QWidget()
                        more_info_scroll_area_E2_QWidget.setFixedSize(580, 1070)

                        self.more_info_scroll_area_E2 = QScrollArea(more_info_screen_E2)
                        self.change_color_new(self.more_info_scroll_area_E2, "QScrollArea")
                        self.more_info_scroll_area_E2.setWidget(more_info_scroll_area_E2_QWidget)
                        self.more_info_scroll_area_E2.setWidgetResizable(True)
                        self.more_info_scroll_area_E2.setGeometry(0, 0, 600, 600)

                        more_info_screen_Q3 = QWidget()
                        more_info_scroll_area_Q3_QWidget = QWidget()
                        more_info_scroll_area_Q3_QWidget.setFixedSize(580, 1070)

                        self.more_info_scroll_area_Q3 = QScrollArea(more_info_screen_Q3)
                        self.change_color_new(self.more_info_scroll_area_Q3, "QScrollArea")
                        self.more_info_scroll_area_Q3.setWidget(more_info_scroll_area_Q3_QWidget)
                        self.more_info_scroll_area_Q3.setWidgetResizable(True)
                        self.more_info_scroll_area_Q3.setGeometry(0, 0, 600, 600)

                        more_info_screen_Q4 = QWidget()
                        more_info_scroll_area_Q4_QWidget = QWidget()
                        more_info_scroll_area_Q4_QWidget.setFixedSize(580, 1070)

                        self.more_info_scroll_area_Q4 = QScrollArea(more_info_screen_Q4)
                        self.change_color_new(self.more_info_scroll_area_Q4, "QScrollArea")
                        self.more_info_scroll_area_Q4.setWidget(more_info_scroll_area_Q4_QWidget)
                        self.more_info_scroll_area_Q4.setWidgetResizable(True)
                        self.more_info_scroll_area_Q4.setGeometry(0, 0, 600, 600)

                        more_info_screen_E4 = QWidget()
                        more_info_scroll_area_E4_QWidget = QWidget()
                        more_info_scroll_area_E4_QWidget.setFixedSize(580, 1070)

                        self.more_info_scroll_area_E4 = QScrollArea(more_info_screen_E4)
                        self.change_color_new(self.more_info_scroll_area_E4, "QScrollArea")
                        self.more_info_scroll_area_E4.setWidget(more_info_scroll_area_E4_QWidget)
                        self.more_info_scroll_area_E4.setWidgetResizable(True)
                        self.more_info_scroll_area_E4.setGeometry(0, 0, 600, 600)

                        new_class.more_info_scroll_area_Q1_QWidget = more_info_scroll_area_Q1_QWidget
                        new_class.more_info_scroll_area_Q2_QWidget = more_info_scroll_area_Q2_QWidget
                        new_class.more_info_scroll_area_E2_QWidget = more_info_scroll_area_E2_QWidget
                        new_class.more_info_scroll_area_Q3_QWidget = more_info_scroll_area_Q3_QWidget
                        new_class.more_info_scroll_area_Q4_QWidget = more_info_scroll_area_Q4_QWidget
                        new_class.more_info_scroll_area_E4_QWidget = more_info_scroll_area_E4_QWidget

                        self.stacked_widget.addWidget(more_info_screen_Q1)
                        self.change_color_new(more_info_screen_Q1, "QWidget")
                        MORE_INFO_ID_Q1 = self.stacked_widget.count() - 1

                        self.stacked_widget.addWidget(more_info_screen_Q2)
                        self.change_color_new(more_info_screen_Q2, "QWidget")
                        MORE_INFO_ID_Q2 = self.stacked_widget.count() - 1

                        self.stacked_widget.addWidget(more_info_screen_E2)
                        self.change_color_new(more_info_screen_E2, "QWidget")
                        MORE_INFO_ID_E2 = self.stacked_widget.count() - 1

                        self.stacked_widget.addWidget(more_info_screen_Q3)
                        self.change_color_new(more_info_screen_Q3, "QWidget")
                        MORE_INFO_ID_Q3 = self.stacked_widget.count() - 1

                        self.stacked_widget.addWidget(more_info_screen_Q4)
                        self.change_color_new(more_info_screen_Q4, "QWidget")
                        MORE_INFO_ID_Q4 = self.stacked_widget.count() - 1

                        self.stacked_widget.addWidget(more_info_screen_E4)
                        self.change_color_new(more_info_screen_E4, "QWidget")
                        MORE_INFO_ID_E4 = self.stacked_widget.count() - 1

                        new_class.MORE_INFO_ID_Q1 = MORE_INFO_ID_Q1
                        new_class.MORE_INFO_ID_Q2 = MORE_INFO_ID_Q2
                        new_class.MORE_INFO_ID_E2 = MORE_INFO_ID_E2
                        new_class.MORE_INFO_ID_Q3 = MORE_INFO_ID_Q3
                        new_class.MORE_INFO_ID_Q4 = MORE_INFO_ID_Q4
                        new_class.MORE_INFO_ID_E4 = MORE_INFO_ID_E4

                        Q1_grade_line_edit = QLineEdit(new_class.more_info_screen)
                        Q2_grade_line_edit = QLineEdit(new_class.more_info_screen)
                        E2_grade_line_edit = QLineEdit(new_class.more_info_screen)
                        Q3_grade_line_edit = QLineEdit(new_class.more_info_screen)
                        Q4_grade_line_edit = QLineEdit(new_class.more_info_screen)
                        E4_grade_line_edit = QLineEdit(new_class.more_info_screen)

                        self.change_color_new(Q1_grade_line_edit, "QLineEdit")
                        Q1_grade_line_edit.setGeometry(90, 300, 40, 20)
                        Q1_grade_line_edit.setText("hi")

                        for name, text, y in [(Q1_grade_line_edit, new_class.Q1_grade, 300),
                            (Q2_grade_line_edit, new_class.Q2_grade, 330),
                            (E2_grade_line_edit, new_class.E2_grade, 360),
                            (Q3_grade_line_edit, new_class.Q3_grade, 390),
                            (Q4_grade_line_edit, new_class.Q4_grade, 420),
                            (E4_grade_line_edit, new_class.E4_grade, 450)]:
                            self.change_color_new(name, "QLineEdit")
                            name.setGeometry(90, y, 40, 20)
                            name.setText(str(text))
                        Q1_grade_line_edit.setText("anything")
                        Q1_grade_line_edit.setGeometry(90, 300, 40, 20)

                        new_class.Q1_grade_line_edit = Q1_grade_line_edit
                        new_class.Q2_grade_line_edit = Q2_grade_line_edit
                        new_class.E2_grade_line_edit = E2_grade_line_edit
                        new_class.Q3_grade_line_edit = Q3_grade_line_edit
                        new_class.Q4_grade_line_edit = Q4_grade_line_edit
                        new_class.E4_grade_line_edit = E4_grade_line_edit

                        '''
                        for name, text in [(Q1_grade_line_edit, str(new_class.Q1_grade)),
                                           (Q2_grade_line_edit, str(new_class.Q2_grade)),
                                           (E2_grade_line_edit, str(new_class.E2_grade)),
                                           (Q3_grade_line_edit, str(new_class.Q3_grade)),
                                           (Q4_grade_line_edit, str(new_class.Q4_grade)),
                                           (E4_grade_line_edit, str(new_class.E4_grade))]:
                            # if text is not None:
                            name.setText(text)
                        '''

                        Q1_weight_line_edit = QLineEdit(new_class.more_info_screen)
                        Q2_weight_line_edit = QLineEdit(new_class.more_info_screen)
                        E2_weight_line_edit = QLineEdit(new_class.more_info_screen)
                        Q3_weight_line_edit = QLineEdit(new_class.more_info_screen)
                        Q4_weight_line_edit = QLineEdit(new_class.more_info_screen)
                        E4_weight_line_edit = QLineEdit(new_class.more_info_screen)

                        for name, text, y in [(Q1_weight_line_edit, new_class.Q1_weight, 300),
                                              (Q2_weight_line_edit, new_class.Q2_weight, 330),
                                              (E2_weight_line_edit, new_class.E2_weight, 360),
                                              (Q3_weight_line_edit, new_class.Q3_weight, 390),
                                              (Q4_weight_line_edit, new_class.Q4_weight, 420),
                                              (E4_weight_line_edit, new_class.E4_weight, 450)]:
                            name.setGeometry(140, y, 40, 20)
                            name.setText(str(text))
                            self.change_color_new(name, "QLineEdit")

                        new_class.Q1_weight_line_edit = Q1_weight_line_edit
                        new_class.Q2_weight_line_edit = Q2_weight_line_edit
                        new_class.E2_weight_line_edit = E2_weight_line_edit
                        new_class.Q3_weight_line_edit = Q3_weight_line_edit
                        new_class.Q4_weight_line_edit = Q4_weight_line_edit
                        new_class.E4_weight_line_edit = E4_weight_line_edit

                        '''
                        for name, text in [(Q1_weight_line_edit, str(new_class.Q1_weight)),
                                           (Q2_weight_line_edit, str(new_class.Q2_weight)),
                                           (E2_weight_line_edit, str(new_class.E2_weight)),
                                           (Q3_weight_line_edit, str(new_class.Q3_weight)),
                                           (Q4_weight_line_edit, str(new_class.Q4_weight)),
                                           (E4_weight_line_edit, str(new_class.E4_weight))]:
                            name.setText(text)
                        '''

                        new_class.categories = ast.literal_eval(class_[22])

                        new_class.Q1.term_first_time = class_[23]
                        new_class.Q1.assignments = ast.literal_eval(class_[24])
                        new_class.Q1.exact_grade = class_[25]

                        new_class.Q2.term_first_time = class_[26]
                        new_class.Q2.assignments = ast.literal_eval(class_[27])
                        new_class.Q2.exact_grade = class_[28]

                        new_class.E2.term_first_time = class_[29]
                        new_class.E2.assignments = ast.literal_eval(class_[30])
                        new_class.E2.exact_grade = class_[31]

                        new_class.Q3.term_first_time = class_[32]
                        new_class.Q3.assignments = ast.literal_eval(class_[33])
                        new_class.Q3.exact_grade = class_[34]

                        new_class.Q4.term_first_time = class_[35]
                        new_class.Q4.assignments = ast.literal_eval(class_[36])
                        new_class.Q4.exact_grade = class_[37]

                        new_class.E4.term_first_time = class_[38]
                        new_class.E4.assignments = ast.literal_eval(class_[39])
                        new_class.E4.exact_grade = class_[40]

                        for term in [new_class.Q1, new_class.Q2, new_class.E2,
                                     new_class.Q3, new_class.Q4, new_class.E4]:
                            for category in new_class.categories:
                                y_offset = len(term.category_line_edits) * 30

                                category_name_line_edit = QLineEdit(term.category_scroll_area_QWidget)
                                category_name_line_edit.setObjectName("any_input_needed")
                                category_name_line_edit.setGeometry(0, y_offset, 150, 20)
                                self.change_color_new(category_name_line_edit, "QLineEdit")

                                category_weight_line_edit = QLineEdit(term.category_scroll_area_QWidget)
                                category_weight_line_edit.setGeometry(160, y_offset, 40, 20)
                                self.change_color_new(category_weight_line_edit, "QLineEdit")

                                term.category_line_edits.append([category_name_line_edit, category_weight_line_edit])

                                category_name_line_edit.setText(category[0])
                                category_weight_line_edit.setText(category[1])

                            for assignment in term.assignments:
                                y_offset = len(term.assignment_line_edits) * 30

                                assignment_category_combo_box = ComboBox(term.assignment_scroll_area_QWidget)
                                assignment_category_combo_box.setObjectName("no_input_validation")
                                assignment_category_combo_box.setGeometry(0, y_offset, 200, 20)
                                self.change_color_new(assignment_category_combo_box, "ComboBox")

                                for category in new_class.categories:
                                    assignment_category_combo_box.addItem(category[0])

                                assignment_name_line_edit = QLineEdit(term.assignment_scroll_area_QWidget)
                                assignment_name_line_edit.setObjectName("no_input_validation")
                                assignment_name_line_edit.setGeometry(210, y_offset, 120, 20)
                                self.change_color_new(assignment_name_line_edit, "QLineEdit")

                                assignment_points_received_line_edit = QLineEdit(term.assignment_scroll_area_QWidget)
                                assignment_points_received_line_edit.setGeometry(340, y_offset, 55, 20)
                                self.change_color_new(assignment_points_received_line_edit, "QLineEdit")

                                assignment_points_total_line_edit = QLineEdit(term.assignment_scroll_area_QWidget)
                                assignment_points_total_line_edit.setGeometry(405, y_offset, 55, 20)
                                self.change_color_new(assignment_points_total_line_edit, "QLineEdit")

                                term.assignment_category_combo_boxes.append(assignment_category_combo_box)
                                term.assignment_line_edits.append(
                                    [assignment_category_combo_box, assignment_name_line_edit,
                                     assignment_points_received_line_edit, assignment_points_total_line_edit])

                                assignment_category_combo_box.setCurrentText(assignment[0])
                                assignment_name_line_edit.setText(assignment[1])
                                assignment_points_received_line_edit.setText(assignment[2])
                                assignment_points_total_line_edit.setText(assignment[3])

                    for row in user_data_reader:
                        self.GPA_scale = float(row[0])
                        self.honors_weight_100 = row[1]
                        self.AP_weight_100 = row[2]
                        self.honors_weight_4 = row[3]
                        self.AP_weight_100 = row[4]
                        self.honors_weight = row[5]
                        self.AP_weight = row[6]
                        self.default_Q1_weight = row[7]
                        self.default_Q2_weight = row[8]
                        self.default_E2_weight = row[9]
                        self.default_Q3_weight = row[10]
                        self.default_Q4_weight = row[11]
                        self.default_E4_weight = row[12]
                        self.color_1 = row[13]
                        self.color_2 = row[14]

                        self.change_GPA_scale_label_quarterly.setText(f"Scale: {self.GPA_scale}")
                        self.change_GPA_scale_label_quarterly.adjustSize()
                        self.change_GPA_scale_label_cumulative.setText(f"Scale: {self.GPA_scale}")
                        self.change_GPA_scale_label_cumulative.adjustSize()

                        self.change_honors_100_weight_line_edit.setText(str(row[1]))
                        self.change_AP_100_weight_line_edit.setText(str(row[2]))
                        self.change_honors_4_weight_line_edit.setText(str(row[3]))
                        self.change_AP_4_weight_line_edit.setText(str(row[4]))

                        self.change_Q1_default_weight_line_edit.setText(str(row[7]))
                        self.change_Q2_default_weight_line_edit.setText(str(row[8]))
                        self.change_E2_default_weight_line_edit.setText(str(row[9]))
                        self.change_Q3_default_weight_line_edit.setText(str(row[10]))
                        self.change_Q4_default_weight_line_edit.setText(str(row[11]))
                        self.change_E4_default_weight_line_edit.setText(str(row[12]))

                        self.change_colors_func(first=True)

                    QMessageBox.information(self, "Loading Data", "Data loaded successfully")
                except IndexError:  # if the user edits the data
                    QMessageBox.information(self, "Loading Data Error", "Data was invalid and could not be loaded")

        class_data_file.close()
        user_data_file.close()

    def create_export_data_screen(self):
        """This function creates the elements for the exporting data screen"""

        # back button
        self.create_back_button(self.export_data_homepage, self.HOME_SCREEN)

        # top text
        self.export_data_top_text = QLabel("Export Data", self.export_data_homepage)
        self.font_size(self.export_data_top_text, 20)
        self.center_widget(self.export_data_top_text, 20)

        # buttons
        self.create_PDF_button = QPushButton("Create PDF", self.export_data_homepage)
        self.create_PDF_button.clicked.connect(lambda: self.change_screen(self.CREATE_PDF_SCREEN))
        self.font_size(self.create_PDF_button, 20)
        self.center_widget(self.create_PDF_button, 70)

        self.export_to_spreadsheet_button = QPushButton("Export to Excel Spreadsheet", self.export_data_homepage)
        self.export_to_spreadsheet_button.clicked.connect(lambda: self.change_screen(self.EXPORT_TO_SPREADSHEET_SCREEN))
        self.font_size(self.export_to_spreadsheet_button, 20)
        self.center_widget(self.export_to_spreadsheet_button, 125)

    def create_create_PDF_screen(self):
        """This controls the elements on the create PDF screen"""
        self.create_back_button(self.create_PDF_screen, self.EXPORT_DATA_HOMEPAGE)

        # top text
        self.create_PDF_top_text_1 = QLabel("Create PDF", self.create_PDF_screen)
        self.font_size(self.create_PDF_top_text_1, 25)
        self.center_widget(self.create_PDF_top_text_1, 20)

        self.create_PDF_top_text_2 = QLabel("You can either create a PDF of all of your grades "
                                            "\n or a PDF of your assignments from a specific class", self.create_PDF_screen)
        self.create_PDF_top_text_2.setAlignment(Qt.AlignCenter)
        self.font_size(self.create_PDF_top_text_2, 15)
        self.center_widget(self.create_PDF_top_text_2, 70)

        # buttons
        self.create_PDF_quarterly = QPushButton("Create PDF of all Quarterly/Annual classes", self.create_PDF_screen)
        self.create_PDF_quarterly.clicked.connect(lambda: self.create_PDF_for_all_classes("Quarterly"))
        self.font_size(self.create_PDF_quarterly, 15)
        self.center_widget(self.create_PDF_quarterly, 160)

        self.create_PDF_cumulative = QPushButton("Create PDF of all Cumulative classes", self.create_PDF_screen)
        self.create_PDF_cumulative.clicked.connect(lambda: self.create_PDF_for_all_classes("Cumulative"))
        self.font_size(self.create_PDF_cumulative, 15)
        self.center_widget(self.create_PDF_cumulative, 210)

    def create_PDF_for_all_classes(self, scope):
        """This creates a PDF for all Quarterly/Cumulative classes"""
        runnable = self.calculate_my_GPA_func(scope=scope, from_export=True)  # ensures that the function can be run
        if runnable == "error":  # if GPA can't be calculated
            QMessageBox.critical(self, "Creating PDF error", "PDF could not be made due to issues in the Calculate my GPA screen. "
                                                             "Calculate your GPA on that screen before making a PDF")
        else:
            def draw_centered_text(text, y):  # used to draw text
                '''This function centralizes elements of the PDF'''
                width = Canvas._pagesize[0]  # gets the width from [width, height]
                text_width = Canvas.stringWidth(text)  # gets the width of the text to be centralized
                x = (width - text_width) / 2  # finds the x value
                Canvas.drawString(x, y, text)  # draws the text

            years = ['8', '9', '10', '11', '12']
            # uses a class made earlier in the program
            confirm = AllClassesQMessageBox("Select an Option", "Enter your current Grade in school ", years, scope=scope, parent=self)
            y_coord = 750  # starting y_coordinate
            if confirm.exec():  # if yes
                name, year_ = confirm.get_selected_options_and_text(scope)
                file = "GPA.pdf"  # name of PDF
                Canvas = canvas.Canvas(file, pagesize=letter)  # canvas to draw on

                # information for the top
                draw_centered_text("Monroe-Woodbury High School Grade Report", y_coord)
                y_coord -= 20  # the y coordinate decreases to make sure information doesn't overlap
                draw_centered_text(name, y_coord)
                y_coord -= 20
                draw_centered_text(self.formatted_date, y_coord)
                y_coord -= 10

                if scope == "Quarterly":
                    y_coord -= 20
                    draw_centered_text(f"{year_}th Grade", y_coord)

                    y_coord -= 20
                    Canvas.drawString(150, y_coord, "Class")  # get all the categories
                    Canvas.drawString(350, y_coord, "Grade")
                    Canvas.drawString(400, y_coord, "Weight")
                    Canvas.drawString(450, y_coord, "Credit")
                    y_coord -= 20

                    for user_class in self.user_classes:  # get all the classes
                        if user_class.scope == "Quarterly" and not (user_class.grade == user_class.weight == user_class.credit == ""):
                            Canvas.drawString(150, y_coord, user_class.class_name)
                            Canvas.drawString(350, y_coord, str(round(float(user_class.grade))))
                            try:
                                if float(user_class.weight) == float(self.honors_weight):
                                    Canvas.drawString(400, y_coord, "H")
                                elif float(user_class.weight) == float(self.AP_weight):
                                    Canvas.drawString(400, y_coord, "AP")
                                else:
                                    Canvas.drawString(400, y_coord, "R")
                            except ValueError:  # sometimes the weight isn't converted
                                Canvas.drawString(400, y_coord, str(user_class.weight))
                            Canvas.drawString(450, y_coord, user_class.credit)
                            y_coord -= 20
                elif scope == "Cumulative":
                    for year in range(8, 13):  # range() is exclusive, so it goes up to 13 instead of 12
                        classes_in_this_year = 0
                        for user_class in self.user_classes:
                            if user_class.scope == "Cumulative" and user_class.year == year\
                                    and not (user_class.grade == user_class.weight == user_class.credit == ""):  # only classes for that year
                                classes_in_this_year += 1

                        if classes_in_this_year:  # if there is at least one class for that grade
                            y_coord -= 20

                            draw_centered_text(f"{year}th Grade", y_coord)
                            y_coord -= 20

                            # information about class data
                            Canvas.drawString(150, y_coord, "Class")
                            Canvas.drawString(350, y_coord, "Grade")
                            Canvas.drawString(400, y_coord, "Weight")
                            Canvas.drawString(450, y_coord, "Credit")
                            y_coord -= 20

                            for user_class in self.user_classes:
                                if user_class.scope == "Cumulative" and user_class.year == year \
                                        and not (user_class.grade == user_class.weight == user_class.credit == ""):  # only classes for that year
                                    Canvas.drawString(150, y_coord, user_class.class_name)
                                    Canvas.drawString(350, y_coord, str(round(float(user_class.grade))))
                                    try:
                                        if float(user_class.weight) == float(self.honors_weight):
                                            Canvas.drawString(400, y_coord, "H")
                                        elif float(user_class.weight) == float(self.AP_weight):
                                            Canvas.drawString(400, y_coord, "AP")
                                        else:
                                            Canvas.drawString(400, y_coord, "R")
                                    except ValueError:  # sometimes the weight isn't converted
                                        Canvas.drawString(400, y_coord, str(user_class.weight))
                                    Canvas.drawString(450, y_coord, user_class.credit)
                                    y_coord -= 20

                y_coord -= 20  # draw the GPA at the bottom of the PDF
                draw_centered_text(f"Unweighted GPA: {self.unweighted_gpa}", y_coord)
                y_coord -= 20
                draw_centered_text(f"Weighted GPA: {self.weighted_gpa}", y_coord)

                # information about weights
                y_coord -= 100
                draw_centered_text(f"Honors Scale: {self.honors_weight}", y_coord)
                y_coord -= 20
                draw_centered_text(f"AP Scale: {self.AP_weight}", y_coord)

                Canvas.save()
                webbrowser.open(file)  # opens the file

    def create_PDF_for_one_class(self):
        pass

    def create_export_to_spreadsheet_screen(self):
        """This creates the elements for the export to spreadsheet screen"""
        self.create_back_button(self.export_to_spreadsheet_screen, self.EXPORT_DATA_HOMEPAGE)

        # top text
        self.create_spreadsheet_top_text_1 = QLabel("Create Excel Spreadsheet", self.export_to_spreadsheet_screen)
        self.font_size(self.create_spreadsheet_top_text_1, 25)
        self.center_widget(self.create_spreadsheet_top_text_1, 20)

        self.create_spreadsheet_top_text_2 = QLabel("You can either create a spreadsheet of all of your grades "
                                            "\n or a spreadsheet of your assignments from a specific class", self.export_to_spreadsheet_screen)
        self.create_spreadsheet_top_text_2.setAlignment(Qt.AlignCenter)
        self.font_size(self.create_spreadsheet_top_text_2, 15)
        self.center_widget(self.create_spreadsheet_top_text_2, 70)

        # buttons
        self.create_PDF_spreadsheet_quarterly = QPushButton("Create spreadsheet of all Quarterly/Annual classes", self.export_to_spreadsheet_screen)
        self.create_PDF_spreadsheet_quarterly.clicked.connect(lambda: self.create_spreadsheet_for_all_classes("Quarterly"))
        self.font_size(self.create_PDF_spreadsheet_quarterly, 15)
        self.center_widget(self.create_PDF_spreadsheet_quarterly, 160)

        self.create_spreadsheet_cumulative = QPushButton("Create spreadsheet of all Cumulative classes", self.export_to_spreadsheet_screen)
        self.create_spreadsheet_cumulative.clicked.connect(lambda: self.create_spreadsheet_for_all_classes("Cumulative"))
        self.font_size(self.create_spreadsheet_cumulative, 15)
        self.center_widget(self.create_spreadsheet_cumulative, 210)

        self.create_spreadsheet_for_one_class_button = QPushButton("Create spreadsheet for one class", self.export_to_spreadsheet_screen)
        self.create_spreadsheet_for_one_class_button.clicked.connect(self.create_spreadsheet_for_one_class)
        self.font_size(self.create_spreadsheet_for_one_class_button, 15)
        self.center_widget(self.create_spreadsheet_for_one_class_button, 260)

    def open_file(self, filepath):
        """This is used to open an Excel file"""
        if os.name == 'nt':  # For Windows
            os.startfile(filepath)
        elif os.uname().sysname == 'Darwin':  # For macOS
            os.system('open ' + filepath)
        else:  # For Linux
            os.system('xdg-open ' + filepath)

    def create_spreadsheet_for_all_classes(self, scope):
        """This is used to create a spreadsheet for all the classes a user is taking (Quarterly or Cumulative)"""
        runnable = self.calculate_my_GPA_func(scope=scope, from_export=True)
        if runnable == "error":  # if GPA can't be calculated
            QMessageBox.critical(self, "Creating Spreadsheet error", "Spreadsheet could not be made due to issues in the Calculate my GPA screen. "
                                                                     "Calculate your GPA on that screen before making a spreadsheet")
        else:
            years = ['8', '9', '10', '11', '12']
            # uses a class made earlier in the program
            confirm = AllClassesQMessageBox("Select an Option", "Enter your current Grade in school: ", years, scope=scope, parent=self)

            if confirm.exec():  # if yes
                name, year = confirm.get_selected_options_and_text(scope)

                workbook = openpyxl.Workbook()  # opens a workbook
                worksheet = workbook.active
                worksheet.title = f"Monroe-Woodbury Grade Report"

                # information at the top
                worksheet['C1'] = "Monroe-Woodbury Grade Report"
                worksheet['C1'].alignment = Alignment(horizontal='center')
                worksheet['B2'] = "Student Name: "
                worksheet['C2'] = name
                worksheet['B3'] = "Date: "
                worksheet['C3'] = self.formatted_date

                last_row = None
                if scope == "Quarterly":
                    worksheet['A6'] = "Class Name"  # create headers
                    worksheet['B6'] = "Grade"
                    worksheet['C6'] = "Weight"
                    worksheet['D6'] = "Credit"

                    row = 7
                    for user_class in self.user_classes:  # insert information for each class
                        if user_class.scope == "Quarterly" and not (user_class.grade == user_class.weight == user_class.credit == ""):
                            worksheet[f'A{row}'] = user_class.class_name
                            worksheet[f'B{row}'] = round(float(user_class.grade))
                            worksheet[f'D{row}'] = float(user_class.credit)
                            try:
                                if float(user_class.weight) == float(self.honors_weight):
                                    worksheet[f'C{row}'] = "H"
                                elif float(user_class.weight) == float(self.AP_weight):
                                    worksheet[f'C{row}'] = "AP"
                                else:
                                    worksheet[f'C{row}'] = "R"
                            except ValueError:  # sometimes the weight isn't converted
                                worksheet[f'C{row}'] = user_class.weight

                            row += 1
                    last_row = row  # for information at the bottom of the PDF
                elif scope == "Cumulative":
                    row = 4
                    for year_ in range(8, 13):  # range() is exclusive, so it goes up to 13 instead of 12
                        classes_in_this_year = 0
                        for user_class in self.user_classes:  # each class
                            if user_class.scope == "Cumulative" and user_class.year == year_ \
                                    and not (user_class.grade == user_class.weight == user_class.credit == ""):  # only classes for that year
                                classes_in_this_year += 1

                        if classes_in_this_year:  # if there is at least one class for that grade
                            row += 2  # two spaces in between each class
                            worksheet[f'C{row}'] = f"{year_}th Grade"
                            row += 1

                            worksheet[f'A{row}'] = "Class Name"
                            worksheet[f'B{row}'] = "Grade"
                            worksheet[f'C{row}'] = "Weight"
                            worksheet[f'D{row}'] = "Credit"
                            row += 1

                            for user_class in self.user_classes:
                                # inserting information about each class
                                if user_class.scope == "Cumulative" and user_class.year == year_ \
                                        and not (user_class.grade == user_class.weight == user_class.credit == ""):  # only classes for that year
                                    worksheet[f'A{row}'] = user_class.class_name
                                    worksheet[f'B{row}'] = round(float(user_class.grade))
                                    worksheet[f'D{row}'] = float(user_class.credit)
                                    try:
                                        if float(user_class.weight) == float(self.honors_weight):
                                            worksheet[f'C{row}'] = "H"
                                        elif float(user_class.weight) == float(self.AP_weight):
                                            worksheet[f'C{row}'] = "AP"
                                        else:
                                            worksheet[f'C{row}'] = "R"
                                    except ValueError:
                                        worksheet[f'C{row}'] = user_class.weight

                                    row += 1
                    last_row = row

                # putting the GPA at the bottom
                last_row += 2
                worksheet[f'B{last_row}'] = "Unweighted GPA: "
                worksheet[f'C{last_row}'] = self.unweighted_gpa
                last_row += 1
                worksheet[f'B{last_row}'] = "Weighted GPA: "
                worksheet[f'C{last_row}'] = self.weighted_gpa

                for column in range(ord('A'), ord('E')):  # Iterate over columns 'A' to 'D'
                    col_letter = chr(column)
                    worksheet.column_dimensions[col_letter].width = 20  # made the columns wider wider

                workbook.save("class_data.xlsx")  # save the workbook

                # Open the Excel file
                self.open_file('class_data.xlsx')

    def create_spreadsheet_for_one_class(self):
        """This function creates a spreadsheet for one class"""

        if len(self.user_classes) == 0:  # if there are no classes
            QMessageBox.critical(self, "Exporting Data error", "Please enter at least one class")
        else:  # see if GPA can be calculated
            runnable = self.update_class_data(show_error=True, from_export=True, scope="Both")

            quarterly_classes = 0
            cumulative_classes = 0
            if runnable == "error":
                for user_class in self.user_classes:
                    # figure out if a scope is empty
                    if user_class.scope == "Quarterly" or user_class.scope == "Both":
                        quarterly_classes += 1
                    if user_class.scope == "Cumulative" or user_class.scope == "Both":
                        cumulative_classes += 1   # an elif isn't used as if the scope is Both, both of these should trigger
                    if quarterly_classes == 0:  # only for cumulative
                        QMessageBox.critical(self, "Exporting Data error", "Ensure that you can calculate your Cumulative GPA before exporting data")
                    elif cumulative_classes == 0:  # only for quarterly
                        QMessageBox.critical(self, "Exporting Data error", "Ensure that you can calculate your Quarterly GPA before exporting data")
                    else:  # for both
                        QMessageBox.critical(self, "Exporting Data error", "Ensure that you can calculate your GPA on both the Quarterly and Cumulative scope before exporting data")
            else:
                class_names = []
                hidden_class_names = []  # includes the class ID
                for user_class in self.user_classes:
                    if user_class.year:  # append the class name and year to help with duplicates
                        class_names.append(f"{user_class.class_name} ({user_class.year}th Grade)")
                    else:  # if no year is given on the quarterly screen
                        class_names.append(f"{user_class.class_name} (No year given)")
                    hidden_class_names.append(user_class.class_id)
                class_names.sort()  # put the classes in alphabetical order to help the user
                hidden_class_names.sort()

                options = {"Select a Class:": class_names,
                           "Select a term:": ["All (F4/F2)", "Q1", "Q2", "E2", "Q3", "Q4", "E4"]}
                # create an instance of a class made earlier in the program
                message_box = ChooseClassQMessageBox("Select an Option", "Customize your spreadsheet below: ", options, self, class_=self.user_classes)

                if message_box.exec():
                    selected_options, selected_indices, entered_text = message_box.get_selected_options_and_text(self.user_classes)
                    for user_class in self.user_classes:
                        if int(user_class.class_id) == int(hidden_class_names[selected_indices[0]]):  # if this is the correct class
                            workbook = openpyxl.Workbook()  # open a workbook
                            worksheet = workbook.active
                            worksheet.title = f"Report for {user_class.class_name}"

                            # top information
                            worksheet['C1'] = "Monroe Woodbury Class Report"
                            worksheet['C1'].alignment = Alignment(horizontal='center')
                            worksheet['B2'] = "Student Name: "
                            worksheet['C2'] = entered_text
                            worksheet['B3'] = "Date: "
                            worksheet['C3'] = self.formatted_date

                            # basic information about the class
                            worksheet['B6'] = "Class Name: "
                            worksheet['C6'] = user_class.class_name
                            worksheet['B7'] = "Grade: "
                            worksheet['C7'] = round(float(user_class.grade), 4)
                            worksheet['B9'] = "Credit: "
                            worksheet['C9'] = float(user_class.credit)

                            worksheet['B8'] = "Weight: "
                            try:
                                if float(user_class.weight) == float(self.honors_weight):
                                    worksheet['C8'] = "H"
                                elif float(user_class.weight) == float(self.AP_weight):
                                    worksheet['C8'] = "AP"
                                else:
                                    worksheet['C8'] = "R"
                            except ValueError:
                                worksheet['C8'] = user_class.weight

                            row = 13
                            # information about term grades. Each grade only shows if the grade was entered
                            if selected_indices[1] == 0:  # only for F4
                                for term, term_grade, term_weight in [["Q1", user_class.Q1_grade, user_class.Q1_weight], ["Q2", user_class.Q2_grade, user_class.Q2_weight],
                                                                      ["E2", user_class.E2_grade, user_class.E2_weight], ["Q3", user_class.Q3_grade, user_class.Q3_weight],
                                                                      ["Q4", user_class.Q4_grade, user_class.Q4_weight], ["E4", user_class.E4_grade, user_class.E4_weight]]:
                                    if term_grade:
                                        worksheet['A12'] = "Term Name"
                                        worksheet['B12'] = "Term Grade"
                                        worksheet['C12'] = "Term Weight"

                                        worksheet[f'A{row}'] = term
                                        worksheet[f'B{row}'] = round(float(term_grade), 4)
                                        worksheet[f'C{row}'] = float(term_weight)
                                        row += 1
                            else:  # for a specific term
                                worksheet['B12'] = f"{selected_options[1]} Grade: "  # Q1 Grade for example
                                for term, term_grade in [("Q1", user_class.Q1_grade), ("Q2", user_class.Q2_grade),
                                                         ("E2", user_class.E2_grade), ("Q3", user_class.Q3_grade),
                                                         ("Q4", user_class.Q4_grade), ("E4", user_class.E4_grade)]:
                                    if selected_options[1] == term:
                                        worksheet['C12'] = (round(float(term_grade)))
                                        row += 1

                            row += 2
                            worksheet[f'B{row}'] = "Grading Categories"
                            worksheet[f'B{row}'].alignment = Alignment(horizontal='right')
                            row += 1

                            worksheet[f'B{row}'] = "Category Name"
                            worksheet[f'C{row}'] = "Category Weight"
                            row += 1

                            for category in user_class.categories:  # add each category
                                worksheet[f'B{row}'] = category[0]
                                worksheet[f'C{row}'] = float(category[1])
                                row += 1

                            def create_column_names(row_):
                                """This function creates column names for each term"""
                                for name, column_ in [["Category", "A"], ["Assignment Name", "B"], ["Points Received", "C"],
                                                     ["Points Available", "D"], ["Assignment Grade", "E"]]:
                                    worksheet[f'{column_}{row_}'] = name

                            for term in ["Q1", "Q2", "E2", "Q3", "Q4", "E4"]:  # create assignments for each term
                                if selected_options[1] in ["All (F4/F2)", term]:  # if the term is all or Q1
                                    user_class.set_term(term)

                                    row += 2
                                    worksheet[f'C{row}'] = f"{term} Assignments"
                                    worksheet[f'C{row}'].alignment = Alignment(horizontal='center')
                                    row += 1

                                    create_column_names(row)
                                    row += 1

                                    # entering in information about each assignment
                                    for assignment in user_class.current_term.assignments:
                                        worksheet[f'A{row}'] = assignment[0]
                                        worksheet[f'B{row}'] = assignment[1]
                                        worksheet[f'C{row}'] = float(assignment[2])
                                        worksheet[f'D{row}'] = float(assignment[3])

                                        try:
                                            assignment_grade = float(assignment[2]) / float(assignment[3]) * 100
                                            if assignment_grade > 100:
                                                assignment_grade = 100
                                        except ZeroDivisionError:  # if the assignment is extra credit
                                            assignment_grade = 100

                                        worksheet[f'E{row}'] = round(float(assignment_grade), 2)
                                        row += 1

                            for column in range(ord('A'), ord('F')):  # Iterate over columns 'A' to 'E'
                                col_letter = chr(column)
                                worksheet.column_dimensions[col_letter].width = 20

                            workbook.save("one_class_data.xlsx")

                            # Open the Excel file
                            self.open_file('one_class_data.xlsx')

    def SQL_dynamic_backup(self, final_run=False):
        """This function backs up the data dynamically for SQL"""
        while True:  # this runs in the background with a thread
            self.update_class_data(show_error=False)  # update current data
            # delete all SQL data
            query1 = "DELETE FROM class_data WHERE userID = %s"
            my_cursor.execute(query1, (self.account_id,))
            query2 = "DELETE FROM user_data WHERE userID = %s"
            my_cursor.execute(query2, (self.account_id, ))

            for user_class in self.user_classes:
                # inserting data

                # determining the screen to insert - doing str(self.screen) wouldn't work
                temporary_screen = None  # this line makes it look better in Pycharm
                if user_class.screen == self.quarterly_GPA_screen:
                    temporary_screen = "self.quarterly_GPA_screen"
                elif user_class.screen == self.year_8_screen:
                    temporary_screen = "self.year_8_screen"
                elif user_class.screen == self.year_9_screen:
                    temporary_screen = "self.year_9_screen"
                elif user_class.screen == self.year_10_screen:
                    temporary_screen = "self.year_10_screen"
                elif user_class.screen == self.year_11_screen:
                    temporary_screen = "self.year_11_screen"
                elif user_class.screen == self.year_12_screen:
                    temporary_screen = "self.year_12_screen"

                # all data that is needed
                fields_for_classes = ["userID", "scope", "screen", "class_name", "grade", "weight", "credit",
                                      "year", "Q1_weight", "Q2_weight", "E2_weight", "Q3_weight", "Q4_weight", "E4_weight",
                                      "exact_grade", "first_time",
                                      "Q1_grade", "Q2_grade", "E2_grade", "Q3_grade", "Q4_grade", "E4_grade",
                                      "categories",
                                      "Q1_term_first_time", "Q1_assignments", "Q1_exact_grade",
                                      "Q2_term_first_time", "Q2_assignments", "Q2_exact_grade",
                                      "E2_term_first_time", "E2_assignments", "E2_exact_grade",
                                      "Q3_term_first_time", "Q3_assignments", "Q3_exact_grade",
                                      "Q4_term_first_time", "Q4_assignments", "Q4_exact_grade",
                                      "E4_term_first_time", "E4_assignments", "E4_exact_grade",]
                # dictionary to store the data
                data_for_classes = {
                    "userID": self.account_id,
                    "scope": user_class.scope,
                    "screen": temporary_screen,
                    "class_name": user_class.class_name,
                    "grade": user_class.grade,
                    "weight": user_class.weight,
                    "credit": user_class.credit,
                    "year": user_class.year,
                    "Q1_weight": user_class.Q1_weight,
                    "Q2_weight": user_class.Q2_weight,
                    "E2_weight": user_class.E2_weight,
                    "Q3_weight": user_class.Q3_weight,
                    "Q4_weight": user_class.Q4_weight,
                    "E4_weight": user_class.E4_weight,
                    "exact_grade": user_class.exact_grade,
                    "first_time": user_class.first_time,
                    "Q1_grade": user_class.Q1_grade,
                    "Q2_grade": user_class.Q2_grade,
                    "E2_grade": user_class.E2_grade,
                    "Q3_grade": user_class.Q3_grade,
                    "Q4_grade": user_class.Q4_grade,
                    "E4_grade": user_class.E4_grade,
                    "categories": str(user_class.categories),  # a string instead of a list
                    "Q1_term_first_time": user_class.Q1.term_first_time,
                    "Q1_assignments": str(user_class.Q1.assignments),
                    "Q1_exact_grade": user_class.Q1.exact_grade,
                    "Q2_term_first_time": user_class.Q2.term_first_time,
                    "Q2_assignments": str(user_class.Q2.assignments),
                    "Q2_exact_grade": user_class.Q2.exact_grade,
                    "E2_term_first_time": user_class.E2.term_first_time,
                    "E2_assignments": str(user_class.E2.assignments),
                    "E2_exact_grade": user_class.E2.exact_grade,
                    "Q3_term_first_time": user_class.Q3.term_first_time,
                    "Q3_assignments": str(user_class.Q3.assignments),
                    "Q3_exact_grade": user_class.Q3.exact_grade,
                    "Q4_term_first_time": user_class.Q4.term_first_time,
                    "Q4_assignments": str(user_class.Q4.assignments),
                    "Q4_exact_grade": user_class.Q4.exact_grade,
                    "E4_term_first_time": user_class.E4.term_first_time,
                    "E4_assignments": str(user_class.E4.assignments),
                    "E4_exact_grade": user_class.E4.exact_grade,
                }

                placeholders = ', '.join(['%s'] * len(fields_for_classes))  # Create placeholders for the SQL query
                field_names = ', '.join(fields_for_classes)  # Join the field names for the SQL query
                query3 = f"INSERT INTO class_data ({field_names}) VALUES ({placeholders})"  # Create the SQL query
                values = [data_for_classes[field] for field in fields_for_classes]  # Extract the values from the data dictionary
                my_cursor.execute(query3, values)  # Execute the query
                db.commit()  # Commit the transaction

            # for user data
            fields_for_non_classes = ["userID", "username", "password", "email", "GPA_scale",
                                      "honors_weight_100", "AP_weight_100", "honors_weight_4", "AP_weight_4", "honors_weight", "AP_weight",
                                      "default_Q1_weight", "default_Q2_weight", "default_E2_weight", "default_Q3_weight",
                                      "default_Q4_weight", "default_E4_weight", "color_1", "color_2"]
            data_for_non_classes = {
                "userID": self.account_id,
                "username": self.username,
                "password": self.password,
                "email": self.email,
                "GPA_scale": self.GPA_scale,
                "honors_weight_100": self.honors_weight_100,
                "AP_weight_100": self.AP_weight_100,
                "honors_weight_4": self.honors_weight_4,
                "AP_weight_4": self.AP_weight_4,
                "honors_weight": self.honors_weight,
                "AP_weight": self.AP_weight,
                "default_Q1_weight": self.default_Q1_weight,
                "default_Q2_weight": self.default_Q2_weight,
                "default_E2_weight": self.default_E2_weight,
                "default_Q3_weight": self.default_Q3_weight,
                "default_Q4_weight": self.default_Q4_weight,
                "default_E4_weight": self.default_E4_weight,
                "color_1": self.color_1,
                "color_2": self.color_2
            }

            placeholders = ', '.join(['%s'] * len(fields_for_non_classes))  # Create placeholders for the SQL query
            field_names = ', '.join(fields_for_non_classes)  # Join the field names for the SQL query
            query4 = f"INSERT INTO user_data ({field_names}) VALUES ({placeholders})"  # Create the SQL query
            values = [data_for_non_classes[field] for field in fields_for_non_classes]  # Extract the values from the data dictionary
            my_cursor.execute(query4, values)  # Execute the query
            db.commit()  # Commit the transaction

            if final_run:  # the end of the program
                break
            time.sleep(2)  # run once per 2 seconds

    def csv_backup(self):
        """This function backs up the data to be saved locally"""
        self.update_class_data(show_error=False)  # update the class data
        # Open the file in append mode
        with open('gpa_calculator_class_data.csv', mode='a', newline='') as file:
            file.truncate(0)  # delete the file

            for user_class in self.user_classes:

                # get the screens, can't easily be turned into strings with str()
                temporary_screen = None  # this line makes it look better in Pycharm
                if user_class.screen == self.quarterly_GPA_screen:
                    temporary_screen = "self.quarterly_GPA_screen"
                elif user_class.screen == self.year_8_screen:
                    temporary_screen = "self.year_8_screen"
                elif user_class.screen == self.year_9_screen:
                    temporary_screen = "self.year_9_screen"
                elif user_class.screen == self.year_10_screen:
                    temporary_screen = "self.year_10_screen"
                elif user_class.screen == self.year_11_screen:
                    temporary_screen = "self.year_11_screen"
                elif user_class.screen == self.year_12_screen:
                    temporary_screen = "self.year_12_screen"
                # fields to save data
                fields_for_classes = ["class_id", "scope", "screen", "class_name", "grade", "weight", "credit",
                                      "year", "Q1_weight", "Q2_weight", "E2_weight", "Q3_weight", "Q4_weight", "E4_weight",
                                      "exact_grade", "first_time",
                                      "Q1_grade", "Q2_grade", "E2_grade", "Q3_grade", "Q4_grade", "E4_grade",
                                      "categories",
                                      "Q1_term_first_time", "Q1_assignments", "Q1_exact_grade",
                                      "Q2_term_first_time", "Q2_assignments", "Q2_exact_grade",
                                      "E2_term_first_time", "E2_assignments", "E2_exact_grade",
                                      "Q3_term_first_time", "Q3_assignments", "Q3_exact_grade",
                                      "Q4_term_first_time", "Q4_assignments", "Q4_exact_grade",
                                      "E4_term_first_time", "E4_assignments", "E4_exact_grade"]
                # dictionary to store the data
                data_for_classes = {
                    "class_id": user_class.class_id,
                    "scope": user_class.scope,
                    "screen": temporary_screen,
                    "class_name": user_class.class_name,
                    "grade": user_class.grade,
                    "weight": user_class.weight,
                    "credit": user_class.credit,
                    "year": user_class.year,
                    "Q1_weight": user_class.Q1_weight,
                    "Q2_weight": user_class.Q2_weight,
                    "E2_weight": user_class.E2_weight,
                    "Q3_weight": user_class.Q3_weight,
                    "Q4_weight": user_class.Q4_weight,
                    "E4_weight": user_class.E4_weight,
                    "exact_grade": user_class.exact_grade,
                    "first_time": user_class.first_time,
                    "Q1_grade": user_class.Q1_grade,
                    "Q2_grade": user_class.Q2_grade,
                    "E2_grade": user_class.E2_grade,
                    "Q3_grade": user_class.Q3_grade,
                    "Q4_grade": user_class.Q4_grade,
                    "E4_grade": user_class.E4_grade,
                    "categories": user_class.categories,
                    "Q1_term_first_time": user_class.Q1.term_first_time,
                    "Q1_assignments": user_class.Q1.assignments,
                    "Q1_exact_grade": user_class.Q1.exact_grade,
                    "Q2_term_first_time": user_class.Q2.term_first_time,
                    "Q2_assignments": user_class.Q2.assignments,
                    "Q2_exact_grade": user_class.Q2.exact_grade,
                    "E2_term_first_time": user_class.E2.term_first_time,
                    "E2_assignments": user_class.E2.assignments,
                    "E2_exact_grade": user_class.E2.exact_grade,
                    "Q3_term_first_time": user_class.Q3.term_first_time,
                    "Q3_assignments": user_class.Q3.assignments,
                    "Q3_exact_grade": user_class.Q3.exact_grade,
                    "Q4_term_first_time": user_class.Q4.term_first_time,
                    "Q4_assignments": user_class.Q4.assignments,
                    "Q4_exact_grade": user_class.Q4.exact_grade,
                    "E4_term_first_time": user_class.E4.term_first_time,
                    "E4_assignments": user_class.E4.assignments,
                    "E4_exact_grade": user_class.E4.exact_grade,
                }

                # insert the data
                writer = csv.DictWriter(file, fieldnames=fields_for_classes)
                writer.writerow(data_for_classes)

        # save user data
        with open('gpa_calculator_user_data.csv', mode='a', newline='') as file:
            file.truncate(0)  # delete the file

            # fields for user data
            fields_for_non_classes = ["GPA_scale", "honors_weight_100", "AP_weight_100", "honors_weight_4", "AP_weight_4", "honors_weight", "AP_weight",
                                      "default_Q1_weight", "default_Q2_weight", "default_E2_weight", "default_Q3_weight",
                                      "default_Q4_weight", "default_E4_weight", "color_1", "color_2"]
            data_for_non_classes = {
                "GPA_scale": self.GPA_scale,
                "honors_weight_100": self.honors_weight_100,
                "AP_weight_100": self.AP_weight_100,
                "honors_weight_4": self.honors_weight_4,
                "AP_weight_4": self.AP_weight_4,
                "honors_weight": self.honors_weight,
                "AP_weight": self.AP_weight,
                "default_Q1_weight": self.default_Q1_weight,
                "default_Q2_weight": self.default_Q2_weight,
                "default_E2_weight": self.default_E2_weight,
                "default_Q3_weight": self.default_Q3_weight,
                "default_Q4_weight": self.default_Q4_weight,
                "default_E4_weight": self.default_E4_weight,
                "color_1": self.color_1,
                "color_2": self.color_2
            }

            # insert the data
            writer = csv.DictWriter(file, fieldnames=fields_for_non_classes)
            writer.writerow(data_for_non_classes)

    def save_data_when_program_finished(self, sig, frame) -> None:
        if window.logged_in:
            window.SQL_dynamic_backup(final_run=True)
        window.csv_backup()

    def lines_edits_valid(self, line_edit):
        """This class determines if a line edit needs input validation"""
        if line_edit.objectName() == "no_input_validation":  # class name, assignment name, assignment category combo box
            return True
        elif line_edit.objectName() == "any_input_needed":  # category combo box
            return line_edit.text()
        elif line_edit.objectName() == "6_chars_needed":  # username
            return len(line_edit.text()) >= 6
        elif line_edit.objectName() == "password":  # password
            return len(line_edit.text()) >= 6 and self.valid_password(line_edit.text())
        elif line_edit.objectName() == "email_line_edit":  # emails
            # if it's a valid email or if it's blank
            return re.match(self.email_pattern, line_edit.text()) is not None or line_edit.text() == ""
        elif line_edit.objectName() == "none_or_float":  # term grade
            if line_edit.text() == "":
                return True
            try:  # if the grade is between 0 and 100
                return 0.0 <= float(line_edit.text()) <= 100
            except ValueError:  # if the grade isn't float
                return False
        elif line_edit.objectName() == "grade_line_edit":  # grade
            if self.GPA_scale == float(100.0):  # if 100.0 scale
                try:  # if the grade is between 0 and 100
                    return 0.0 <= float(line_edit.text()) <= 100
                except ValueError:  # if the grade isn't float
                    return False
            elif self.GPA_scale == float(4.0):
                if line_edit.text() in self.letter_to_4:  # if letter grade
                    return True
                else:
                    try:  # if between 0 and 100
                        return 0.0 <= float(line_edit.text()) <= 100
                    except ValueError:  # if not float
                        return False
        else:  # if the text is a positive number
            return line_edit.text().replace('.', '', 1).isdigit()

    def combo_boxes_valid(self, combo_box):
        """Determines if a combo box needs input validation"""
        if combo_box.objectName() == "no_input_validation":
            return True
        return combo_box.currentText()  # this would only be for weight combo box

    def find_scroll_area(self, widget):
        """This functions determines which scroll area a grade, credit, or weight widget is from"""
        if widget.parent() == self.quarterly_scroll_area_QWidget:
            return self.quarterly_classes_scroll_area  # quarterly screen
        elif widget.parent() == self.year_8_scroll_area_QWidget:
            return self.year_8_scroll_area
        elif widget.parent() == self.year_9_scroll_area_QWidget:
            return self.year_9_scroll_area
        elif widget.parent() == self.year_10_scroll_area_QWidget:
            return self.year_10_scroll_area
        elif widget.parent() == self.year_11_scroll_area_QWidget:
            return self.year_11_scroll_area
        elif widget.parent() == self.year_12_scroll_area_QWidget:
            return self.year_12_scroll_area

    def input_validation(self):
        """This function creates error signs that act as input validation"""
        try:
            for line_edit, id_ in self.all_line_edits:  # delete all error signs for line edits
                if line_edit not in self.findChildren(QLineEdit):
                    for i, error_sign in enumerate(self.error_signs_line_edits):
                        if i == id_:
                            error_sign.setParent(None)
            self.all_line_edits.clear()

            for combo_box, id_ in self.all_combo_boxes:  # delete all error signs for combo boxes
                if combo_box not in self.findChildren(ComboBox):
                    for index, error_sign in enumerate(self.error_signs_combo_boxes):
                        if index == id_:
                            error_sign.setParent(None)
            self.all_combo_boxes.clear()

            for line_edit in self.findChildren(QLineEdit):  # every line edit
                sign = self.error_signs_line_edits[self.error_sign_number_line_edits]  # assign an error sign
                if not self.lines_edits_valid(line_edit):  # if the line edit has an issue
                    sign.setParent(line_edit.parent())  # set the sign to the correct screen
                    # move the sign
                    sign.move(line_edit.x() + line_edit.width() - 20, line_edit.y() + line_edit.height() - 20)
                    sign.show()  # show the sign

                    # these next lines determine the error message to show
                    if line_edit.objectName() == "any_input_needed":    # category line edit
                        self.create_hover_help_text(sign, "This field requires an input of any type")
                    elif line_edit.objectName() == "grade_line_edit":  # changes based on GPA scale
                        if float(self.GPA_scale) == 100.0:
                            self.create_hover_help_text(sign, "Must be a number from 0 to 100. \n"
                                                              "Use the 4.0 scale for letter grades", scroll_area=self.find_scroll_area(line_edit))
                        elif float(self.GPA_scale) == 4.0:
                            self.create_hover_help_text(sign, "Must be a number from 0 to 100 or a valid letter grade", scroll_area=self.find_scroll_area(line_edit))
                    elif line_edit.objectName() == "none_or_float":  # term grade
                        self.create_hover_help_text(sign, "Must be a number from 0 to 100")
                    elif line_edit.objectName() == "6_chars_needed":  # username
                        self.create_hover_help_text(sign, "Usernames must be at least 6 characters long")
                    elif line_edit.objectName() == "password":  # password
                        self.create_hover_help_text(sign, "Password must have at least 6 letters, at least one number, \n"
                                                          "at least one special symbol, and at least one capital letter")
                    elif line_edit.objectName() == "credit_line_edit":  # credit
                        self.create_hover_help_text(sign, "Must be a positive number", scroll_area=self.find_scroll_area(line_edit))
                    elif line_edit.objectName() == "email_line_edit":  # email
                        self.create_hover_help_text(sign, "Must be a valid email")
                    else:  # everything else
                        self.create_hover_help_text(sign, "Must be a positive number")
                else:
                    sign.setParent(None)  # remove the sign from the screen
                self.all_line_edits.append([line_edit, self.error_sign_number_line_edits])
                self.error_sign_number_line_edits += 1  # for the next line edit

            for i, combo_box in enumerate(self.findChildren(ComboBox)):  # all combo boxes
                sign = self.error_signs_combo_boxes[self.error_sign_number_combo_boxes]
                if not self.combo_boxes_valid(combo_box):  # if not valid
                    sign.setParent(combo_box.parent())  # create sign
                    # move the sign
                    sign.move(combo_box.x() + 5, combo_box.y() + combo_box.height() - 20)
                    sign.show()  # show the sign
                    # error message, only for credit combo box
                    self.create_hover_help_text(sign, "Please fill out this field", scroll_area=self.find_scroll_area(combo_box))
                else:
                    sign.setParent(None)
                self.all_combo_boxes.append([combo_box, self.error_sign_number_combo_boxes])
                self.error_sign_number_combo_boxes += 1

        except IndexError:  # if there are more than 500 line_edits or combo_boxes on one screen, this will occur
            # this is very unlikely
            pass
        except RuntimeError:  # this error occurs whenever the user enters some message boxes, such as changing color or exporting data
            # the error is harmless when dealt with in this manner
            pass

        self.error_sign_number_line_edits = 0  # resets the index back to zero for the next iteration
        self.error_sign_number_combo_boxes = 0


# This block checks if the script is being run directly (as opposed to being imported as a module)
if __name__ == "__main__":
    app = QApplication(sys.argv)  # creates an instance of QApplication
    window = Window()  # instance of the Window class

    window.show()  # displays the GUI
    app.exec()  # starts the application

    if window.logged_in:
        window.SQL_dynamic_backup(final_run=True)
    window.csv_backup()

