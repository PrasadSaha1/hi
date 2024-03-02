# FBLA-Introduction-to-Programming
Greetings! My name is Prasad Saha. I am a sophomore at Monroe-Woodbury High School, and this is my project for NYS FBLA Introduction to Programming. <br>
The task was to create a program for students at my school to calculate their weighted and unweighted GPA. This calculator does that using Monroe-Woodbury's grading system. <br>
For a simple experience, users can go to Quarterly GPA, which is made for a single quarter. A more comprehensive GPA can be found if the user clicks Annual/Cumulative GPA. This program defaults to MW's grading scale, but the user can adjust the grading scale throughout the program. It also saves the user's data with a file. <br>
This program was made using Python's Tkinter module, which is a module that creates GUIs. To run this program, copy the code and the error.png image into a compiler. I used Pycharm to make this program, but it should work with other compilers.  <br>
Tkinter is a built-in module, but I've noticed that many online compilers do not support Tkinter. If that is the case, you will have to use an IDE such as Pycharm or VS code. You may have to install it with pip <br>
This program allows the user to save their data through using files. This is done automatically and no work is required by the user to set up these files <br>
There is a small bug that occurs when the user enters two classes of the same name. The user should avoid doing that as classes after the first class will be ignored when storing data into the file <br>
This program allows the user to export their data as a PDF. Reportlab must be installed using pip. if reportlab can not be installed for whatever reason, comment out these lines and put pass in save_my_gpa_func in LoadingData, commenting everything else out <br>
This program also uses an image to validate user input. If that image can not be imported (the image is in the Github), follow the instructions in the program to fix it


