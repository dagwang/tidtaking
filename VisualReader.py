import sys

from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery, QSqlTableModel
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QDataWidgetMapper, QFormLayout, QVBoxLayout, \
    QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QInputDialog
from tag_reader import *

SERVER_NAME = 'GETAC\SQLEXPRESS'
DATABASE_NAME = 'Rossignolrennet_2020'
USERNAME = 'emit'
PASSWORD = 'time'
connString = f'DRIVER={{SQL Server}};' \
             f'SERVER={SERVER_NAME};' \
             f'USERNAME={USERNAME};' \
             f'PASSWORD={PASSWORD};' \
             f'DATABASE={DATABASE_NAME}'

class ConnectedReader(QThread, QWidget):

    tag_info = pyqtSignal(dict)
    tag = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        rm = ReaderManager()
        self.reader = rm.connect_first()

    def run(self):
        while 1:
            info = self.reader.read_tag_when_available()
            self.tag_info.emit(info)
            self.tag.emit(info['tag'])


class MainWindow(QMainWindow):
    unknown_tag = pyqtSignal(str)
    selected_runner = pyqtSignal(int, str)

    def __init__(self):
        super().__init__()
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

        form = QFormLayout()
        layout = QVBoxLayout()

        first_name = QLineEdit()
        start_number = QLineEdit()
        form.addRow(QLabel("Startnummer"), start_number)
        form.addRow(QLabel("Fornavn"), first_name)
        self.lookup_mapper.setModel(self.lookup_model)
        self.lookup_mapper.addMapping(first_name, 0)
        self.lookup_mapper.addMapping(start_number, 2)

        layout.addLayout(form)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        # Open database
        self.db = QSqlDatabase.addDatabase('QODBC')
        self.db.setDatabaseName(connString)
        if self.db.open():
            print('connect to SQL Server successfully')
        else:
            print('connection failed')

        self.reader.start()

    def lookup_tag(self, tag_string):
        qry = QSqlQuery(self.db)
        query = 'SELECT name, ename, startno, starttime FROM name WHERE ecard = %s OR ecard2 = %s' % (tag_string, tag_string)
        qry.prepare(query)
        qry.exec()
        self.lookup_model.setQuery(qry)
        self.lookup_mapper.toFirst()
        if self.lookup_model.rowCount() == 0:
            self.unknown_tag.emit(tag_string)
        print(self.lookup_model.rowCount())

    def select_runner(self, tag_string):
        print('tag:' + tag_string)
        bib, done = QInputDialog.getInt(self,'Tilordne ' + tag_string, 'Tilordne til startnummer:')
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



app = QApplication(sys.argv)
window = MainWindow()
window.show()


app.exec_()