import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from tag_reader import *


class ConnectedReader(QWidget):

    tag_info = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        rm = ReaderManager()
        reader = rm.connect_first()
        for ii in range(2):
            info = reader.read_tag_when_available()
            self.tag_info.emit(info)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.reader = ConnectedReader()
        self.reader.tag_info.connect(self.custom_slot)

    def custom_slot(self, a):
        print(a)


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec_()