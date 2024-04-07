**Modules** The modules used for this project were Tkinter (to make the GUI), math (to make a big number), os (to find the size of the file),
signal (to detect KeyBoardInterrupt), sys (to end the program upon KeyBoardInterrupt), ast (to parse the file), 
reportlab (to make a PDF), webbrowser (to open the PDF), datetime (to get the date for the PDF). 
Tkinter and Reportlab may needed to be installed using pip.

**Image** The image was taken for free from https://www.freeiconspng.com/images/error-2

**Saving Data** The program opens a file called "data_for_calc_gpa.txt". The for_export list in the GPACalculator class is appended 
to whenever the user makes a new class on the cumulative screen. The contents of that list are updated once per frame with the
get_class_data function in the GPACalculator class. When the program terminates, more information is appended to that list, such as 
default values the user changed throughout the program such as weights of Honors and AP classes, and that list is written into the file.
The information is written in the file after window.mainloop(), meaning it would run once the user closes the GUI. If the program ends
with a KeyBoardInterrupt, the data is saved with the save_data_when_program_finished function.

**Loading in Data** If there is data in the file, which is checked with os.path.getsize("data_for_calc_gpa.txt"), and the user hits 
Load Data, the data in the file will be parsed with ast and the information in the program will updated based on the information in the file.
