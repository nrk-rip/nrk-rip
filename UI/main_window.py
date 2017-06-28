import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QPushButton, QLineEdit, QSpacerItem, QSizePolicy
from PyQt5.QtCore import QSize


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

        url_text = QLineEdit(self)
        grid_layout.addWidget(url_text, 1, 0)

        button = QPushButton("Rip", self)
        grid_layout.addWidget(button, 2, 0)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = NRKRipWindow()
    mainWin.show()
    sys.exit( app.exec_() )
