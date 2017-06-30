import sys
import time

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QPushButton, QLineEdit, QSpacerItem, QSizePolicy
from PyQt5.QtCore import QSize, QTimer

import nrklib

class NRKRipWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        #self.setMinimumSize(QSize(640, 480))
        self.setWindowTitle("NRK Rip")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        grid_layout = QGridLayout(self)
        central_widget.setLayout(grid_layout)

        title = QLabel("URL", self)
        title.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        grid_layout.addWidget(title, 0, 0)

        self.url_text = QLineEdit(self)
        self.url_text.textChanged.connect(self.__url_changed)
        grid_layout.addWidget(self.url_text, 1, 0)

        self.rip_button = QPushButton("Rip", self)
        self.rip_button.clicked.connect(self.__buttonRipClicked)
        grid_layout.addWidget(self.rip_button, 2, 0)

    def __url_changed(self):
        print("URL: " + self.url_text.text())
        # Validate URL (need validation method in NRKLib

    def save_media(self):
        print("Started ripping")
        self.rip_button.setEnabled(False)
        nrklib.save_media(self.url_text.text())
        self.rip_button.setEnabled(True)
        print("Ended ripping")

    def __buttonRipClicked(self):
        #QTimer.singleShot(1, lambda: self.save_media)
        self.save_media()




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = NRKRipWindow()
    mainWin.show()
    sys.exit( app.exec_() )
