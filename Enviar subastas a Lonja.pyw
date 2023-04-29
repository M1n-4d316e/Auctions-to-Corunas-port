import pip


# Import or install packages
def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])


import_or_install('PySide6')
import_or_install('requests')
import_or_install('json')
import_or_install('datetime')

from PySide6.QtCore import QDate
import sys
import petitions
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QFileDialog, QMessageBox, QDateEdit


class Main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # Create the UI
        self.setWindowTitle("Enviar subastas a Lonja")
        self.create_window()
        self.button1.setEnabled(False)
        self.button2.setEnabled(False)
        self.button3.setEnabled(False)
        self.date_edit.setEnabled(False)
        self.button1.clicked.connect(self.button1_clicked)
        self.button2.clicked.connect(self.button2_clicked)
        self.button3.clicked.connect(self.button3_clicked)
        self.login(None)

    @QtCore.Slot()
    def import_xml(self):
        # open XML file
        file_path, _ = QFileDialog.getOpenFileName(None, 'Abrir archivo ...', '', 'XML (*.xml)')

        if file_path:
            with open(file_path, 'r') as XML:
                return XML.read()

    def create_window(self):
        # Create the UI
        self.dialog = None
        self.text3 = QtWidgets.QLabel("Bienvenido.",
                                      alignment=QtCore.Qt.AlignCenter)
        self.button1 = QtWidgets.QPushButton("Enviar subastas a Lonja")
        self.button2 = QtWidgets.QPushButton("Descargar precarga de datos segun fecha")
        self.button3 = QtWidgets.QPushButton("Descargar los compradores")
        self.line = QtWidgets.QFrame()
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setMinimumHeight(20)
        self.line2 = QtWidgets.QFrame()
        self.line2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line2.setMinimumHeight(20)
        self.date_edit = QDateEdit(self)
        self.date_edit.setDate(QDate.currentDate())
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text3)
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.line)
        self.layout.addWidget(self.date_edit)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.line2)
        self.layout.addWidget(self.button3)

    def login(self, s):
        message, x = petitions.login()

        if x:
            self.text3.setText(message)
            self.button1.setEnabled(True)
            self.button2.setEnabled(True)
            self.button3.setEnabled(True)
            self.date_edit.setEnabled(True)
        else:
            QMessageBox.information(
                self,
                "Atención",
                message
            )

    def button1_clicked(self, s):
        message = petitions.sendauction(self.import_xml())

        QMessageBox.information(
            self,
            "Atención",
            message
        )

    def button2_clicked(self, s):
        message = petitions.preloadbydate(self.date_edit.date().toString("yyyy-MM-dd"))

        QMessageBox.information(
            self,
            "Atención",
            message
        )

    def button3_clicked(self, s):

        message = petitions.downloadbuyers()

        QMessageBox.information(
            self,
            "Atención",
            message
        )


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Main()
    widget.resize(100, 100)
    widget.show()

    sys.exit(app.exec())
