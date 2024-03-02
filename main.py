'''
Notes -
The position of many x positions of a widget being placed are centred.
If they are centered in the middle of the screen, for example, the x position was found by 300 (half of the oringial screen size, changed with x_location_change) subtracted by half tie width of the widget
If there is an identifier that could be for cumulative or quarterly but which one it is isn't in the name, it is likely quarterly
Classes should be unique in name, but there is nothing forcing that in most cases. The second class of that name may be forgotten when data is imported
'''

#importing tkinter, the messagebox module, and simpledialog. Everything from tkinter is imported for convenience
from tkinter import * #tkinter may need to be install with pip in some instances
from tkinter import messagebox, simpledialog
from math import factorial #needed to make a big number for the maximum grade to convert to an A+

import os #needed to find the size of the file
import signal #detects KeyboardInterrupt
import sys #will be needed to end the program if there is KeyboardInterrupt

#these modules deal with making the pdf
#if reportlab can not be installed with pip for whatever reason, comment out these lines and put pass in save_my_gpa_func in LoadingData, commenting everything else out
from reportlab.lib.pagesizes import letter #reportlab must be installed with pip
from reportlab.pdfgen import canvas
import webbrowser #opens the PDF
import datetime #to get the date

#to access docstrings, put help(FUNCTION/CLASS NAME) at the very end of the code, then exit out of the window and look at the print area

#creating the window
window = Tk()
window.geometry("700x700")
window.title("GPA Calculator")

#Setting some constants. Using these make it easier to change the entire program at once
BACKGROUND_COLOR = "#481c1c"
FONT = "Times New Roman"
TEXTCOLOR = "#66ff33"

#setting the background color for the GUI
window.config(background=BACKGROUND_COLOR)

#this variable determines what screen is being displayed
screen = "home"

#these variables will be used to prevent entry boxes from entering in data multiple times (ie, "17" would only appear once, not "1717171717171...")
first_frame_cumulative_GPA = True
first_frame_settings = True
first_frame_previous_data_classes = True

data_loaded = False #Used to prevent data from being loaded in multiple times
gpa_calculated = False #To prevent bugs, the GPA must be calculated before exporting data
x_location_change = 0 #used to make the widgets in the center the screen no matter the size of the window
time = 0 #used for fps

error_sign = PhotoImage(file="error.png") #import an image

#if there is a problem with importing the image, comment out the error_sign line (that defines the image), and comment out the line in the for loop that creates the error_label widget
#then, put the line below into the for loop
#error_label = Label(window, bg="red", width=2)

#this makes 1000 error_labels (more than what would ever be in the program)
error_labels = []
for label in range(1000):
    error_label = Label(window, image=error_sign, bg=BACKGROUND_COLOR)
    error_labels.append(error_label)


file_path = "data_for_calc_gpa.txt" #makes a file or gets a pre-existing one
previous_data_all = [] #this is where previous data will be imported
previous_data_classes = [] #this only includes previous data about each class, not things such as weighting and scale

file_append = open(file_path, 'a') #opens the file to write and read it
file_read = open(file_path, "r")

#this program uses classes to help organize the code
class HomeScreen:
    '''The HomeScreen class controls the elements that appear when the user starts the program'''
    def __init__(self):
        '''This function makes the widgets that will appear on the home screen. It also creates the universal back button'''
        self.intro_text = Label(window, text="Welcome to the GPA Calculator!", bg=BACKGROUND_COLOR, fg=TEXTCOLOR, font=(FONT, 30))
        self.calc_my_gpa = Button(window, text="Calculate my GPA", command=self.calc_my_gpa_button_func, font=(FONT, 30),
                                  bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR,
                                  activeforeground=TEXTCOLOR)
        self.help = Button(window, text="Help", command=self.help_func, font=(FONT, 30),
                                  bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR,
                                  activeforeground=TEXTCOLOR)
        self.data_information = Button(window, text="Data Information", command=self.data_information_func, font=(FONT, 30),
                                  bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR,
                                  activeforeground=TEXTCOLOR)

        #universal back button, used throughout the program
        self.universal_back_button = Button(window, text="Back", command=self.universal_back_button_func,
                                            font=(FONT, 20), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)

    def calc_my_gpa_button_func(self):
        '''When the button is pressed, the screen will change to the GPA home screen. It also gives the user a chance to load in their data before it's deleted'''
        global screen, file_append
        if os.path.getsize("data_for_calc_gpa.txt") and not data_loaded:
            #if data has not yet been loaded but there is data in the file, this will inform the user to import the data or it will be deleted (to prevent unexpected behavior)
            answer = messagebox.askyesno("Data not loaded",
                                         "There is data that can be imported by going to the Data Information screen. \nWould you like to get that data? \nClick Yes for a chance to load in that data by going into Data Information, click No to delete the data and continue with the program.")
            if answer: #yes, load in data
                pass #it doesn't change the screen at all
            else:
                file_append.truncate(0) #make file empty
                screen = "GPA_home"
        else:
            screen = "GPA_home" #changes screen to GPA home screen (choose from quarterly or cumulative GPA)

    def help_func(self):
        '''When the button is pressed, the screen will change to the help menu. It also gives the user a chance to load in their data before it's deleted'''
        global screen, file_append
        if os.path.getsize("data_for_calc_gpa.txt") and not data_loaded:
            #if data has not yet been loaded but there is data in the file, this will inform the user to import the data or it will be deleted (to prevent unexpected behavior)
            answer = messagebox.askyesno("Data not loaded",
                                         "There is data that can be imported by going to the Data Information screen. If you click no, that data will be lost.")
            if answer: #yes, load in data
                pass #it doesn't change the screen at all
            else:
                file_append.truncate(0) #clear file
                screen = "help_menu"
        else:
            screen = "help_menu"

    def data_information_func(self):
        '''When the button is pressed, the screen will change to the data menu'''
        global screen
        screen = "data_menu"

    def universal_back_button_func(self):
        '''When the back button is pressed, the user will be brought to a previous screen based on the screen they are currently on'''
        global screen
        if screen in ["GPA_home", "help_menu", "data_menu"]:
            screen = "home" #at the first screen after the home menu, if back is pressed, the user will go back to the home menu
        elif screen in ["instructions_1", "instructions_2", "settings"]:
            screen = "help_menu" #within the screens of the help menu, the user will be brought to the help menu hold back if the back button is pressed
        elif screen in ["quarterly_grades", "cumulative_grades"]:
            screen = "GPA_home" #within the screens of the GPA menu, the user will go back to the GPA home page
        elif screen == "class_term_grades_chooser_8":
            screen = "more_8" #within the class term grades chooser screen for more_8, if back is pressed, they will go back to more_8
        elif screen == "class_term_grades_chooser_9":
            screen = "more_9" #within the class term grades chooser screen for more_9, if back is pressed, they will go back to more_9
        elif screen == "class_term_grades_chooser_10":
            screen = "more_10" #within the class term grades chooser screen for more_10, if back is pressed, they will go back to more_10
        elif screen == "class_term_grades_chooser_11":
            screen = "more_11" #within the class term grades chooser screen for more_11, if back is pressed, they will go back to more_11
        elif screen == "class_term_grades_chooser_12":
            screen = "more_12" #within the class term grades chooser screen for more_12, if back is pressed, they will go back to more_12
        elif screen in ["more_8", "more_9", "more_10", "more_11", "more_12"]:
            screen = "cumulative_grades" #if the user is on the more screen for a grade, they will go back to cumulative_grades home screen

class GPACalculator:
    '''The GPACalculator class controls the elements after the user hits Calculate my GPA from the home screen'''
    def __init__(self):
        '''This defines all the widgets for the GPA home screen'''
        #These three widgets appear on the first screen
        self.gpa_text = Label(window, text="Choose scope of GPA", font=(FONT, 30), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.quarterly_button = Button(window, text="Quarterly", command=self.quarterly_button_func, font=(FONT, 30),
                               bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.cumulative_button = Button(window, text="Annual/Cumulative", command=self.cumulative_button_func, font=(FONT, 30),
                          bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)

        #define numbers
        self.y_var_quarterly = 150 #these numbers allow the widgets to be placed correctly when a new class is made. This one is for quarterly GPA.
        self.year_8_classes_y_var = 60 #this is for the 8th grade screen
        self.year_9_classes_y_var = 60 #this is for the 9th grade screen
        self.year_10_classes_y_var = 60 #this is for the 10th grade screen
        self.year_11_classes_y_var = 60 #this is for the 11th grade screen
        self.year_12_classes_y_var = 60 #this is for the 12th grade screen
        self.gpa_scale = 100.0 #determines if the GPA will be 100.0 or 4.0 based on user input

        self.honors_scale_100 = 1.03 #determines the scales for honors and AP classes on 100.0 and 4.0 scale, which can be changed based in the settings
        self.AP_scale_100 = 1.05
        self.honors_scale_4 = 1.125
        self.AP_scale_4 = 1.25

        self.default_Q1 = 21.25 #determines the default % of each term on the class term grades chooser screen, which can be changed in the settings
        self.default_Q2 = 21.25
        self.default_Q3 = 21.25
        self.default_Q4 = 21.25
        self.default_E2 = 5
        self.default_E4 = 10

        self.honors_scale = self.honors_scale_100 #changes the honors and AP scale based on the scale (100.0 or 4.0)
        self.AP_scale = self.AP_scale_100
        self.unweighted_gpa = '' #this is the GPA that will be displayed before the user hits calculate my GPA (an empty string)
        self.weighted_gpa = ''

        self.class_data_quarterly = [] #stores data for each of the user's classes on the quarterly screen
        self.class_data_cumulative = [] #stores data for each of the user's classes on the cumulative screen
        self.for_export = [] #this is the information that will be saved in a file at the end of the program
        self.data2 = [] #this is based on the information of quarterly and cumulative class data, and will be used in the function that calculates the user's GPA
        self.term_info_widgets = [] #this stores the widgets on the class term grade chooser screen

        #this stores the grades for the 4.0 scale
        self.grades_4 = {"A+": 4.0, "A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7,
                         "C+": 2.3, "C": 2.0, "C-": 1.7, "D+": 1.3, "D": 1.0, "F": 0.0}
        # Converts numerical grades to letter grades, with factorial(999) basically being infinity
        self.grade_ranges_4 = {"A+": range(97, factorial(999)), "A": range(93, 97), "A-": range(90, 93), "B+": range(87, 90),
                               "B": range(83, 87), "B-": range(80, 83), "C+": range(77, 80), "C": range(73, 77),
                               "C-": range(70, 73), "D+": range(67, 70), "D": range(65, 67), "F": range(0, 65)}

        #this the text at the top of the window for quarterly GPA
        self.quarterly_top = Label(window, text="Fill in the information requested\n Add new classes as needed\nHit Calculate my GPA for your weighted and unweighted GPA", bg=BACKGROUND_COLOR, fg=TEXTCOLOR, font=(FONT, 12))

        #this is determine if the GPA is on the 100.0 or 4.0 scale
        self.GPA_type_label = Label(window, text="Scale:", bg=BACKGROUND_COLOR, fg=TEXTCOLOR, font=(FONT, 12))
        self.current_scale = Label(window, text=self.gpa_scale, bg=BACKGROUND_COLOR, fg=TEXTCOLOR, font=(FONT, 12))
        self.change_scale = Button(window, text="Change Scale", command=self.change_scale_func, font=(FONT, 12),
                                   bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)

        #this is the text above the entry area for quarterly GPA
        self.class_name_label = Label(window, text="Class Name", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.grade_label = Label(window, text="Grade", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.weight_label = Label(window, text="Weight", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.credit_label = Label(window, text="Credit", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)

        #these are the buttons at the bottom of the window (add class, delete class, calculate GPA)
        self.add_new_class = Button(window, text="Add New Class", command=self.add_new_class_quarterly_func, font=(FONT, 20), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.delete_class = Button(window, text="Delete Class", command=self.delete_class_quarterly_func, font=(FONT, 20), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.whats_my_gpa = Button(window, text="Calculate my GPA", command=self.whats_my_gpa_func, font=(FONT, 20), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)

        #this is where the gpa is displayed
        self.unweighted_gpa_label = Label(window, text=f"Unweighted GPA: {self.unweighted_gpa}", font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.weighted_gpa_label = Label(window, text=f"Weighted GPA: {self.weighted_gpa}", font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)

        #This is the text at the top of the cumulative GPA home screen
        self.Cumulative_GPA_text = Label(window, text="Fill in the information requested for each grade\n Add new classes as needed\nHit Calculate my GPA for your cumulative weighted and unweighted GPA", bg=BACKGROUND_COLOR, fg=TEXTCOLOR, font=(FONT, 12))

        #these are labels that display each grade on the cumulative home screen
        self.year_8_label = Label(window, text="8th Grade", bg=BACKGROUND_COLOR, fg=TEXTCOLOR, font=(FONT, 12))
        self.year_9_label = Label(window, text="9th Grade", bg=BACKGROUND_COLOR, fg=TEXTCOLOR, font=(FONT, 12))
        self.year_10_label = Label(window, text="10th Grade", bg=BACKGROUND_COLOR, fg=TEXTCOLOR, font=(FONT, 12))
        self.year_11_label = Label(window, text="11th Grade", bg=BACKGROUND_COLOR, fg=TEXTCOLOR, font=(FONT, 12))
        self.year_12_label = Label(window, text="12th Grade", bg=BACKGROUND_COLOR, fg=TEXTCOLOR, font=(FONT, 12))

        #these are the buttons on the cumulative GPA home screen that bring you to the sub screen to input more information about each grade
        self.more_8 = Button(window, text="More", command=self.more_8_func, font=(FONT, 30), bg=BACKGROUND_COLOR,
                             fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.more_9 = Button(window, text="More", command=self.more_9_func, font=(FONT, 30), bg=BACKGROUND_COLOR,
                             fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.more_10 = Button(window, text="More", command=self.more_10_func, font=(FONT, 30), bg=BACKGROUND_COLOR,
                              fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.more_11 = Button(window, text="More", command=self.more_11_func, font=(FONT, 30), bg=BACKGROUND_COLOR,
                              fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.more_12 = Button(window, text="More", command=self.more_12_func, font=(FONT, 30), bg=BACKGROUND_COLOR,
                              fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)

        #Widgets for each column in 8th Grade, as well as label at the top of the 8th Grade screen
        self.top_8 = Label(window, text="8th Grade", font=(FONT, 30), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.class_name_label_8 = Label(window, text="Class Name", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.grade_label_8 = Label(window, text="Grade", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.weight_label_8 = Label(window, text="Weight", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.credit_label_8 = Label(window, text="Credit", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)

        #add or delete a class for 8th Grade
        self.add_class_8 = Button(window, text="Add Class", command=lambda: self.add_class_cumulative_func(year=8), font=(FONT, 20), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.delete_class_8 = Button(window, text="Delete Class", command=lambda: self.delete_class_cumulative_func(year=8), font=(FONT, 20), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)


        #Widgets for each column in 9th Grade, as well as label at the top of the 9th Grade screen
        self.top_9 = Label(window, text="9th Grade", font=(FONT, 30), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.class_name_label_9 = Label(window, text="Class Name", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.grade_label_9 = Label(window, text="Grade", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.weight_label_9 = Label(window, text="Weight", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.credit_label_9 = Label(window, text="Credit", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)

        #add or delete a class for 9th Grade
        self.add_class_9 = Button(window, text="Add Class", command=lambda: self.add_class_cumulative_func(year=9), font=(FONT, 20), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.delete_class_9 = Button(window, text="Delete Class", command=lambda: self.delete_class_cumulative_func(year=9), font=(FONT, 20), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)

        #Widgets for each column in 10th Grade, as well as label at the top of the 10th Grade screen
        self.top_10 = Label(window, text="10th Grade", font=(FONT, 30), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.class_name_label_10 = Label(window, text="Class Name", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.grade_label_10 = Label(window, text="Grade", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.weight_label_10 = Label(window, text="Weight", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.credit_label_10 = Label(window, text="Credit", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)

        #add or delete a class for 10th Grade
        self.add_class_10 = Button(window, text="Add Class", command=lambda: self.add_class_cumulative_func(year=10), font=(FONT, 20), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.delete_class_10 = Button(window, text="Delete Class", command=lambda: self.delete_class_cumulative_func(year=10), font=(FONT, 20), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)

        #Widgets for each column in 11th Grade, as well as label at the top of the 11th Grade screen
        self.top_11 = Label(window, text="11th Grade", font=(FONT, 30), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.class_name_label_11 = Label(window, text="Class Name", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.grade_label_11 = Label(window, text="Grade", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.weight_label_11 = Label(window, text="Weight", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.credit_label_11 = Label(window, text="Credit", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)

        #add or delete a class for 11th Grade
        self.add_class_11 = Button(window, text="Add Class", command=lambda: self.add_class_cumulative_func(year=11), font=(FONT, 20), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.delete_class_11 = Button(window, text="Delete Class", command=lambda: self.delete_class_cumulative_func(year=11), font=(FONT, 20), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)

        #Widgets for each column in 12th Grade, as well as label at the top of the 12th Grade screen
        self.top_12 = Label(window, text="12th Grade", font=(FONT, 30), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.class_name_label_12 = Label(window, text="Class Name", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.grade_label_12 = Label(window, text="Grade", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.weight_label_12 = Label(window, text="Weight", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.credit_label_12 = Label(window, text="Credit", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)

        #add or delete a class for 12th Grade
        self.add_class_12 = Button(window, text="Add Class", command=lambda: self.add_class_cumulative_func(year=12), font=(FONT, 20), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.delete_class_12 = Button(window, text="Delete Class", command=lambda: self.delete_class_cumulative_func(year=12), font=(FONT, 20), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)

    def quarterly_button_func(self):
        '''This function changes the screen to the quarterly GPA screen and resets the GPA'''
        global screen
        screen = "quarterly_grades"
        #this resets the GPA, so it doesn't appear at the start of the screen, in addition to being updated from cumulative GPA
        self.unweighted_gpa = ""
        self.weighted_gpa = ""

    def cumulative_button_func(self):
        '''This function changes the screen to the cumulative GPA screen and resets the GPA'''
        global screen
        screen = "cumulative_grades"
        #this resets the GPA, so it doesn't appear at the start of the screen, in addition to being updated from quarterly GPA
        self.unweighted_gpa = ""
        self.weighted_gpa = ""

    def more_8_func(self):
        '''Opens the 8th Grade Screen'''
        global screen
        screen = "more_8"

    def more_9_func(self):
        '''Opens the 9th Grade Screen'''
        global screen
        screen = "more_9"

    def more_10_func(self):
        '''Opens the 10th Grade Screen'''
        global screen
        screen = "more_10"

    def more_11_func(self):
        '''Opens the 11th Grade Screen'''
        global screen
        screen = "more_11"

    def more_12_func(self):
        '''Opens the 12th Grade Screen'''
        global screen
        screen = "more_12"

    def change_scale_func(self):
        '''This function switches the GPA scale (100.0 and 4.0) to the other scale, changes the AP and Honors Scale, and changes the text displaying the scale'''
        if self.gpa_scale == 100.0:
            self.gpa_scale = 4.0 #changes scale
            self.honors_scale = self.honors_scale_4 #changes weight for Honors and AP Classes
            self.AP_scale = self.AP_scale_4
        elif self.gpa_scale == 4.0:
            self.gpa_scale = 100.0 #changes scale
            self.honors_scale = self.honors_scale_100 #changes weight for honors and AP Classes
            self.AP_scale = self.AP_scale_100
        self.current_scale.config(text=self.gpa_scale) #changes the text that displays the current scale

    def choose_scale_100_func(self):
        '''This sets the GPA scale to 100.0 when the 100.0 button is pressed'''
        self.gpa_scale = 100

    def choose_scale_4_func(self):
        '''This sets the GPA to 4.0 when the 4.0 button is pressed'''
        self.gpa_scale = 4

    def add_new_class_quarterly_func(self):
        '''This function adds a new row of entry boxes (a new class for the user) when they press the add new class button on the quarterly GPA screen'''
        if len(self.class_data_quarterly) < 11: #A user can not have more than 11 classes to prevent widgets from overlapping, and this would not happen in a quarter
            #creates entry for class name, grade, and credit (usually how much they met)
            class_entry = Entry(window, width=15, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, insertbackground=TEXTCOLOR)
            grade_entry = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, insertbackground=TEXTCOLOR)
            credit_entry = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, insertbackground=TEXTCOLOR)

            #creates an option menu for  the weight of a class
            var = StringVar(window)
            weight_menu = OptionMenu(window, var, "R", "H", "AP")
            weight_menu.config(bg=BACKGROUND_COLOR, fg=TEXTCOLOR, highlightthickness=0, activebackground=BACKGROUND_COLOR,
                               activeforeground=TEXTCOLOR, width=5, font=(FONT, 10))


            #this appends the information about the class to class_data_quarterly
            #no x_location_change as that will occur when the widget is placed
            #first index is the widget, second is the x position, third is the y position
            self.class_data_quarterly.append([[class_entry, 100, self.y_var_quarterly],
                                              [grade_entry, 254, self.y_var_quarterly],
                                              [weight_menu, 308, self.y_var_quarterly],
                                              [credit_entry, 382, self.y_var_quarterly],
                                              ])

            # this makes the row of entry boxes move down every time the user adds a new class
            self.y_var_quarterly += 26 #26 is the height of the widgets

    def delete_class_quarterly_func(self):
        """This deletes the most recent class when called on the quarterly screen"""
        if len(self.class_data_quarterly) >= 1:  # confirms there is at least one class
            for widget in self.class_data_quarterly[-1]: #more recent class added
                widget[0].place_forget()  # this loop removes the widgets for the deleted class from the window. The widget is at index 0
            self.class_data_quarterly.pop()  # this removes the user's class from class_data_quarterly
            self.y_var_quarterly -= 26  # this confirms that the next class added is below the previous class

    def add_class_cumulative_func(self, year): #takes a parameter, which is the year
        '''This class adds a new class on the cumulative_gpa screen'''
        year_classes = [Class for Class in self.class_data_cumulative if Class[5] == year] #a class will be appended if it's from the year on screen
        if len(year_classes) < 17: #confirms there are less than 17 classes to prevent widgets from overlapping
            #makes the entries for the user to enter the class name, grade, and course credit
            class_entry = Entry(window, width=15, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, insertbackground=TEXTCOLOR)
            grade_entry = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, insertbackground=TEXTCOLOR)
            credit_entry = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, insertbackground=TEXTCOLOR)

            #creates an option menu for the weight of a class
            var = StringVar(window)
            weight_menu = OptionMenu(window, var, "R", "H", "AP")
            weight_menu.config(bg=BACKGROUND_COLOR, fg=TEXTCOLOR, highlightthickness=0,
                               activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR, width=5, font=(FONT, 10))
            #this button opens the place where the user inputs information about each term for a class
            more_info = Button(window, text="More", command= lambda: self.more_info_func(Class=class_entry.get()), font=(FONT, 10),
                               bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)

            #these will be used to place the widgets
            x_var_cumulative = 100
            y_var_cumulative = 0

            #these if statements make sure the y_position of the widgets are in the right place
            if year == 8:
                self.year_8_classes_y_var += 26 #adds 26 (height of entries) to the variable
                y_var_cumulative = self.year_8_classes_y_var #assigns the local y variable to the y variable for the year
            elif year == 9:
                self.year_9_classes_y_var += 26 #adds 26 (height of entries) to the variable
                y_var_cumulative = self.year_9_classes_y_var #assigns the local y variable to the y variable for the year
            elif year == 10:
                self.year_10_classes_y_var += 26 #adds 26 (height of entries) to the variable
                y_var_cumulative = self.year_10_classes_y_var #assigns the local y variable to the y variable for the year
            elif year == 11:
                self.year_11_classes_y_var += 26 #adds 26 (height of entries) to the variable
                y_var_cumulative = self.year_11_classes_y_var #assigns the local y variable to the y variable for the year
            elif year == 12:
                self.year_12_classes_y_var += 26 #adds 26 (height of entries) to the variable
                y_var_cumulative = self.year_12_classes_y_var #assigns the local y variable to the y variable for the year

            #this appends all the information to class_data_cumulative. It appends a list of tuples, including the location widget, widget x position, and widget y position
            #it also appends the year of the class and information for the term grade chooser screen, including the default weights. The string is the grade for that term
            self.class_data_cumulative.append([(class_entry, x_var_cumulative, y_var_cumulative),
                                    (grade_entry, x_var_cumulative + 154, y_var_cumulative),
                                   (weight_menu, x_var_cumulative + 208, y_var_cumulative),
                                    (credit_entry, x_var_cumulative + 282, y_var_cumulative),
                                   (more_info, x_var_cumulative + 336, y_var_cumulative),
                                    year, ["", str(self.default_Q1)], ["", str(self.default_Q2)], ["", str(self.default_E2)], ["", str(self.default_Q3)], ["", str(self.default_Q4)], ["", str(self.default_E4)], ""])
            #this appends all the information into for_export to be put into a file after the program ends. It appends a list that will contain the information of each entry boxes and the position of thw widget
            #the "" for more_data will never be filled, it is just there to be consistent
            #it also appends the default term %. The string is the grade for that term
            self.for_export.append([["", x_var_cumulative, y_var_cumulative],
                                               ["", x_var_cumulative + 154, y_var_cumulative],
                                               ["", x_var_cumulative + 208, y_var_cumulative],
                                               ["", x_var_cumulative + 282, y_var_cumulative],
                                               ["", x_var_cumulative + 336, y_var_cumulative],
                                               year, ["", str(self.default_Q1)], ["", str(self.default_Q2)],
                                               ["", str(self.default_E2)], ["", str(self.default_Q3)],
                                               ["", str(self.default_Q4)], ["", str(self.default_E4)], ""])

    def delete_class_cumulative_func(self, year):
        '''This function is responsible for deleting a class'''
        #this gathers all the classes of a certain grade level
        classes_of_year = []
        for Class in self.class_data_cumulative:
            if Class[5] == year: #for each class of the year, append the info into classes_of_year
                classes_of_year.append(Class)
        if classes_of_year: #confirms that there is a class for this year
            if classes_of_year[-1][0][0].get() == "": #If the class name is empty. This is to prevent buggy behavior with for_export, which relies on the name of the class when storing data
                messagebox.showerror("Remove Class Error", "Please enter a name for the class before removing it")
            else:
                self.class_data_cumulative.remove(classes_of_year[-1]) #removes the last class from class_data_cumulative
                for index, Class in enumerate(self.for_export):
                    try: #if the name of the class is the same as the name for this class in self.for_export
                        if classes_of_year[-1][0][0].get() == Class[index][0]:
                            self.for_export.remove(Class) #sometimes this displays buggy behavior
                    except: #error only occurs when the two sides aren't equal
                        pass
                for widget in classes_of_year[-1][0:5]:
                    widget[0].place_forget() #deletes the widgets for this class from the screen
                if year == 8: #these lines ensure that future widgets will be in the correct location
                    self.year_8_classes_y_var -= 26
                elif year == 9:
                    self.year_9_classes_y_var -= 26
                elif year == 10:
                    self.year_10_classes_y_var -= 26
                elif year == 11:
                    self.year_11_classes_y_var -= 26
                elif year == 12:
                    self.year_12_classes_y_var -= 26

    def more_info_func(self, Class):
        '''This function controls the screen where the user can enter information about each term for a class'''
        global screen
        weight = credit = 0
        names_for_all_classes = []
        for _class in self.class_data_cumulative:
            names_for_all_classes.append(_class[0][0].get())
        if Class == "": #the user must enter a name to prevent buggy behavior
            messagebox.showerror("Calc GPA Error", "Please enter in a class name first")
        if names_for_all_classes.count(Class) >= 2: #this is because the name of the class is used to identify the class
            messagebox.showerror("Calc GPA Error", "Class must have a unique name")
        else:
            for users_class in self.class_data_cumulative:
                if users_class[0][0].get() == Class: #this gets the name of the class and matches it with the name in class_data_cumulative
                    weight = users_class[2][0]["text"] #this info is to be displayed on the screen
                    credit = users_class[3][0].get()

                    current_Q1_grade = users_class[6][0] #the current grade for each term in based on info in class_data_cumulative
                    current_Q2_grade = users_class[7][0] #at the start, it's ""
                    current_E2_grade = users_class[8][0]
                    current_Q3_grade = users_class[9][0]
                    current_Q4_grade = users_class[10][0]
                    current_E4_grade = users_class[11][0]

                    current_Q1_weight = users_class[6][1] #the % weight of the term for the user's F4 grade
                    current_Q2_weight = users_class[7][1] #at the start, it's 21.25% for the quarter, 5% for the midterm, and 10% for the final
                    current_E2_weight = users_class[8][1]
                    current_Q3_weight = users_class[9][1]
                    current_Q4_weight = users_class[10][1]
                    current_E4_weight = users_class[11][1]

            if screen == "more_8": #there is a different screen for each year due to the back button, but there are no other differences
                screen = "class_term_grades_chooser_8"
            elif screen == "more_9":
                screen = "class_term_grades_chooser_9"
            elif screen == "more_10":
                screen = "class_term_grades_chooser_10"
            elif screen == "more_11":
                screen = "class_term_grades_chooser_11"
            elif screen == "more_12":
                screen = "class_term_grades_chooser_12"

            #this information will be at the top of the screen
            self.term_grade_class_name = Label(window, text=f"Class Name: {Class}", font=(FONT, 20), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
            self.term_grade_weight = Label(window, text=f"Type: {weight}", font=(FONT, 20), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
            self.term_grade_credit = Label(window, text=f"Credit: {credit}", font=(FONT, 20), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)

            #widgets on top of the entries
            self.terms_text = Label(window, text="Terms", font=(FONT, 20), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
            self.term_grade_label = Label(window, text="Grade", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
            self.term_weight_label = Label(window, text="%", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)

            #These are the labels for each term
            self.Q1 = Label(window, text="Q1:", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
            self.Q2 = Label(window, text="Q2:", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
            self.E2 = Label(window, text="E2:", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
            self.Q3 = Label(window, text="Q3:", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
            self.Q4 = Label(window, text="Q4:", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
            self.E4 = Label(window, text="E4:", font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)

            #this is where the user inputs their grade for each term
            self.Q1_entry = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                  insertbackground=TEXTCOLOR)
            self.Q2_entry = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                  insertbackground=TEXTCOLOR)
            self.E2_entry = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                  insertbackground=TEXTCOLOR)
            self.Q3_entry = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                  insertbackground=TEXTCOLOR)
            self.Q4_entry = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                  insertbackground=TEXTCOLOR)
            self.E4_entry = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                  insertbackground=TEXTCOLOR)

            #this is where the user inputs the weight of each term
            self.Q1_weight = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                   insertbackground=TEXTCOLOR)
            self.Q2_weight = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                   insertbackground=TEXTCOLOR)
            self.E2_weight = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                   insertbackground=TEXTCOLOR)
            self.Q3_weight = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                   insertbackground=TEXTCOLOR)
            self.Q4_weight = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                   insertbackground=TEXTCOLOR)
            self.E4_weight = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                   insertbackground=TEXTCOLOR)

            #this button saves the user's information
            self.save_button = Button(window, text="Save", command= lambda: self.save_button_func(Class=Class), font=(FONT, 20),
                                      bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)

            #these are the locations of each widget on the screen. They are defined here for convenience
            self.term_grade_class_name.place(x=173 + x_location_change, y=20)
            self.term_grade_weight.place(x=263 + x_location_change, y=60)
            self.term_grade_credit.place(x=257 + x_location_change, y=100)

            self.terms_text.place(x=263 + x_location_change, y=150)
            self.term_grade_label.place(x=262 + x_location_change, y=193)
            self.term_weight_label.place(x=331 + x_location_change, y=193)

            #note that the label is at 224, grade entry at 256, and weight entry at 313
            self.Q1.place(x=224 + x_location_change, y=220)
            self.Q1_entry.place(x=256 + x_location_change, y=220)
            self.Q1_weight.place(x=313 + x_location_change, y=220)

            self.Q2.place(x=224 + x_location_change, y=250)
            self.Q2_entry.place(x=256 + x_location_change, y=250)
            self.Q2_weight.place(x=313 + x_location_change, y=250)

            self.E2.place(x=224 + x_location_change, y=280)
            self.E2_entry.place(x=256 + x_location_change, y=280)
            self.E2_weight.place(x=313 + x_location_change, y=280)

            self.Q3.place(x=224 + x_location_change, y=310)
            self.Q3_entry.place(x=256 + x_location_change, y=310)
            self.Q3_weight.place(x=313 + x_location_change, y=310)

            self.Q4.place(x=224 + x_location_change, y=340)
            self.Q4_entry.place(x=256 + x_location_change, y=340)
            self.Q4_weight.place(x=313 + x_location_change, y=340)

            self.E4.place(x=224 + x_location_change, y=370)
            self.E4_entry.place(x=256 + x_location_change, y=370)
            self.E4_weight.place(x=313 + x_location_change, y=370)

            self.save_button.place(x=263 + x_location_change, y=400)

            #this puts the current grade for a term in the entry box. These will always be defined as they are created with the class
            self.Q1_entry.insert(0, current_Q1_grade)
            self.Q2_entry.insert(0, current_Q2_grade)
            self.E2_entry.insert(0, current_E2_grade)
            self.Q3_entry.insert(0, current_Q3_grade)
            self.Q4_entry.insert(0, current_Q4_grade)
            self.E4_entry.insert(0, current_E4_grade)

            #this puts the current weight for a term in the entry box
            self.Q1_weight.insert(0, current_Q1_weight)
            self.Q2_weight.insert(0, current_Q2_weight)
            self.E2_weight.insert(0, current_E2_weight)
            self.Q3_weight.insert(0, current_Q3_weight)
            self.Q4_weight.insert(0, current_Q4_weight)
            self.E4_weight.insert(0, current_E4_weight)

            #this allows certain labels on this screen to have text appear when they are hovered over
            for label in [self.term_grade_label, self.term_weight_label,
                          self.Q1, self.Q2, self.E2, self.Q3, self.Q4, self.E4]:
                label.bind("<Enter>", start_hover)
                label.bind("<Leave>", end_hover)

            #this appends all the widgets to a list to make it easy to place them later on
            self.term_info_widgets.append(
                [self.term_grade_class_name, self.term_grade_weight, self.term_grade_credit, self.terms_text,
                 self.term_grade_label, self.term_weight_label, self.Q1, self.Q1_entry,
                 self.Q1_weight, self.Q2, self.Q2_entry, self.Q2_weight, self.E2,
                 self.E2_entry, self.E2_weight, self.Q3, self.Q3_entry,
                 self.Q3_weight, self.Q4, self.Q4_entry, self.Q4_weight,
                 self.E4, self.E4_entry, self.E4_weight, self.save_button])

    def save_button_func(self, Class):
        '''This function saves the data for the term grades for a class'''
        #this lists makes a list of lists with the user's data
        entries = [self.Q1_entry.get(), self.Q2_entry.get(), self.E2_entry.get(), self.Q3_entry.get(), self.Q4_entry.get(), self.E4_entry.get()]
        weights = [self.Q1_weight.get(), self.Q2_weight.get(), self.E2_weight.get(), self.Q3_weight.get(), self.Q4_weight.get(), self.E4_weight.get()]
        entry_weight = list(zip(entries, weights))
        for term in entry_weight: #each term
            if term[0] != "" and term[1] == "":
                #if there is a grade but not a weight, there will be an error
                messagebox.showerror("Making Class Error", "Please have a % for each term that has a grade")
                break
            try:
                if term[0] != "" and term[1] != "":
                    float(term[0])
                    float(term[1])
            except ValueError:
                # if they are not empty but they are not float, an error will be raised
                messagebox.showerror("Making Class Error", "Terms and percents must be numbers, with no % sign")
                break
        else:
            for users_class in self.class_data_cumulative:
                if users_class[0][0].get() == Class: #if the name of the class is the class that we are currently choosing term grades for
                    users_class[6] = entry_weight[0] #sets the data for class_data_cumulative to the data that the user inputted on this screen
                    users_class[7] = entry_weight[1]
                    users_class[8] = entry_weight[2]
                    users_class[9] = entry_weight[3]
                    users_class[10] = entry_weight[4]
                    users_class[11] = entry_weight[5]
            for users_class in self.for_export:
                if users_class[0][0] == Class: #if the name of the class is the class that we are currently choosing term grades for
                    users_class[6] = entry_weight[0] #sets the data for class_data_cumulative to the data that the user inputted on this screen
                    users_class[7] = entry_weight[1]
                    users_class[8] = entry_weight[2]
                    users_class[9] = entry_weight[3]
                    users_class[10] = entry_weight[4]
                    users_class[11] = entry_weight[5]

            grades = [] #these will be used for determining the user's grade
            weights = []
            for term in entry_weight:
                if term[0] != "": #if not empty, makes sure the weight of the term also isn't factored in
                    grades.append(float(term[0]) * float(term[1]))
                    weights.append(float(term[1]))
            try:
                for users_class in self.class_data_cumulative:
                    if users_class[0][0].get() == Class: #if this is the correct class
                        users_class[12] = str(sum(grades) / sum(weights)) #a precise grade for the class, won't be rounded when calculating GPA
                        messagebox.showinfo("Making Class", "Class saved successfully")
                for users_class in self.for_export:
                    if users_class[0][0] == Class: #appends the grade to for_export
                        users_class[12] = str(sum(grades) / sum(weights))
            except ZeroDivisionError: #there are no terms
                messagebox.showerror("Making Class Error", "Please enter the grade for at least one term. If you only want the F4 grade, make the weight of one of the terms 100 and all the others 0, and enter the grade there")

    def get_class_data(self):
        '''This function takes the users inputs and stores them in data2'''
        global first_frame_previous_data_classes
        self.data2.clear() #data2 is cleared every frame to prevent unintended duplicates
        for Class in previous_data_classes:
            if first_frame_previous_data_classes: #this will occur only early in the program, when there's no data in the entries
                #note that class is previous_data_classes[index]
                new_class = []
                new_class.append(Class[0][0]) #appends class name
                if Class[12]: #if a precise grade from terms
                    new_class.append(Class[12])
                else:
                    new_class.append(Class[1][0]) #regular grade
                if Class[2][0]: #weight of the class
                    new_class.append(Class[2][0])
                else: #if not entered, don't do anything
                    new_class.append("")
                new_class.append(Class[3][0]) #credit for class
                new_class.append(Class[5]) #year of class
                self.data2.append(new_class) #appends it to data2
                first_frame_previous_data_classes = False
        if screen != "quarterly_grades": #prevents data for quarterly grades entering when on cumulative screen
            #if dealing with cumulative grades over quarter grades
            for index, Class in enumerate(self.class_data_cumulative): #this loop puts data about each class into data2
                new_class = [] #a list is made for each class in class_data
                new_class.append(Class[0][0].get()) #name of class
                self.for_export[index][0][0] = Class[0][0].get() #puts name in for_export
                if Class[12]: #if grade from terms
                    new_class.append(Class[12])
                    self.for_export[index][1][0] = Class[12] #puts grade in for_export
                else:
                    new_class.append(Class[1][0].get()) #grade user recieved without terms
                    self.for_export[index][1][0] = Class[1][0].get()
                if Class[2][0]["text"] == "R": #if regular course
                    new_class.append(1)
                    self.for_export[index][2][0] = 1
                elif Class[2][0]["text"] == "H": #if honors course
                    new_class.append(self.honors_scale)
                    self.for_export[index][2][0] = self.honors_scale
                elif Class[2][0]["text"] == "AP": #if regents course
                    new_class.append(self.AP_scale)
                    self.for_export[index][2][0] = self.AP_scale
                else:
                    new_class.append("") #if blank
                new_class.append(Class[3][0].get()) #credit for class (usually based on how often it met)
                self.for_export[index][3][0] = Class[3][0].get()
                new_class.append(Class[5]) #grade level the class was taken in (8-12)
                self.for_export[index][5] = Class[5]
                self.data2.append(new_class) #appends the temporary new_class list, which contains all the above information, into the data2 list
        if screen == "quarterly_grades": #dealing with quarterly GPA
            for index, Class in enumerate(self.class_data_quarterly): #quarterly GPA
                new_class = []
                new_class.append(Class[0][0].get()) #name of class
                new_class.append(Class[1][0].get()) #grade user recieved
                if Class[2][0]["text"] == "R": #regular course
                    new_class.append(1)
                elif Class[2][0]["text"] == "H": #honors course
                    new_class.append(self.honors_scale)
                elif Class[2][0]["text"] == "AP": #AP course
                    new_class.append(self.AP_scale)
                else:
                    new_class.append("") #nothing for weight
                new_class.append(Class[3][0].get()) #credit for class (usually based on how often it met)
                self.data2.append(new_class) #appends the temporary new_class list, which contains all the above information, into the data2 list

    def whats_my_gpa_func(self):
        '''This function calculates the user's GPA when Calculate my GPA is pressed on the GPA page'''
        global gpa_calculated #for exporting data
        can_calculate = False #to see if there are classes on the screen
        if self.class_data_quarterly and screen == "quarterly_grades":
            can_calculate = True #classes for quarterly screen
        elif self.class_data_cumulative and screen != "quarterly_grades":
            can_calculate = True #classes for cumulative screen
        if can_calculate:
            if self.gpa_scale == 100:
                try:
                    #unweighted_total_grade_list makes a list of every grade the user has (stored in self.data2), multipled by the amount of credit for the class.
                    unweighted_total_grade_list_100 = list(map(lambda Class: float(Class[1]) * float(Class[3]), self.data2))
                    #weighted is similar but also includes the weight of the class
                    weighted_total_grade_list_100 = list(map(lambda Class: float(Class[1]) * float(Class[2]) * float(Class[3]), self.data2))
                    #this is a list of the total points available in every class (100) * the credit for the class
                    total_points_available_list_100 = list(map(lambda Class: 100 * float(Class[3]), self.data2))
                    #this replaces the already defines weighted and unweighted GPA widgets. It adds up the elements in the respective lists and divides it by the total points.
                    #the GPA is rounded to 4 decmial places, with zeroes shown.
                    self.unweighted_gpa = "{:.4f}".format(sum(unweighted_total_grade_list_100) / sum(total_points_available_list_100) * 100)
                    self.weighted_gpa = "{:.4f}".format(sum(weighted_total_grade_list_100) / sum(total_points_available_list_100) * 100)
                    gpa_calculated = True #this is for exporting data
                except ValueError:
                    for Class in self.data2:
                        if Class[1] in self.grades_4:
                            #if the user entered a letter grade for 100.0 scale
                            messagebox.showerror("Calc GPA Error", "100.0 Scale does not support letter grades")
                            return "error"
                    else: #if the user did not fill out all the required fields, an error message will appear
                        messagebox.showerror("Calc GPA Error", "Please fill out all fields correctly. In addition, if you are loading your data in, please check each year before calculating your GPA.")
                        return "error"
                except ZeroDivisionError: #if weight or credit is zero
                    messagebox.showerror("Calc GPA Error", "Weight and Credit can not be zero")
                    return "error"
            elif self.gpa_scale == 4:
                try:
                    unweighted_total_grade_list_4 = []
                    weighted_total_grade_list_4 = []
                    total_points_available_list_4 = []
                    for Class in self.data2:
                        if Class[1] in self.grades_4: #if it is a letter grade, Class[1] is the grade
                            #this appends the grade the user recieved from 0.0-4.0, converted from a letter grade
                            unweighted_total_grade_list_4.append(self.grades_4[Class[1]] * float(Class[3]))
                            #weighted grade includes weight
                            weighted_total_grade_list_4.append(self.grades_4[Class[1]] * float(Class[3]) * float(Class[2]))
                            #the total points available is 4 times the credit for the course
                            total_points_available_list_4.append(float(4) * float(Class[3]))
                        elif float(Class[1]) or float(Class[1]) == 0.0: #float didn't work with 0
                            #this is if a numeral grade was inputted
                            for key, value in self.grade_ranges_4.items():
                                if round(float(Class[1])) in value: #the grade matches this grade range
                                    #appends the value for the key (key is a range of grades, such as 93-96, value is from 0.0-4.0)
                                    unweighted_total_grade_list_4.append(float(self.grades_4[key]) * float(Class[3]))
                                    #for weighted GPA
                                    weighted_total_grade_list_4.append(float(self.grades_4[key]) * float(Class[3]) * float(Class[2]))
                                    #credit * 4 is total available
                                    total_points_available_list_4.append(float(4) * float(Class[3]))
                    #this replaces the already defines weighted and unweighted GPA widgets. It adds up the elements in the respective lists and divides it by the total points.
                    #the GPA is rounded to 1 decimal place, with zeroes shown.
                    self.unweighted_gpa = "{:.1f}".format(sum(unweighted_total_grade_list_4) / sum(total_points_available_list_4) * 4)
                    self.weighted_gpa = "{:.1f}".format(sum(weighted_total_grade_list_4) / sum(total_points_available_list_4) * 4)
                    gpa_calculated = True #for exporting data
                except ValueError: #if a field is empty (besides class name)
                    messagebox.showerror("Calc GPA Error", "Please fill out all fields correctly. In addition, if you are loading your data in, please check each year before calculating your GPA.")
                    return "error"
                except ZeroDivisionError: #if weight or credit is zero
                    messagebox.showerror("Calc GPA Error", "Weight and Credit can not be zero")
                    return "error"

            #this updates the labels for the GPA
            self.unweighted_gpa_label.config(text=f"Unweighted GPA: {self.unweighted_gpa}")
            self.weighted_gpa_label.config(text=f"Weighted GPA: {self.weighted_gpa}")
        else: #must be at least one class
            messagebox.showerror("Calc GPA Error", "Please enter at least one class")
            return "error"

class HelpMenu:
    """The HelpMenu class controls the elements pressed after the user presses Help on the home screen"""
    def __init__(self):
        '''This function creates the buttons and label on the help menu home screen'''
        #widgets for help menu home screen
        self.instructions = Button(window, text="Instructions", command=self.instructions_func, font=(FONT, 30),
                                  bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.settings = Button(window, text="Settings", command=self.settings_func, font=(FONT, 30),
                                  bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.help_menu_label = Label(window, text="Help Menu", font=(FONT, 30), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)

        #widgets for instructions page 1
        self.instructions_top = Label(window, text="Instructions",
                                        font=(FONT, 30), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.intro_instructions = Label(window, text="This calculator allows students of Monroe-Woodbury High School \n to calculate their quarterly and cumulative GPA.",
                                        font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.quarterly_GPA_instructions = Label(window, text="For a simple, quarterly GPA, click Calculate My GPA, and then click Quarterly \n Fill in all the instructions, adding classes as you need to, and then hit calculate my GPA \n Because this is meant to be a simple experience, data for quarterly GPA is not stored.",
                                        font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.cumulative_GPA_instructions = Label(window, text="For a more comprehensive GPA, hit Annual/Cumulative. \n Here, you can receive your cumulative GPA for all the classes you took in High School \n If you in the middle of a year, update the credit for each class \n For example, if 3 quarters have passed, full year courses get .75 credit \n Data is stored and can be loaded in on the Data Information page",
                                        font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.QA_top = Label(window, text="Questions and Answers",
                                        font=(FONT, 30), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.Q1 = Label(window, text="Question: What is GPA and how is it calculated? "
                                     "\n\nAnswer: GPA is the grade point average for all the classes for a given period. \nIt is calculated based on the grade the student received, \nthe credit (usually proportional to length) of the course, and for weighted GPA, weight",
                                    font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, justify="left")
        self.Q2 = Label(window, text="Question: What is the difference between weighted and unweighted GPA? \n\nAnswer: Unweighted GPA doesn't give extra weight for Honors and AP classes\nWeighted GPA accounts for Honors and AP classes and gives extra weight to them\nWeighted GPA is more common at Monroe-Woodbury",
                                        font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, justify="left")

        #widgets for instructions page 2
        self.next_page = Button(window, text="Next Page", command=self.change_page_func, font=(FONT, 20),
                                  bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.Q3 = Label(window, text="Question: What is the difference between weighted and unweighted GPA?"
                                    "\n\nAnswer: Regular classes get 1.0 weight, Honors classes get 1.03 (1.125 on 4.0 scale), \nand AP classes get 1.05 (1.25 on 4.0 scale). \nThis is done automatically and get be adjusted in the settings"
                                    "\nFor specific classes - "
                                    "\n            Pre-AP World History gets Honors credit"
                                    "\n            Dual Enrollment (college) classes that are not AP classes get regular credit",
                                    font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, justify="left")
        self.Q4 = Label(window, text="Question: What is the difference between 100.0 and 4.0 GPA? \n\nAnswer: Monroe-Woodbury uses 100.0 GPA, but many other schools use 4.0 GPA\nBoth are provided so M-W students can easily compare GPAs to students at other schools.",
                         font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, justify="left")
        self.Q5 = Label(window, text="Question: What 8th-grade classes count for High School GPA? \nAnswer: Only enter in Algebra I, Biology, and World Language for 8th Grade",
                         font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, justify="left")
        self.Q6 = Label(window, text="Question: Where can I access the grades for classes I took in previous years? \nAnswer: Click Grade History in PowerSchool and click Grade History",
                         font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, justify="left")
        self.Q7 = Label(window, text="Question: How can I report a bug for this program? \nAnswer: All bugs can be reported to prasadsaha11@gmail.com",
                         font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, justify="left")
        self.previous_page = Button(window, text="Previous Page", command=self.change_page_func, font=(FONT, 20),
                                bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)

        #widgets for the settings screen
        self.settings_top = Label(window, text="Settings",
                                        font=(FONT, 30), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)

        #Label to change the weights of harder classes
        self.change_honors_weight_100_label = Label(window, text="Honors Weight (100.0):",
                                        font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.change_AP_weight_100_label = Label(window, text="AP Weight (100.0)",
                                              font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.change_honors_weight_4_label = Label(window, text="Honors Weight (4.0):",
                                              font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.change_AP_weight_4_label = Label(window, text="AP Weight (4.0):",
                                              font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)

        #the entries to change the weights of harder classes
        self.change_honors_weight_100_entry = Entry(window, width=5, font=(FONT, 15),
                                              bg=BACKGROUND_COLOR, fg=TEXTCOLOR, insertbackground=TEXTCOLOR)
        self.change_AP_weight_100_entry = Entry(window, width=5, font=(FONT, 15),
                                              bg=BACKGROUND_COLOR, fg=TEXTCOLOR, insertbackground=TEXTCOLOR)
        self.change_honors_weight_4_entry = Entry(window, width=5, font=(FONT, 15),
                                              bg=BACKGROUND_COLOR, fg=TEXTCOLOR, insertbackground=TEXTCOLOR)
        self.change_AP_weight_4_entry = Entry(window, width=5, font=(FONT, 15),
                                              bg=BACKGROUND_COLOR, fg=TEXTCOLOR, insertbackground=TEXTCOLOR)

        #the labels to change the weight of each term in term grades chooser
        self.change_Q1_weight_label = Label(window, text="Quarter 1 Weight:",
                                        font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.change_Q2_weight_label = Label(window, text="Quarter 2 Weight:",
                                            font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.change_E2_weight_label = Label(window, text="Midterm Weight:",
                                            font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.change_Q3_weight_label = Label(window, text="Quarter 3 Weight:",
                                            font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.change_Q4_weight_label = Label(window, text="Quarter 4 Weight:",
                                            font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.change_E4_weight_label = Label(window, text="Final Exam Weight:",
                                            font=(FONT, 12), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)

        #the entries to change the weight of each term
        self.change_Q1_weight_entry = Entry(window, width=5, font=(FONT, 15),
                                      bg=BACKGROUND_COLOR, fg=TEXTCOLOR, insertbackground=TEXTCOLOR)
        self.change_Q2_weight_entry = Entry(window, width=5, font=(FONT, 15),
                                      bg=BACKGROUND_COLOR, fg=TEXTCOLOR, insertbackground=TEXTCOLOR)
        self.change_E2_weight_entry = Entry(window, width=5, font=(FONT, 15),
                                      bg=BACKGROUND_COLOR, fg=TEXTCOLOR, insertbackground=TEXTCOLOR)
        self.change_Q3_weight_entry = Entry(window, width=5, font=(FONT, 15),
                                      bg=BACKGROUND_COLOR, fg=TEXTCOLOR, insertbackground=TEXTCOLOR)
        self.change_Q4_weight_entry = Entry(window, width=5, font=(FONT, 15),
                                      bg=BACKGROUND_COLOR, fg=TEXTCOLOR, insertbackground=TEXTCOLOR)
        self.change_E4_weight_entry = Entry(window, width=5, font=(FONT, 15),
                                      bg=BACKGROUND_COLOR, fg=TEXTCOLOR, insertbackground=TEXTCOLOR)

        self.confirm_settings_button = Button(window, text="Confirm New Settings", command=self.confirm_settings_button_func, font=(FONT, 15),
                                              bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)

    def instructions_func(self):
        '''This function changes the screen to the instructions screen'''
        global screen
        screen = "instructions_1"

    def settings_func(self):
        '''This function changes the screen to the settings screen'''
        global screen
        screen = "settings"

    def change_page_func(self):
        """This function goes to the other page of the instructions menu"""
        global screen
        if screen == "instructions_1":
            screen = "instructions_2"
        elif screen == "instructions_2":
            screen = "instructions_1"

    def confirm_settings_button_func(self):
        '''This function updates the weights of Honors and AP Classes based on the new settings'''
        try:
            #this updates the weight of honors and AP classes
            gpa_calculator.honors_scale_100 = float(help_menu.change_honors_weight_100_entry.get())
            gpa_calculator.AP_scale_100 = float(help_menu.change_AP_weight_100_entry.get())
            gpa_calculator.honors_scale_4 = float(help_menu.change_honors_weight_4_entry.get())
            gpa_calculator.AP_scale_4 = float(help_menu.change_AP_weight_4_entry.get())

            #this updates the weight of each term
            gpa_calculator.default_Q1 = float(help_menu.change_Q1_weight_entry.get())
            gpa_calculator.default_Q2 = float(help_menu.change_Q2_weight_entry.get())
            gpa_calculator.default_E2 = float(help_menu.change_E2_weight_entry.get())
            gpa_calculator.default_Q3 = float(help_menu.change_Q3_weight_entry.get())
            gpa_calculator.default_Q4 = float(help_menu.change_Q4_weight_entry.get())
            gpa_calculator.default_E4 = float(help_menu.change_E4_weight_entry.get())

            #gpa_calculator.honors_scale and AP_scale is for 4.0 vs 100, but it also must be updated here
            if gpa_calculator.gpa_scale == 100.0:
                gpa_calculator.honors_scale = gpa_calculator.honors_scale_100
                gpa_calculator.AP_scale = gpa_calculator.AP_scale_100
            elif gpa_calculator.gpa_scale == 4.0:
                gpa_calculator.honors_scale = gpa_calculator.honors_scale_4
                gpa_calculator.AP_scale = gpa_calculator.AP_scale_4

            messagebox.showinfo("Changed Settings", "Settings changed successfully")
        except ValueError: #if there is something that isn't float
            messagebox.showerror("Change Settings Error", "Please enter numbers for all fields")

class LoadingData:
    """This class controls the elements for the loading data screen"""
    def __init__(self):
        '''This function defines the widgets for this class'''
        self.data_info_top = Label(window, text="Data Information",
                              font=(FONT, 30), bg=BACKGROUND_COLOR, fg=TEXTCOLOR)
        self.load_data_button = Button(window, text="Load Data", command=self.load_data_func, font=(FONT, 30),
                                  bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.delete_data_button = Button(window, text="Delete Data", command=self.delete_data_func, font=(FONT, 30),
                                  bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)
        self.save_data_button = Button(window, text="Save Data as PDF", command=self.save_data_func, font=(FONT, 30),
                                  bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR)

    def load_data_func(self):
        global previous_data_all, previous_data_classes, data_loaded
        if os.path.getsize("data_for_calc_gpa.txt") and not data_loaded: #if the file isn't empty and hasn't been loaded in yet
            previous_data_all.append(file_read.read()) #this appends the file contents to a list

            try: #this can be any type of wrong data, such as NameError. This would likely happen if the user directly edited the filed
                previous_data_all = eval(previous_data_all[0]) #if data is invalid, it won't be imported
                data_loaded = True #makes sure the data can only be imported once

                #these two lines save whether the GPA scale was 100.0 or 4.0
                gpa_calculator.gpa_scale = previous_data_all[-1][0]
                gpa_calculator.current_scale.config(text=gpa_calculator.gpa_scale)

                #these are the weights of Honors and AP classes
                gpa_calculator.honors_scale_100 = previous_data_all[-1][1]
                gpa_calculator.AP_scale_100 = previous_data_all[-1][2]
                gpa_calculator.honors_scale_4 = previous_data_all[-1][3]
                gpa_calculator.AP_scale_4 = previous_data_all[-1][4]

                if gpa_calculator.gpa_scale == 4.0: #this makes sure the current scale is updated
                    gpa_calculator.honors_scale = gpa_calculator.honors_scale_4
                    gpa_calculator.AP_scale = gpa_calculator.AP_scale_4

                #this makes sure widgets are placed in the correct location
                gpa_calculator.year_8_classes_y_var = previous_data_all[-1][5]
                gpa_calculator.year_9_classes_y_var = previous_data_all[-1][6]
                gpa_calculator.year_10_classes_y_var = previous_data_all[-1][7]
                gpa_calculator.year_11_classes_y_var = previous_data_all[-1][8]
                gpa_calculator.year_12_classes_y_var = previous_data_all[-1][9]

                #these are the weights of each term for the term choose
                gpa_calculator.default_Q1 = previous_data_all[-1][10]
                gpa_calculator.default_Q2 = previous_data_all[-1][11]
                gpa_calculator.default_E2 = previous_data_all[-1][12]
                gpa_calculator.default_Q3 = previous_data_all[-1][13]
                gpa_calculator.default_Q4 = previous_data_all[-1][14]
                gpa_calculator.default_E4 = previous_data_all[-1][15]

                #this is previous data for the classes, which is everything but the last list
                previous_data_classes = previous_data_all[:-1]

                for index, Class in enumerate(previous_data_classes):
                    #these are the widgets that will go into cumulative class data for previous class
                    small_class_entry = Entry(window, width=15, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                              insertbackground=TEXTCOLOR)
                    grade_entry = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                        insertbackground=TEXTCOLOR)
                    var = StringVar(window)
                    weight_menu = OptionMenu(window, var, "R", "H", "AP")
                    weight_menu.config(bg=BACKGROUND_COLOR, fg=TEXTCOLOR, highlightthickness=0,
                                       activebackground=BACKGROUND_COLOR, activeforeground=TEXTCOLOR, width=5,
                                       font=(FONT, 10))
                    credit_entry = Entry(window, width=5, font=(FONT, 15), bg=BACKGROUND_COLOR, fg=TEXTCOLOR,
                                         insertbackground=TEXTCOLOR)
                    more_info = Button(window, text="More", command=lambda: gpa_calculator.more_info_func(Class=small_class_entry.get()),
                                       font=(FONT, 10), bg=BACKGROUND_COLOR, fg=TEXTCOLOR, activebackground=BACKGROUND_COLOR,
                                       activeforeground=TEXTCOLOR)

                    #this appends all the previous data into class_data_cumulative, including the location of widgets and settings information
                    gpa_calculator.class_data_cumulative.append([(small_class_entry, previous_data_classes[index][0][1], previous_data_classes[index][0][2]),
                                                       (grade_entry, previous_data_classes[index][1][1], previous_data_classes[index][1][2]),
                                                     (weight_menu, previous_data_classes[index][2][1], previous_data_classes[index][2][2]),
                                                       (credit_entry, previous_data_classes[index][3][1], previous_data_classes[index][3][2]),
                                                       (more_info, previous_data_classes[index][4][1], previous_data_classes[index][4][2]),
                                                       previous_data_classes[index][5], [previous_data_classes[index][6][0], previous_data_classes[index][6][1]], [previous_data_classes[index][7][0], previous_data_classes[index][7][1]],
                                                       [previous_data_classes[index][8][0], previous_data_classes[index][8][1]], [previous_data_classes[index][9][0], previous_data_classes[index][9][1]],
                                                       [previous_data_classes[index][10][0], previous_data_classes[index][10][1]], [previous_data_classes[index][11][0], previous_data_classes[index][11][1]], previous_data_classes[index][12]])
                    #this appends all the previous data into for_export to saved into the file again
                    gpa_calculator.for_export.append([[previous_data_classes[index][0][0], previous_data_classes[index][0][1], previous_data_classes[index][0][2]],
                                                       [previous_data_classes[index][1][0], previous_data_classes[index][1][1], previous_data_classes[index][1][2]],
                                                     [previous_data_classes[index][2][0], previous_data_classes[index][2][1], previous_data_classes[index][2][2]],
                                                       [previous_data_classes[index][3][0], previous_data_classes[index][3][1], previous_data_classes[index][3][2]],
                                                       ["", previous_data_classes[index][4][1], previous_data_classes[index][4][2]],
                                                       previous_data_classes[index][5], [previous_data_classes[index][6][0], previous_data_classes[index][6][1]], [previous_data_classes[index][7][0], previous_data_classes[index][7][1]],
                                                       [previous_data_classes[index][8][0], previous_data_classes[index][8][1]], [previous_data_classes[index][9][0], previous_data_classes[index][9][1]],
                                                       [previous_data_classes[index][10][0], previous_data_classes[index][10][1]], [previous_data_classes[index][11][0], previous_data_classes[index][11][1]], ""])
                messagebox.showinfo("Loading in Data", "Data loaded in successfully")
                file_append.truncate(0)  # clears the file
            except:
                messagebox.showerror("Load Data Error", "Data was invalid and could not be loaded in")
                file_append.truncate(0) #clears the file
        else:
            if data_loaded: #data already loaded in
                messagebox.showerror("Load Data Error", "Data already loaded in")
            else: #there is no data
                messagebox.showerror("Load Data Error", "No data to load in")

    def delete_data_func(self):
        '''This function deletes the data from the file (but not from anywhere else)'''
        answer = messagebox.askyesno("Delete Saved Data", "Are you sure you would like to delete saved data?")
        if not answer:
            pass
        if answer:
            file_append.truncate(0) #clear file
            messagebox.showinfo("Data Deleted", "Saved data has been deleted. This action did not delete any data within the program. To achieve that, reopen the program and do not load your data.")

    def save_data_func(self):
        '''For now, this function has not been finished'''
        if not gpa_calculated: #GPA must have been calculated to prevent an error
            messagebox.showerror("Export GPA Error", "Please hit calculate GPA once on the cumulative screen before exporting your data")
        else: #check for errors
            error_in_GPA_calculation = gpa_calculator.whats_my_gpa_func() #if a return statement was triggered
            if error_in_GPA_calculation != "error": #the GPA was calculated sucessfully
                answer = messagebox.askyesno("Export GPA", "This will open a PDF on a new screen. Are you sure you want to continue?")
                if not answer: #if they say no, do nothing
                    pass
                else:
                    #user's name
                    users_name = simpledialog.askstring("Name", "Please enter your name:")
                    y_coord = 750 #starting y_coordinate
                    file = "GPA.pdf" #name of PDF
                    c = canvas.Canvas(file, pagesize=letter) #canvas to draw on

                    current_date = datetime.date.today() #the date
                    formatted_date = current_date.strftime("%B %d, %Y")

                    #information for the top
                    c.drawString(150, y_coord, "Monroe-Woodbury High School Grade Report")
                    y_coord -= 20 #the y coordinate decreases to make sure information doesn't overlap
                    c.drawString(250, y_coord, users_name)
                    y_coord -= 20
                    c.drawString(225, y_coord, formatted_date)
                    y_coord -= 20

                    #information about class data
                    c.drawString(100, y_coord, "Class")
                    c.drawString(200, y_coord, "Grade")
                    c.drawString(250, y_coord, "Weight")
                    c.drawString(300, y_coord, "Credit")
                    c.drawString(350, y_coord, "Year")

                    y_coord -= 20

                    for Class in gpa_calculator.class_data_cumulative:
                        x_coord = 100 #x position
                        for index, widget in enumerate(Class[0:6]): #up to year of the class
                            if index != 4: #index 4 is the more info button
                                if index == 0: #class name
                                    c.drawString(x_coord, y_coord, widget[0].get()) #enters the name of the class
                                    if (len(widget[0].get()) * 7 + 25) < 150: #len(widget[0].get() * 7 converts the length of the info and the unit for canvas width
                                        x_coord += 100 #increase x coordinate to prevent overlapping
                                    else:
                                        x_coord += len(widget[0].get()) * 7 + 25
                                elif index == 2: #weight of class with option menu
                                    c.drawString(x_coord, y_coord, widget[0]["text"]) #enter the weight of the class
                                    if (len(widget[0]["text"]) * 7 + 25) < 50: #this should always happen
                                        x_coord += 50
                                    else:
                                        x_coord += len(widget[0].get()) * 7 + 25
                                elif index == 5: #year
                                    c.drawString(x_coord, y_coord, str(widget)) #enter the credit of the class
                                    if (len(str(widget)) * 7 + 25) < 50: #this should always happen
                                        x_coord += 50
                                    else:
                                        x_coord += len(str(widget)) * 7 + 25
                                else: #index 1 or 3, which is grade and credit
                                    c.drawString(x_coord, y_coord, widget[0].get())
                                    if (len(widget[0].get()) * 7 + 25) < 50: #len(widget[0].get() * 7 converts the length of the info and the unit for canvas width
                                        x_coord += 50 #increase x coordinate to prevent overlapping
                                    else:
                                        x_coord += len(widget[0].get()) * 7 + 25
                        y_coord -= 20
                    y_coord -= 20
                    c.drawString(200, y_coord, f"Unweighted GPA: {gpa_calculator.unweighted_gpa}")
                    y_coord -= 20
                    c.drawString(200, y_coord, f"Weighted GPA: {gpa_calculator.weighted_gpa}")

                    c.save()
                    webbrowser.open(file)

#this is to make sure entry boxes only have the text entered once for the grade from term info
first_frame_more_8 = [True]
first_frame_more_9 = [True]
first_frame_more_10 = [True]
first_frame_more_11 = [True]
first_frame_more_12 = [True]

#this is to make sure entry boxes only have the text entered once when importing previous_data
first_frame_previous_more_8 = [True]
first_frame_previous_more_9 = [True]
first_frame_previous_more_10 = [True]
first_frame_previous_more_11 = [True]
first_frame_previous_more_12 = [True]

def display_classes(year, first_frame_more_year, first_frame_previous_more_year):
    '''This function places the classes and displays information in them for cumulative GPA'''
    for i, Class in enumerate(gpa_calculator.class_data_cumulative):
        if Class[5] == year: #if this is a class for this year
            first_frame_more_year[0] = True #this resets every time the user goes to this screen
            for index, part in enumerate(Class[0:5]): #the widgets
                #part is Class[index]
                part[0].place(x=part[1] + x_location_change, y=part[2]) #place the widget based on the saved x and y position
                if index == 1 and Class[12] and first_frame_more_year[0]:  #the grade entry from term grades
                    part[0].delete(0, END)
                    part[0].insert(0, str(round(float(Class[12]))))
                    first_frame_more_year[0] = False #it will only appear in the entry on the first frame to prevent things such as 1717171717 instead of 17
                if previous_data_classes and first_frame_previous_more_year[0]: #if there was previous data not placed yet
                    try: #if there is previous data for a class but none for the classes of the grade, there will be an index error
                        if index == 0:
                            part[0].insert(0, previous_data_classes[i][0][0]) #Class Name
                        if index == 1 and not Class[12]:
                            try: #grade of class
                                part[0].insert(0, str(round(float(previous_data_classes[i][1][0]))))
                            except: #may cause error if there's an empty grade
                                pass
                        if index == 2: #weight of class
                            if previous_data_classes[i][2][0] == 1:
                                part[0].children['menu'].invoke(0) #option one
                            elif previous_data_classes[i][2][0] in [gpa_calculator.honors_scale_100, gpa_calculator.honors_scale_4]:
                                part[0].children['menu'].invoke(1) #option two if the weight is honors
                            elif previous_data_classes[i][2][0] in [gpa_calculator.AP_scale_100, gpa_calculator.AP_scale_4]:
                                part[0].children['menu'].invoke(2) #AP weight, option three
                        if index == 3:
                            part[0].insert(0, previous_data_classes[i][3][0]) #credit
                    except: #IndexError, but just in case there is another error
                        pass
            first_frame_previous_more_year[0] = False #it will only occur on the first time the screen is opened for that year

def update_ui():
    """This function updates the UI everytime the user enters a new screen"""
    global first_frame_settings, first_frame_cumulative_GPA

    if screen == "home": #this will be seen whenever the user goes home or at the start of the program
        home_screen.universal_back_button.place_forget() #the back button is forgotten here rather than elsewhere as multiple screens use it
        home_screen.intro_text.place(x=35 + x_location_change, y=30)
        home_screen.calc_my_gpa.place(x=135 + x_location_change, y=100)
        home_screen.help.place(x=245 + x_location_change, y=190)
        home_screen.data_information.place(x=147 + x_location_change, y=280)
    else:
        #when the screen is changed, every widget on the home screen will be forgotten
        for widget in [home_screen.intro_text, home_screen.calc_my_gpa, home_screen.help, home_screen.data_information]:
            widget.place_forget()

    if screen == "GPA_home":
        #widgets for GPA home screen
        home_screen.universal_back_button.place(x=0 + x_location_change, y=0)
        gpa_calculator.gpa_text.place(x=123 + x_location_change, y=30)
        gpa_calculator.quarterly_button.place(x=209 + x_location_change, y=90)
        gpa_calculator.cumulative_button.place(x=127 + x_location_change, y=180)
    else:
        #forgets the widgets, but not the universal back button
        for widget in [gpa_calculator.gpa_text, gpa_calculator.quarterly_button, gpa_calculator.cumulative_button]:
            widget.place_forget()

    if screen == "quarterly_grades":
        #this configures the GPA every frame
        gpa_calculator.unweighted_gpa_label.config(text=f"Unweighted GPA: {gpa_calculator.unweighted_gpa}")
        gpa_calculator.weighted_gpa_label.config(text=f"Weighted GPA: {gpa_calculator.weighted_gpa}")

        #this is the text at the top and the back button
        gpa_calculator.quarterly_top.place(x=108 + x_location_change, y=20)
        home_screen.universal_back_button.place(x=0 + x_location_change, y=0)

        #these are the widgets for determining the scale
        gpa_calculator.GPA_type_label.place(x=200 + x_location_change, y=95)
        gpa_calculator.current_scale.place(x=260 + x_location_change, y=95)
        gpa_calculator.change_scale.place(x=325 + x_location_change, y=90)

        #this is the the text above the class entry area
        gpa_calculator.class_name_label.place(x=137 + x_location_change, y=128)
        gpa_calculator.grade_label.place(x=259 + x_location_change, y=128)
        gpa_calculator.weight_label.place(x=320 + x_location_change, y=128)
        gpa_calculator.credit_label.place(x=387 + x_location_change, y=128)

        for Class in gpa_calculator.class_data_quarterly:
            for part in Class: #part = Class[0], places the part (class)
                part[0].place(x=part[1] + x_location_change, y=part[2])

        #this is where the GPAs are located before the user calculates their GPA
        gpa_calculator.unweighted_gpa_label.place(x=190 + x_location_change, y=445)
        gpa_calculator.weighted_gpa_label.place(x=200 + x_location_change, y=470)

        #these are the buttons at the bottom
        gpa_calculator.add_new_class.place(x=54 + x_location_change, y=500)
        gpa_calculator.whats_my_gpa.place(x=336 + x_location_change, y=500)
        gpa_calculator.delete_class.place(x=70 + x_location_change, y=554)
    else:
        #this forgets most of the widgets
        for widget in [gpa_calculator.quarterly_top, gpa_calculator.class_name_label, gpa_calculator.grade_label,
                       gpa_calculator.weight_label, gpa_calculator.credit_label, #gpa_calculator.year_label,
                       gpa_calculator.add_new_class, gpa_calculator.whats_my_gpa,
                       gpa_calculator.unweighted_gpa_label, gpa_calculator.weighted_gpa_label, gpa_calculator.delete_class,
                       gpa_calculator.current_scale, gpa_calculator.change_scale, gpa_calculator.GPA_type_label]:
            widget.place_forget()
        #this forgets the classes, but only when the screen is not on another screen where classes are displayed
        if screen not in ["cumulative_grades", "class_term_grades_chooser_8", "class_term_grades_chooser_9", "class_term_grades_chooser_10", "class_term_grades_chooser_11", "class_term_grades_chooser_12"]:
            for Class in gpa_calculator.class_data_quarterly:
                for widget in Class[0:4]: #acutal widgets
                  widget[0].place_forget()
        gpa_calculator.y_var = 150 #this assures that in the future, when the user adds new classes, they appear in the right spot.

    if screen == "cumulative_grades":
        #this configures the GPA once per frame
        gpa_calculator.unweighted_gpa_label.config(text=f"Unweighted GPA: {gpa_calculator.unweighted_gpa}")
        gpa_calculator.weighted_gpa_label.config(text=f"Weighted GPA: {gpa_calculator.weighted_gpa}")

        #these are the widgets at the top of the screen
        home_screen.universal_back_button.place(x=0 + x_location_change, y=0)
        gpa_calculator.Cumulative_GPA_text.place(x=75 + x_location_change, y=20)
        gpa_calculator.GPA_type_label.place(x=200 + x_location_change, y=95)
        gpa_calculator.current_scale.place(x=260 + x_location_change, y=95)
        gpa_calculator.change_scale.place(x=325 + x_location_change, y=90)

        #These are the labels that display the text for the years
        gpa_calculator.year_8_label.place(x=117 + x_location_change, y=125)
        gpa_calculator.year_9_label.place(x=432 + x_location_change, y=125)
        gpa_calculator.year_10_label.place(x=117 + x_location_change, y=305)
        gpa_calculator.year_11_label.place(x=432 + x_location_change, y=305)
        gpa_calculator.year_12_label.place(x=117 + x_location_change, y=485)

        #these are the buttons to access more information for the year
        gpa_calculator.more_8.place(x=87 + x_location_change, y=155)
        gpa_calculator.more_9.place(x=402 + x_location_change, y=155)
        gpa_calculator.more_10.place(x=87 + x_location_change, y=335)
        gpa_calculator.more_11.place(x=402 + x_location_change, y=335)
        gpa_calculator.more_12.place(x=87 + x_location_change, y=515)

        #widgets for calcuating the cumulative GPA
        gpa_calculator.whats_my_gpa.place(x=337 + x_location_change, y=500)
        gpa_calculator.unweighted_gpa_label.place(x=337 + x_location_change, y=560)
        gpa_calculator.weighted_gpa_label.place(x=337 + x_location_change, y=590)
    else:
        #deletes more of the widgets
        for widget in [gpa_calculator.Cumulative_GPA_text, gpa_calculator.year_8_label, gpa_calculator.more_8,
                       gpa_calculator.year_9_label, gpa_calculator.more_9,
                       gpa_calculator.year_10_label, gpa_calculator.more_10,
                       gpa_calculator.year_11_label, gpa_calculator.more_11,
                       gpa_calculator.year_12_label, gpa_calculator.more_12]:
                       widget.place_forget()

    if screen == "more_8":
        #the labels at the top
        gpa_calculator.top_8.place(x=219 + x_location_change, y=10)
        gpa_calculator.class_name_label_8.place(x=137 + x_location_change, y=60)
        gpa_calculator.grade_label_8.place(x=259 + x_location_change, y=60)
        gpa_calculator.weight_label_8.place(x=320 + x_location_change, y=60)
        gpa_calculator.credit_label_8.place(x=387 + x_location_change, y=60)

        #the buttons at the bottom
        gpa_calculator.add_class_8.place(x=153 + x_location_change, y=550)
        gpa_calculator.delete_class_8.place(x=290 + x_location_change, y=550)

        #add the classes
        display_classes(8, first_frame_more_8, first_frame_previous_more_8)
    else:
        #forget most widgets
        for widget in [gpa_calculator.top_8, gpa_calculator.class_name_label_8, gpa_calculator.grade_label_8, gpa_calculator.weight_label_8,
                       gpa_calculator.credit_label_8, gpa_calculator.add_class_8, gpa_calculator.delete_class_8]:
            widget.place_forget()
        #forgets the classes if the screen is in a screen that the user would have been brought to from this screen
        if screen in ["cumulative_grades", "class_term_grades_chooser_8", "class_term_grades_chooser_9", "class_term_grades_chooser_10", "class_term_grades_chooser_11", "class_term_grades_chooser_12"]:
            for Class in gpa_calculator.class_data_cumulative:
                for widget in Class[0:5]:
                    widget[0].place_forget()

    if screen == "more_9":
        #the labels at the top
        gpa_calculator.top_9.place(x=219 + x_location_change, y=10)
        gpa_calculator.class_name_label_9.place(x=137 + x_location_change, y=60)
        gpa_calculator.grade_label_9.place(x=259 + x_location_change, y=60)
        gpa_calculator.weight_label_9.place(x=320 + x_location_change, y=60)
        gpa_calculator.credit_label_9.place(x=387 + x_location_change, y=60)

        #the buttons at the bottom
        gpa_calculator.add_class_9.place(x=153 + x_location_change, y=550)
        gpa_calculator.delete_class_9.place(x=290 + x_location_change, y=550)

        #add the classes
        display_classes(9, first_frame_more_9, first_frame_previous_more_9)
    else:
        #forget most widgets
        for widget in [gpa_calculator.top_9, gpa_calculator.class_name_label_9, gpa_calculator.grade_label_9,
                       gpa_calculator.weight_label_9,
                       gpa_calculator.credit_label_9, gpa_calculator.add_class_9, gpa_calculator.delete_class_9]:
            widget.place_forget()
        # forgets the classes if the screen is in a screen that the user would have been brought to from this screen
        if screen in ["cumulative_grades", "class_term_grades_chooser_8", "class_term_grades_chooser_9", "class_term_grades_chooser_10", "class_term_grades_chooser_11", "class_term_grades_chooser_12"]:
            for Class in gpa_calculator.class_data_cumulative:
                for widget in Class[0:5]:
                    widget[0].place_forget()

    if screen == "more_10":
        #the labels at the top
        gpa_calculator.top_10.place(x=211 + x_location_change, y=10)
        gpa_calculator.class_name_label_10.place(x=137 + x_location_change, y=60)
        gpa_calculator.grade_label_10.place(x=259 + x_location_change, y=60)
        gpa_calculator.weight_label_10.place(x=320 + x_location_change, y=60)
        gpa_calculator.credit_label_10.place(x=387 + x_location_change, y=60)

        #the buttons at the bottom
        gpa_calculator.add_class_10.place(x=153 + x_location_change, y=550)
        gpa_calculator.delete_class_10.place(x=290 + x_location_change, y=550)

        #add the classes
        display_classes(10, first_frame_more_10, first_frame_previous_more_10)
    else:
        #forget most widgets
        for widget in [gpa_calculator.top_10, gpa_calculator.class_name_label_10, gpa_calculator.grade_label_10,
                       gpa_calculator.weight_label_10,
                       gpa_calculator.credit_label_10, gpa_calculator.add_class_10, gpa_calculator.delete_class_10]:
            widget.place_forget()
        #forgets the classes if the screen is in a screen that the user would have been brought to from this screen
        if screen in ["cumulative_grades", "class_term_grades_chooser_8", "class_term_grades_chooser_9", "class_term_grades_chooser_10", "class_term_grades_chooser_11", "class_term_grades_chooser_12"]:
            for Class in gpa_calculator.class_data_cumulative:
                for widget in Class[0:5]:
                    widget[0].place_forget()

    if screen == "more_11":
        #the labels at the top
        gpa_calculator.top_11.place(x=211 + x_location_change, y=10)
        gpa_calculator.class_name_label_11.place(x=137 + x_location_change, y=60)
        gpa_calculator.grade_label_11.place(x=259 + x_location_change, y=60)
        gpa_calculator.weight_label_11.place(x=320 + x_location_change, y=60)
        gpa_calculator.credit_label_11.place(x=387 + x_location_change, y=60)

        #the buttons at the bottom
        gpa_calculator.add_class_11.place(x=153 + x_location_change, y=550)
        gpa_calculator.delete_class_11.place(x=290 + x_location_change, y=550)

        #add the classes
        display_classes(11, first_frame_more_11, first_frame_previous_more_11)
    else:
        #forget most widgets
        for widget in [gpa_calculator.top_11, gpa_calculator.class_name_label_11, gpa_calculator.grade_label_11,
                       gpa_calculator.weight_label_11,
                       gpa_calculator.credit_label_11, gpa_calculator.add_class_11, gpa_calculator.delete_class_11]:
            widget.place_forget()
        #forgets the classes if the screen is in a screen that the user would have been brought to from this screen
        if screen in ["cumulative_grades", "class_term_grades_chooser_8", "class_term_grades_chooser_9", "class_term_grades_chooser_10", "class_term_grades_chooser_11", "class_term_grades_chooser_12"]:
            for Class in gpa_calculator.class_data_cumulative:
                for widget in Class[0:5]:
                    widget[0].place_forget()

    if screen == "more_12":
        #the labels at the top
        gpa_calculator.top_12.place(x=211 + x_location_change, y=10)
        gpa_calculator.class_name_label_12.place(x=137 + x_location_change, y=60)
        gpa_calculator.grade_label_12.place(x=259 + x_location_change, y=60)
        gpa_calculator.weight_label_12.place(x=320 + x_location_change, y=60)
        gpa_calculator.credit_label_12.place(x=387 + x_location_change, y=60)

        #the buttons at the bottom
        gpa_calculator.add_class_12.place(x=153 + x_location_change, y=550)
        gpa_calculator.delete_class_12.place(x=290 + x_location_change, y=550)

        #add the classes
        display_classes(12, first_frame_more_12, first_frame_previous_more_12)
    else:
        #forget most widgets
        for widget in [gpa_calculator.top_12, gpa_calculator.class_name_label_12, gpa_calculator.grade_label_12,
                       gpa_calculator.weight_label_12,
                       gpa_calculator.credit_label_12, gpa_calculator.add_class_12, gpa_calculator.delete_class_12]:
            widget.place_forget()
        # forgets the classes if the screen is in a screen that the user would have been brought to from this screen
        if screen in ["cumulative_grades", "class_term_grades_chooser_8", "class_term_grades_chooser_9", "class_term_grades_chooser_10", "class_term_grades_chooser_11", "class_term_grades_chooser_12"]:
            for Class in gpa_calculator.class_data_cumulative:
                for widget in Class[0:5]:
                    widget[0].place_forget()

    #if the screen is not a term grades chooser, don't display those widgets
    if screen not in ["class_term_grades_chooser_8", "class_term_grades_chooser_9", "class_term_grades_chooser_10", "class_term_grades_chooser_11", "class_term_grades_chooser_12"]:
        if gpa_calculator.term_info_widgets:
            for widget in gpa_calculator.term_info_widgets[0]: #[0] as it's a list with one element (a list of widgets)
                widget.place_forget()
            gpa_calculator.term_info_widgets.clear() #cleares the list

    if screen == "help_menu":
        #this places all the widgets that appear on the home screen for the help menu
        home_screen.universal_back_button.place(x=0 + x_location_change, y=0)
        help_menu.help_menu_label.place(x=208 + x_location_change, y=30)
        help_menu.instructions.place(x=190 + x_location_change, y=100)
        help_menu.settings.place(x=220 + x_location_change, y=190)
    else:
        #this deletes all the widgets, except for the back button
        for widget in [help_menu.help_menu_label, help_menu.instructions, help_menu.settings]:
            widget.place_forget()

    if screen == "instructions_1":
        #widgets for instructions one of the help menu
        home_screen.universal_back_button.place(x=0 + x_location_change, y=0)
        help_menu.instructions_top.place(x=204 + x_location_change, y=10)
        help_menu.intro_instructions.place(x=95 + x_location_change, y=60)
        help_menu.quarterly_GPA_instructions.place(x=34 + x_location_change, y=100)
        help_menu.cumulative_GPA_instructions.place(x=33 + x_location_change, y=170)

        help_menu.QA_top.place(x=109 + x_location_change, y=300)
        help_menu.Q1.place(x=0 + x_location_change, y=360)
        help_menu.Q2.place(x=0 + x_location_change, y=490)
        help_menu.next_page.place(x=233 + x_location_change, y=595)
    else:
        #deletes most of the widgets, but if it's instructions_2 for the next screen, it doesn't get rid of the top widget
        if screen != "instructions_2":
            help_menu.instructions_top.place_forget()
        for widget in [help_menu.intro_instructions, help_menu.quarterly_GPA_instructions, help_menu.cumulative_GPA_instructions, #this is all for the instructions
                       help_menu.QA_top, help_menu.Q1, help_menu.Q2, help_menu.next_page]: #this is all for the Q&A
            widget.place_forget()

    if screen == "instructions_2":
        #widgets for instructions_2 screen
        home_screen.universal_back_button.place(x=0 + x_location_change, y=0)
        help_menu.instructions_top.place(x=204 + x_location_change, y=10)
        help_menu.Q3.place(x=0 + x_location_change, y=60)
        help_menu.Q4.place(x=0 + x_location_change, y=260)
        help_menu.Q5.place(x=0 + x_location_change, y=370)
        help_menu.Q6.place(x=0 + x_location_change, y=430)
        help_menu.Q7.place(x=0 + x_location_change, y=490)
        help_menu.previous_page.place(x=213 + x_location_change, y=595)
    else:
        #deletes most of the widget, but not the top instructions if the new screen is instructions_1
        if screen != "instructions_1":
            help_menu.instructions_top.place_forget()
        for widget in [help_menu.Q3, help_menu.Q4, help_menu.Q5,
                       help_menu.Q6, help_menu.Q7, help_menu.previous_page]:
            widget.place_forget()

    if screen == "settings":
        #widgets for the settings
        home_screen.universal_back_button.place(x=0 + x_location_change, y=0)
        help_menu.settings_top.place(x=233 + x_location_change, y=30)

        #this places the labels for changing Honors and AP Weight
        help_menu.change_honors_weight_100_label.place(x=198 + x_location_change, y=85)
        help_menu.change_AP_weight_100_label.place(x=211 + x_location_change, y=115)
        help_menu.change_honors_weight_4_label.place(x=205 + x_location_change, y=145)
        help_menu.change_AP_weight_4_label.place(x=218 + x_location_change, y=175)

        # this places the entries for changing Honors and AP weight
        help_menu.change_honors_weight_100_entry.place(x=352 + x_location_change, y=85)
        help_menu.change_AP_weight_100_entry.place(x=337 + x_location_change, y=115)
        help_menu.change_honors_weight_4_entry.place(x=343 + x_location_change, y=145)
        help_menu.change_AP_weight_4_entry.place(x=331 + x_location_change, y=175)

        #this places the labels for changing default term weights
        help_menu.change_Q1_weight_label.place(x=214 + x_location_change, y=235)
        help_menu.change_Q2_weight_label.place(x=214 + x_location_change, y=265)
        help_menu.change_E2_weight_label.place(x=216 + x_location_change, y=295)
        help_menu.change_Q3_weight_label.place(x=214 + x_location_change, y=325)
        help_menu.change_Q4_weight_label.place(x=214 + x_location_change, y=355)
        help_menu.change_E4_weight_label.place(x=208 + x_location_change, y=385)

        #this places the entries for changing default term weights
        help_menu.change_Q1_weight_entry.place(x=329 + x_location_change, y=235)
        help_menu.change_Q2_weight_entry.place(x=329 + x_location_change, y=265)
        help_menu.change_E2_weight_entry.place(x=327 + x_location_change, y=295)
        help_menu.change_Q3_weight_entry.place(x=329 + x_location_change, y=325)
        help_menu.change_Q4_weight_entry.place(x=329 + x_location_change, y=355)
        help_menu.change_E4_weight_entry.place(x=334 + x_location_change, y=385)

        help_menu.confirm_settings_button.place(x=204 + x_location_change, y=445)

        if first_frame_settings:
            #if this is the first frame for the settings (in the whole program), the information will be inputed
            #Honors and AP weight
            help_menu.change_honors_weight_100_entry.insert(0, str(gpa_calculator.honors_scale_100))
            help_menu.change_AP_weight_100_entry.insert(0, str(gpa_calculator.AP_scale_100))
            help_menu.change_honors_weight_4_entry.insert(0, str(gpa_calculator.honors_scale_4))
            help_menu.change_AP_weight_4_entry.insert(0, str(gpa_calculator.AP_scale_4))

            #term grades
            help_menu.change_Q1_weight_entry.insert(0, str(gpa_calculator.default_Q1))
            help_menu.change_Q2_weight_entry.insert(0, str(gpa_calculator.default_Q2))
            help_menu.change_E2_weight_entry.insert(0, str(gpa_calculator.default_E2))
            help_menu.change_Q3_weight_entry.insert(0, str(gpa_calculator.default_Q3))
            help_menu.change_Q4_weight_entry.insert(0, str(gpa_calculator.default_Q4))
            help_menu.change_E4_weight_entry.insert(0, str(gpa_calculator.default_E4))
            first_frame_settings = False #makes sure the information only appears once

    else:
        #deltes most of the widgets
        for widget in [help_menu.settings_top, help_menu.change_honors_weight_100_label, help_menu.change_honors_weight_4_label, help_menu.change_AP_weight_100_label, help_menu.change_AP_weight_4_label,
                       help_menu.change_honors_weight_100_entry, help_menu.change_honors_weight_4_entry, help_menu.change_AP_weight_100_entry, help_menu.change_AP_weight_4_entry,
                       help_menu.change_Q1_weight_label, help_menu.change_Q2_weight_label, help_menu.change_E2_weight_label, help_menu.change_Q3_weight_label, help_menu.change_Q4_weight_label, help_menu.change_E4_weight_label,
                       help_menu.change_Q1_weight_entry, help_menu.change_Q2_weight_entry, help_menu.change_E2_weight_entry, help_menu.change_Q3_weight_entry, help_menu.change_Q4_weight_entry, help_menu.change_E4_weight_entry,
                       help_menu.confirm_settings_button]:
            widget.place_forget()

    if screen == "data_menu":
        #widgets for data_menu
        home_screen.universal_back_button.place(x=0 + x_location_change, y=0)
        data_menu.data_info_top.place(x=160 + x_location_change, y=10)
        data_menu.load_data_button.place(x=200 + x_location_change, y=70)
        data_menu.delete_data_button.place(x=190 + x_location_change, y=160)
        data_menu.save_data_button.place(x=139 + x_location_change, y=250)
    else:
        #deltes most of the widgets
        for widget in [data_menu.data_info_top, data_menu.load_data_button, data_menu.delete_data_button, data_menu.save_data_button]:
            widget.place_forget()

def improve_entry_boxes(event):
    '''This function makes the entry box display the front of it when the user clicks somewhere else'''
    #this is a list of every entry box in the program
    entry_boxes = [widget for widget in window.winfo_children() if isinstance(widget, Entry)]
    for entry in entry_boxes:
        if event.widget != entry: #the event is whenever the user clicks in the window, if the click is not on the entry, this will trigger
            text = entry.get() #the text as it will get deleted
            entry.delete(0, END) #deletes the text
            entry.insert(0, text) #inserts the text, now displaying from the beginning

def save_data_when_program_finished(sig, frame):
    '''This function saves the data if the program ends unexpectedly'''
    file_append.truncate(0) #clears the file
    if len(gpa_calculator.for_export) >= 1: #if there is a class
        #append the non-class elements
        gpa_calculator.for_export.append([gpa_calculator.gpa_scale, gpa_calculator.honors_scale_100, gpa_calculator.AP_scale_100, gpa_calculator.honors_scale_4, gpa_calculator.AP_scale_4,
                                          gpa_calculator.year_8_classes_y_var, gpa_calculator.year_9_classes_y_var, gpa_calculator.year_10_classes_y_var, gpa_calculator.year_11_classes_y_var, gpa_calculator.year_12_classes_y_var,
                                          gpa_calculator.default_Q1, gpa_calculator.default_Q2, gpa_calculator.default_E2, gpa_calculator.default_Q3, gpa_calculator.default_Q4, gpa_calculator.default_E4, ])
        file_append.write(f"{gpa_calculator.for_export}\n") #update the file
    file_append.close() #close the file
    file_read.close()
    sys.exit() #ends the program

def update_frame():
    '''This updates the program once per 17 ms (about 60 fps), updating the ui and running functions for the classes. It also validiates user input'''
    global x_location_change, time, file_empty
    #these lists contain every entry box and option menu in the program
    entry_boxes = [widget for widget in window.winfo_children() if isinstance(widget, Entry)]
    option_menus = [widget for widget in window.winfo_children() if isinstance(widget, OptionMenu)]
    time += 1 #this detemines how many frames have passed
    gpa_calculator.get_class_data() #must be ran every frame
    update_ui() #must be ran every frame
    signal.signal(signal.SIGINT, save_data_when_program_finished) #this will append the data to the file if the program ends with a Keyboard Interupt

    i = 0 #resets every frame
    entries_term_grade_error = []
    error_labels_for_term_grades = []

    for entry in entry_boxes:
        if entry.winfo_ismapped(): #only entry boxes on the screen
            isfloat = lambda s: s.replace('.', '', 1).isdigit() #sees if the entry has float
            if entry.winfo_x() == 256 + x_location_change: #grade in more info:
                if isfloat(entry.get()): #if a float, append to the list
                    entries_term_grade_error.append(entry.get())
                if not entries_term_grade_error: #cause a warning sign to appear
                    error_labels_for_term_grades.append(error_labels[i])
                    #places the warning sign at the end of the entry
                    error_labels[i].place(x=entry.winfo_x() + entry.winfo_width() - error_labels[i].winfo_width() - 5, y=entry.winfo_y() + 5)
                    error_labels[i].lift() #the warning sign will be above everything else
                else:
                    error_labels[i].place_forget() #if there is something in entries_terms_grade_error (there's an input), the warning signs will be delted
                    for label in error_labels_for_term_grades: #forgets all warning labels for term grades
                        label.place_forget()
            elif entry.winfo_x() in [251 + x_location_change, 126 + x_location_change, 441 + x_location_change]:
                #if the widget is a grade entry
                if entry.get() == "": #if the widget is empty, place the error sign at the end of the widget
                    error_labels[i].place(x=entry.winfo_x() + entry.winfo_width() - error_labels[i].winfo_width() - 5, y=entry.winfo_y() + 5)
                    error_labels[i].lift() #make the error sign above everything else
                elif not isfloat(entry.get()) and not (entry.get() in gpa_calculator.grades_4 and gpa_calculator.gpa_scale == 4.0):
                    #this will happen when the grade is not a float, except for when it's a letter grade and the GPA scale is 4.0
                    error_labels[i].place(x=entry.winfo_x() + entry.winfo_width() - error_labels[i].winfo_width() - 5,  y=entry.winfo_y() + 5)
                    error_labels[i].lift()
                else:
                    error_labels[i].place_forget()
            elif entry.get() == "" or (not isfloat(entry.get()) and entry.winfo_x() not in [100 + x_location_change, 22 + x_location_change, 337 + x_location_change]): #second part checks if it's float, but only if it's not a class name entry
                #if the entry is blank or if the entry isn't float and the entry isn't a class name (they don't need to be float)
                error_labels[i].place(x=entry.winfo_x() + entry.winfo_width() - error_labels[i].winfo_width() - 5, y=entry.winfo_y() + 5)
                error_labels[i].lift()
            else:
                error_labels[i].place_forget()
        else: #removes the error label. If it never existed nothing happens (which is what should happen)
            error_labels[i].place_forget()
        i += 1 #moves to the next index in error_labels

    for option in option_menus: #option menu for weight of class
        if option.winfo_ismapped(): #if option menu on screen
            if option["text"] == "": #if the option menu is unfilled
                error_labels[i].place(x=option.winfo_x(), y=option.winfo_y() + 5)
                error_labels[i].lift()
            else:
                error_labels[i].place_forget()
        else:
            error_labels[i].place_forget()
        i += 1 #increases with the same variable as for entry boxes
    for entry in entry_boxes:
        entry.config(selectbackground="black") #this makes it so when text is hightlighted, the highlight it black. It is done here as it was not added until late in development

    x_location_change = (window.winfo_width() / 2) - 300 #this varaible accounts for change in the screen width and is used to centralize everything. It is located here rather than at the start as it must be updated.
    #the default size is 700x700, so this will be 50 by default. Much of the program was made with this at 600x600.
    window.after(17, update_frame) #the function is recursive and will run from the start of the program to the end of it

#this creates instances of each classe
gpa_calculator = GPACalculator()
home_screen = HomeScreen()
help_menu = HelpMenu()
data_menu = LoadingData()

update_frame() #runs the function to update the program

#this list is every label that has text appear when hovered over
labels_for_help_text_when_hover = [gpa_calculator.class_name_label, gpa_calculator.grade_label, gpa_calculator.weight_label, gpa_calculator.credit_label, #labels for entry boxes, quarter GPA screen
                                   gpa_calculator.GPA_type_label, gpa_calculator.current_scale, gpa_calculator.unweighted_gpa_label, gpa_calculator.weighted_gpa_label, #labels for UW vs W gpa and 100.0 vs 4.0 gpa
                                   gpa_calculator.year_8_label,  #states to only enter high school level classes for 8th Grade
                                   gpa_calculator.class_name_label_8, gpa_calculator.grade_label_8, gpa_calculator.weight_label_8, gpa_calculator.credit_label_8, #labels for entry boxes above 8th grade, cumulative GPA screen
                                   gpa_calculator.class_name_label_9, gpa_calculator.grade_label_9, gpa_calculator.weight_label_9, gpa_calculator.credit_label_9, #labels for entry boxes above 9th grade, cumulative GPA screen
                                   gpa_calculator.class_name_label_10, gpa_calculator.grade_label_10, gpa_calculator.weight_label_10, gpa_calculator.credit_label_10, #labels for entry boxes above 10th grade, cumulative GPA screen
                                   gpa_calculator.class_name_label_11, gpa_calculator.grade_label_11, gpa_calculator.weight_label_11, gpa_calculator.credit_label_11, #labels for entry boxes above 11th grade, cumulative GPA screen
                                   gpa_calculator.class_name_label_12, gpa_calculator.grade_label_12, gpa_calculator.weight_label_12, gpa_calculator.credit_label_12, #labels for entry boxes above 12th grade, cumulative GPA screen
                                   ]
#this is the text that will appear when the label is hovered over
widget_help_label = Label(window, bg=TEXTCOLOR, fg=BACKGROUND_COLOR)

def start_hover(event):
    """This function makes it so that when a widget is hovered over, a help text appears"""
    lines = 0 #lines of widget_help_label
    x_change = 0 #length of widget_help_label
    #this function originally used widget_help_label.winfo_width(), but that was not accurate so it had to be done manually
    if event.widget.winfo_ismapped(): #if on screen
        #event.widget = the mouse is over that widget
        if event.widget in [gpa_calculator.class_name_label, gpa_calculator.class_name_label_8, gpa_calculator.class_name_label_9,
                            gpa_calculator.class_name_label_10, gpa_calculator.class_name_label_11, gpa_calculator.class_name_label_12]:
            widget_help_label.config(text="Enter the name of your class")
            #this displays information when the user hovers over class_name_label
            lines = 1
            x_change = 155
        elif event.widget in [gpa_calculator.grade_label, gpa_calculator.grade_label_8, gpa_calculator.grade_label_9,
                              gpa_calculator.grade_label_10, gpa_calculator.grade_label_11, gpa_calculator.grade_label_12]:
            widget_help_label.config(text="Enter the grade you received in that class")
            #info for grade label
            lines = 1
            x_change = 221
        elif event.widget in [gpa_calculator.weight_label, gpa_calculator.weight_label_8, gpa_calculator.weight_label_9,
                              gpa_calculator.weight_label_10, gpa_calculator.weight_label_11, gpa_calculator.weight_label_12]:
            #info for weight label, with different responses based on the GPA scale
            if gpa_calculator.gpa_scale == 100.0:
                widget_help_label.config(text=f"Select the weight of the class \n Honors get {gpa_calculator.honors_scale_100} weight and AP gets {gpa_calculator.AP_scale_100} weight \n this can be adjusted in the settings")
                lines = 3
                x_change = 263
            elif gpa_calculator.gpa_scale == 4.0:
                widget_help_label.config(text=f"Select the weight of the class \n Honors get {gpa_calculator.honors_scale_4} weight and AP gets {gpa_calculator.AP_scale_4} weight \n this can be adjusted in the settings")
                lines = 3
                x_change = 269
        elif event.widget == gpa_calculator.credit_label:
            widget_help_label.config(text="Enter the credit for the course \n Every day (A-F) courses usually get 1 credit \n Alternative Day courses usually get .5 credit") #BE SURE TO ALLOW FOR ½ and ¼
            #for credit label on the quarterly screen
            lines = 3
            x_change = 237
        elif event.widget in [gpa_calculator.credit_label_8, gpa_calculator.credit_label_9,
                              gpa_calculator.credit_label_10, gpa_calculator.credit_label_11, gpa_calculator.credit_label_12]:
            widget_help_label.config(text="Enter the credit for the course \n Every day (A-F) Full Year courses usually get 1 credit \n Alternative Day or Semester courses usually get .5 credit \n A semester of PE gets .25 credit")
            #for credit label on the cumulative screen
            lines = 4
            x_change = 305
        elif event.widget == gpa_calculator.GPA_type_label:
            widget_help_label.config(text="The GPA Scale could be 100.0 (what Monroe Woodbury uses) \n or 4.0 (what some other schools use)")
            #for 100.0 vs 4.0 GPA
            lines = 2
            #if the widget is on the left of the screen, there is no need for x_change
        elif event.widget == gpa_calculator.current_scale:
            #this displays information when the current scale is hovered over
            if gpa_calculator.gpa_scale == 100.0:
                widget_help_label.config(text="Honors get 1.03 weight and AP gets 1.05 weight \n this can be adjusted in the settings")
                lines = 2
            elif gpa_calculator.gpa_scale == 4.0:
                widget_help_label.config(text="Honors get 1.125 weight and AP gets 1.25 weight \n This can be adjusted in the settings")
                lines = 2
        elif event.widget == gpa_calculator.unweighted_gpa_label:
            #for unweighted GPA label
            widget_help_label.config(text="This is your GPA without giving extra points for Honors/AP Classes")
            lines = 1
            x_change = 357
        elif event.widget == gpa_calculator.weighted_gpa_label:
            #for weighted GPA label
            widget_help_label.config(text="This is your GPA with extra points for Honors/AP Classes")
            lines = 1
            x_change = 303
        elif event.widget == gpa_calculator.year_8_label:
            #for year label for 8th Grade
            widget_help_label.config(text="Only enter high school level classes (Algebra, Biology, World Langauge)")
            lines = 1
        elif event.widget == gpa_calculator.term_grade_label:
            #for label above the term grade entries
            widget_help_label.config(text="Enter the grade you received in the term")
            lines = 1
            x_change = 217
        elif event.widget == gpa_calculator.term_weight_label:
            #for label above the term weight entries
            widget_help_label.config(text="Enter the weight that the term had for your F4 grade \nIf this term did not impact your F4 grade, put 0 \nThe defaults can be changed in the settings")
            lines = 3
            x_change = 283
        elif event.widget == gpa_calculator.Q1:
            #Quarter 1
            widget_help_label.config(text=f"Q1 Grade")
            lines = 1
        elif event.widget == gpa_calculator.Q2:
            #Quarter 2
            widget_help_label.config(text=f"Q2 Grade")
            lines = 1
        elif event.widget == gpa_calculator.E2:
            #Midterm
            widget_help_label.config(text=f"Midterm")
            lines = 1
        elif event.widget == gpa_calculator.Q3:
            #Quarter 3
            widget_help_label.config(text=f"Q3 Grade")
            lines = 1
        elif event.widget == gpa_calculator.Q4:
            #Quarter 4
            widget_help_label.config(text=f"Q4 Grade")
            lines = 1
        elif event.widget == gpa_calculator.E4:
            #Final
            widget_help_label.config(text=f"Final Exam")
            lines = 1

        help_label_x = event.widget.winfo_x() #x position of the widget
        help_label_y = event.widget.winfo_y() #y position of the widget

        if lines == 1:
            help_label_y = event.widget.winfo_y() - 20 #if help_text_label is one line, it will be located 20 pixels above the widget
        elif lines == 2:
            help_label_y = event.widget.winfo_y() - 35 #if help_text_label is two lines, it will be located 35 pixels above the widget
        elif lines == 3:
            help_label_y = event.widget.winfo_y() - 50 #if help_text_label is three lines, it will be located 50 pixels above the widget
        elif lines == 4:
            help_label_y = event.widget.winfo_y() - 65 #if help_text_label is four lines, it will be located 65 pixels above the widget

        if event.widget.winfo_x() > 300: #if on the right of the screen
            help_label_x -= x_change - event.widget.winfo_width() #the help label text will end at the widget, not start at it

        widget_help_label.place(x=help_label_x, y=help_label_y)
        widget_help_label.lift()

def end_hover(event):
    """This function makes it so that when a widget stops being hovered over, the help text goes away"""
    widget_help_label.place_forget()
    widget_help_label.config(text="")

#binds the labels based on if the mouse is on them
for label in labels_for_help_text_when_hover:
    label.bind("<Enter>", start_hover)
    label.bind("<Leave>", end_hover)

#binds the improve_entry_boxes function
window.bind("<Button-1>", improve_entry_boxes)

window.mainloop() #this line is needed to run the GUI
#the rest of the code happens when the window is closed
file_append.truncate(0) #clears the file
if len(gpa_calculator.for_export) >= 1: #if there is a class
    #append the non-class elements
    gpa_calculator.for_export.append([gpa_calculator.gpa_scale, gpa_calculator.honors_scale_100, gpa_calculator.AP_scale_100, gpa_calculator.honors_scale_4, gpa_calculator.AP_scale_4,
                                      gpa_calculator.year_8_classes_y_var, gpa_calculator.year_9_classes_y_var, gpa_calculator.year_10_classes_y_var, gpa_calculator.year_11_classes_y_var, gpa_calculator.year_12_classes_y_var,
                                      gpa_calculator.default_Q1, gpa_calculator.default_Q2, gpa_calculator.default_E2, gpa_calculator.default_Q3, gpa_calculator.default_Q4, gpa_calculator.default_E4, ])
    file_append.write(f"{gpa_calculator.for_export}\n") #update the file
file_append.close() #close the file
file_read.close()
