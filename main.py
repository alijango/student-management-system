from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, \
    QDialog, QVBoxLayout, QComboBox
import sys
import sqlite3


class MainWindows(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Student Management System")

        file_menu_item = self.menuBar().addMenu('&File')
        help_menu_item = self.menuBar().addMenu('&Help')
        edit_menu_item = self.menuBar().addMenu('&Edit')

        add_student_action = QAction('Add Student', self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction('About', self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        search_action = QAction('Search', self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('Id', 'Name', 'Course', 'Mobile'))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):
        connection = sqlite3.connect('database.db')
        result = connection.execute("SELECT * FROM students")
        # This line code below it to prevent overwrite data so it set row to zero after loop
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    @staticmethod
    def insert():
        dialog = InsertDialog()
        dialog.exec()

    @staticmethod
    def search():
        search = SearchDialogs()
        search.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Insert New Student')
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText('Name')

        self.course = QComboBox()
        items = ['Math', 'Astronomy', 'Biology', 'Physics']
        self.course.addItems(items)

        self.mobile_number = QLineEdit()
        self.mobile_number.setPlaceholderText('Phone Number')

        submit = QPushButton('Submit')
        submit.clicked.connect(self.save_data)

        layout.addWidget(self.student_name)
        layout.addWidget(self.course)
        layout.addWidget(self.mobile_number)
        layout.addWidget(submit)

        self.setLayout(layout)
    # You use method properties when you want to adjust and instance variable
    # like example below

    @property
    def the_student_name(self):
        name = self.student_name.text().strip()
        name = name.title()
        return name

    def save_data(self):
        name = self.the_student_name
        print(name)
        # two ways of course down is correct
        #course = self.course.itemText(self.course.currentIndex())
        course = self.course.currentText()
        mobile = self.mobile_number.text()
        print(name)
        print(course)
        print(mobile)
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query = """ INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)
        """

        data_to_insert = (name.title(), course, mobile)
        cursor.execute(query, data_to_insert)
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


class SearchDialogs(QDialog):
    def __init__(self):
        super().__init__()
        # Set window title and size
        self.setWindowTitle('Search Student')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # Create layout and input widget
        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)

        # Create button
        button = QPushButton('Search')
        button.clicked.connect(self.search_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def search_student(self):
        name = self.student_name.text()
        name = name.title()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name =?", (name, ))
        print(result)
        rows = list(result)
        print(rows)
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item.row())
            main_window.table.item(item.row(), 1).setSelected(True)


app = QApplication(sys.argv)
main_window = MainWindows()
main_window.show()
main_window.load_data()
name_dialog = InsertDialog()
#print(name_dialog.the_student_names)
print(name_dialog.the_student_name)
sys.exit(app.exec())
