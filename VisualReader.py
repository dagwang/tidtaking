import sys
import json

from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery, QSqlTableModel
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QDataWidgetMapper, QFormLayout, QVBoxLayout, \
    QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QInputDialog, QAction, QStatusBar, QComboBox
from tag_reader import *

#defaultdb = dict( SERVER_NAME = 'GETAC\SQLEXPRESS', DATABASE_NAME = 'Rossignolrennet_2020', USERNAME = 'emit',
#    PASSWORD = 'time')
# Driver={ODBC Driver 13 for SQL Server};Server=tcp:tider.database.windows.net,1433;Database=;Uid=tidtaker;Pwd={your_password_here};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;


class ConnectedReader(QThread, QWidget):

    tag_info = pyqtSignal(dict)
    tag = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        rm = ReaderManager()
        self.reader = rm.connect_first()
        self.reader.set_code(70)

    def run(self):
        while 1:
            info = self.reader.read_tag_when_available()
            self.tag_info.emit(info)
            self.tag.emit(info['tag'])


class SelectFromList(QWidget):
    def __init__(self, selection_list):
        super().__init__()
        layout = QVBoxLayout()
        selection = QComboBox()
        self.setMinimumSize(200, 200)
        selection.addItems(selection_list)
        print(selection_list)
        #self.setCentralWidget(selection)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    unknown_tag = pyqtSignal(str)
    selected_runner = pyqtSignal(int, str)

    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(600, 40))
        menu = self.menuBar()

        database_menu = menu.addMenu("&Database")
        ECU_menu = menu.addMenu("&Brikkeleser")
        set_code_action = QAction("&Sett brikkeleserkode",self)
        set_code_action.triggered.connect(self.set_code)
        select_database_action = QAction("&Velg database",self)
        select_database_action.triggered.connect(self.select_database)
        ECU_menu.addAction(set_code_action)
        database_menu.addAction(select_database_action)

        self.tag_label = QLabel()
        self.reader = ConnectedReader()
        self.reader.tag_info.connect(self.custom_slot)
        self.reader.tag.connect(self.custom_slot2)
        self.reader.tag.connect(self.lookup_tag)
        self.unknown_tag.connect(self.select_runner)
        self.selected_runner.connect(self.confirm_bib_change)
        self.lookup_model = QSqlQueryModel()
        self.lookup_mapper = QDataWidgetMapper()
        self.change_model = QSqlTableModel()
        self.change_mapper = QDataWidgetMapper()
        self.db = QSqlDatabase.addDatabase('QODBC')
        with open('C:\\EMIT\\connection.json', 'r') as f:
            self.current_db = json.load(f)
        self.connect_database()
        form = QFormLayout()
        layout = QVBoxLayout()

        first_name = QLineEdit()
        font = first_name.font()
        font.setPointSize(20)
        first_name.setFont(font)
        last_name = QLineEdit()
        last_name.setFont(font)
        start_number = QLineEdit()
        start_number.setFont(font)
        tag_number = QLineEdit()
        tag_number.setFont(font)
        tag_number_2 = QLineEdit()
        tag_number_2.setFont(font)
        form.addRow(QLabel("Startnummer"), start_number)
        form.addRow(QLabel("Fornavn"), first_name)
        form.addRow(QLabel("Etternavn"), last_name)
        form.addRow(QLabel("Brikke"), tag_number)
        form.addRow(QLabel("Brikke 2"), tag_number_2)
        self.lookup_mapper.setModel(self.lookup_model)
        self.lookup_mapper.addMapping(first_name, 0)
        self.lookup_mapper.addMapping(start_number, 2)
        self.lookup_mapper.addMapping(last_name, 1)
        self.lookup_mapper.addMapping(tag_number, 4)
        self.lookup_mapper.addMapping(tag_number_2, 5)

        layout.addLayout(form)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.reader.start()

    def connect_database(self):
        # Open database
        print(self.current_db)
        connString = f"DRIVER={{SQL Server}};" \
                     f"SERVER={self.current_db['SERVER_NAME']};" \
                     f"UID={self.current_db['USERNAME']};" \
                     f"PWD={self.current_db['PASSWORD']};" \
                     f"DATABASE={self.current_db['DATABASE_NAME']}"

        self.db.setDatabaseName(connString)
        if self.db.open():
            self.setWindowTitle(self.current_db['SERVER_NAME'] + " " +self.current_db['DATABASE_NAME'])
        else:
            print('connection failed')

    def lookup_tag(self, tag_string):
        qry = QSqlQuery(self.db)
        query = 'SELECT name, ename, startno, starttime, ecard, ecard2 FROM name WHERE ecard = %s OR ecard2 = %s' % (tag_string, tag_string)
        qry.prepare(query)
        qry.exec()
        self.lookup_model.setQuery(qry)
        self.lookup_mapper.toFirst()
        if self.lookup_model.rowCount() == 0:
            self.unknown_tag.emit(tag_string)
        print(self.lookup_model.rowCount())

    def select_runner(self, tag_string):
        print('tag:' + tag_string)
        input_dialog = QInputDialog(None)
        input_dialog.setIntMaximum(2000)
        font = input_dialog.font()
        font.setPointSize(20)
        input_dialog.setFont(font)
        input_dialog.setInputMode(QInputDialog.IntInput)
        input_dialog.setWindowTitle('Tilordne ' + tag_string)
        input_dialog.setLabelText('Tilordne til startnummer:')
        done = input_dialog.exec_()
        bib = input_dialog.intValue()
        #bib, done = input_dialog.getInt(self,'Tilordne ' + tag_string, 'Tilordne til startnummer:')
        print('valgt', bib)
        self.selected_runner.emit(bib, tag_string)

    def confirm_bib_change(self, bib, tag_string):
        qry = QSqlQuery(self.db)
        query = 'SELECT name, ename, startno, starttime FROM name WHERE startno = %i ' %(bib)
        print(query)
        qry.prepare(query)
        qry.exec()
        qry.first()
        print(qry.value(0), qry.value(1))
        question = 'Tildele %s til starno %i - %s %s' % (tag_string, bib, qry.value(0), qry.value(1))
        dlg = QMessageBox(self)
        font = dlg.font()
        font.setPointSize(20)
        dlg.setFont(font)
        dlg.setWindowTitle("Brikketildeling")
        dlg.setText(question)
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        button = dlg.exec_()

        if button == QMessageBox.Yes:
            wrqry = 'UPDATE name SET ecard = %s WHERE startno = %i' % (tag_string, bib)
            qry.prepare(wrqry)
            qry.exec()
        else:
            print("No update done")

    def custom_slot(self, a):
        print(a)

    def custom_slot2(self, a):
        print(a)

    def set_code(self):
        print('Write code to set ECU code')

    def select_database(self):
        query=QSqlQuery()
        query.exec_('select name from sys.databases')
        db_list = []
        while query.next():
            db_list.append(query.value(0))
            print(query.value(0))
        print(db_list)
        selection = SelectFromList(db_list)
        selection.show()
        time.sleep(10)



app = QApplication(sys.argv)
window = MainWindow()
window.show()


app.exec_()