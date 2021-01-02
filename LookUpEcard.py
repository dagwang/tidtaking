import time

from PyQt5.QtCore import QLine
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt5.QtWidgets import (
    QTableView, QApplication, QDataWidgetMapper, QFormLayout,
    QComboBox, QHBoxLayout, QVBoxLayout, QWidget, QMainWindow, QLabel, QSpinBox, QLineEdit
)

import sys

SERVER_NAME = 'GETAC\SQLEXPRESS'
DATABASE_NAME = 'Rossignolrennet_2020'
USERNAME = 'emit'
PASSWORD = 'time'


def createConnection():
    connString = f'DRIVER={{SQL Server}};' \
                 f'SERVER={SERVER_NAME};' \
                 f'USERNAME={USERNAME};' \
                 f'PASSWORD={PASSWORD};' \
                 f'DATABASE={DATABASE_NAME}'

    global db
    db = QSqlDatabase.addDatabase('QODBC')
    db.setDatabaseName(connString)

    if db.open():
        print('connect to SQL Server successfully')
        return True
    else:
        print('connection failed')
        return False


class displayData(QMainWindow):
    def __init__(self, tag_number):
        super().__init__()
        print('processing query...')
        qry = QSqlQuery(db)
        query = 'SELECT name, ename, startno, starttime FROM name WHERE ecard = %i OR ecard2 = %i' % (tag_number , tag_number)
        qry.prepare(query)
        qry.exec()

        model = QSqlQueryModel()
        model.setQuery(qry)
        print(model.rowCount())
        mapper = QDataWidgetMapper()
        form = QFormLayout()
        layout = QVBoxLayout()

        first_name = QLineEdit()
        start_number = QLineEdit()
        form.addRow(QLabel("Startnummer"), start_number)
        form.addRow(QLabel("Fornavn"), first_name)
        mapper.setModel(model)
        mapper.addMapping(first_name, 0)
        mapper.addMapping(start_number, 2)
        mapper.toFirst()
        layout.addLayout(form)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        #controls = QHBoxLayout()

        '''
        view = QTableView()
        view.setModel(model)
        view.show()
        time.sleep(20)
        '''



if __name__ == '__main__':
    app = QApplication(sys.argv)

    if createConnection():

        dataView = displayData(4013934)
        dataView.show()

    app.exit()
    sys.exit(app.exec_())