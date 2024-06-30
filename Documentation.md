**Modules** The installed modules used include Pyside6 (to make the GUI), openpyxl (to make an Excel spreadsheet), reportlab (to make a PDF), csv (to save data locally), and MySQL (for the account system).

**Image**  Error Message by REditsOfficial, Wikimedia Commons, https://commons.wikimedia.org/wiki/File:ErrorMessage.png

**Program Basics** On the Calculate my GPA screen, the user would choose the scope of their GPA. They would then enter in all of the required information (name and year are optional) for each class they are taking. They can retrieve their weighted and unweighted GPA when ready.
The user can click more next to each class to open the term grades calculator. Users would be able to get a more exact GPA as calculations will use unrounded grades from their terms. This is available on all scopes, but it would not make sense on the Quarterly scope. 
Additionally, the user can click more next to a term and open the assignments menu. They would input categories before entering in assignments for a very exact GPA. 

**Changing the Screen** At the start of the program, various instances of QWidget() are created. These instances are added to a stacked_widget(), whose index is changed with the change_screen() function. The identifiers of the QWidget() instances are lowercase, but the indexes that will act as parameters for change_screen() are uppercase for readability.

**User Experience** The program has several features to benefit the user experience. For instance, the user can hover over many widgets in the program to reveal help text. In addition, whenever an input is invalid, an error sign will be displayed. The user can visit the instructions and FAQ screens to learn more about the program. 

**Saving Data** The program saves data both locally and through an account system. The data is saved locally through CSV files. A seperate file is made for class data and user data (including information in the settings, GPA scale, colors, etc.). At the end of the program, all of this data is added to the file, and the user can access this data by clicking Import Local Data. The account system uses MySQL. A database is defined and throughout the program, data is added and deleted from the database once every two seconds. This also occurs at the end of the program. Like with CSV, all previous data is saved.

**Exporting Data** The program allows the user to export their data through either a PDF or an Excel spreadsheet. The user would enter the Export Data screen, and from there, they would choose the scope of their output report, the class (if applicable), and other information such as their name. From here, a report will be generated in either Excel or in the form of a PDF.


