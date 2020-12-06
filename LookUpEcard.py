from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt5.QtWidgets import QTableView, QApplication
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


def displayData(tag_number):
    print('processing query...')
    qry = QSqlQuery(db)
    query = 'SELECT * FROM name WHERE ecard = %i OR ecard2 = %i' % (tag_number , tag_number)
    qry.prepare(query)
    qry.exec()

    model = QSqlQueryModel()
    model.setQuery(qry)

    view = QTableView()
    view.setModel(model)
    return view


if __name__ == '__main__':
    app = QApplication(sys.argv)

    if createConnection():

        dataView = displayData(4013934)
        dataView.show()

    app.exit()
    sys.exit(app.exec_())