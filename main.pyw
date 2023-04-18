import sys
import petitions
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QFileDialog, QMessageBox


class Main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # Create the UI
        self.setWindowTitle("Enviar subastas a Lonja de A Coruña")
        self.create_window()
        self.button1.setEnabled(False)
        self.button2.setEnabled(False)
        self.button0.clicked.connect(self.button0_clicked)
        self.button1.clicked.connect(self.button1_clicked)
        self.button2.clicked.connect(self.button3_clicked)

    @QtCore.Slot()
    def import_xml(self):
        # open XML file
        file_path, _ = QFileDialog.getOpenFileName(
            None, 'Abrir archivo ...', '', 'XML (*.xml)')

        if file_path:
            with open(file_path, 'r') as XML:
                return XML

    def create_window(self):
        # Create the UI
        self.dialog = None
        self.text3 = QtWidgets.QLabel("Bienvenido.",
                                      alignment=QtCore.Qt.AlignCenter)
        self.button0 = QtWidgets.QPushButton("Iniciar sesión")
        self.button1 = QtWidgets.QPushButton("Importar XML de subastas")
        self.button2 = QtWidgets.QPushButton("Descargar precarga de datos")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text3)
        self.layout.addWidget(self.button0)
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)

    def button0_clicked(self, s):
        message, x = petitions.login()

        QMessageBox.information(
            self,
            "Atención",
            message
        )

        if x:
            self.button0.setEnabled(False)
            self.button1.setEnabled(True)
            self.button2.setEnabled(True)

    def button1_clicked(self, s):
        message = petitions.sendauction(self.import_xml())

        QMessageBox.information(
            self,
            "Atención",
            message
        )

    def button3_clicked(self, s):
        message = petitions.preloadbydate()

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
