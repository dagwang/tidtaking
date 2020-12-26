import sys

from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from tag_reader import *


class ConnectedReader(QThread, QWidget):

    tag_info = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        rm = ReaderManager()
        self.reader = rm.connect_first()

    def run(self):
        while 1:
            info = self.reader.read_tag_when_available()
            self.tag_info.emit(info)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.reader = ConnectedReader()
        self.reader.tag_info.connect(self.custom_slot)
        self.reader.start()

    def custom_slot(self, a):
        print(a)


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec_()