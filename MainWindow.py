from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QMessageBox, QTableWidget, \
    QHeaderView, QFileDialog, QInputDialog, QAction, QTableWidgetItem, QSizePolicy, QAbstractItemView, QMainWindow, \
    QMenuBar
from PyQt5.uic.Compiler.qtproxies import QtGui

from FileSigner import FileSigner
from SignFileWindow import SignFileWindow
from Utils import Utils


class MainWindow(QWidget):

    def _callable(self, l):
        print(l)

    def __init__(self, app):
        super().__init__()
        self.app = app

        menubar = QMenuBar()
        main_menu = menubar.addMenu("Menu")
        verify_signature_item = main_menu.addAction("Verify file signature")
        verify_signature_item.triggered.connect(self.dialog_file_to_verify)
        main_menu.addAction("Generate Certificate")
        main_menu.addAction("Import Certificate")
        main_menu.addSeparator()
        main_menu.addAction("Quit")
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("About")

        self.open_file_to_sign = QPushButton("Sign File")
        self.verify_file_signature = QPushButton("Verify Signature")
        self.generate = QPushButton("Generate new keys")
        self.verify_file_signature = QPushButton("Import certificate")

        table_horiz_layout = QHBoxLayout()
        top_button_horiz_layout = QHBoxLayout()
        top_button_horiz_layout.addWidget(self.open_file_to_sign)
        top_button_horiz_layout.addWidget(self.verify_file_signature)
        top_button_horiz_layout.addWidget(self.generate)

        self.verify_file_signature.clicked.connect(self.dialog_file_to_verify)
        self.open_file_to_sign.clicked.connect(self.dialog_file_to_sign)
        self.generate.clicked.connect(self.generate_certificate)
        main_layout = QVBoxLayout()
        self.create_pubkey_table()
        self.create_privkey_table()
        table_horiz_layout.addWidget(self.public_key_table)
        table_horiz_layout.addWidget(self.personal_key_table)

        self.setWindowTitle('RSA Signature')
        main_layout.addWidget(menubar)
        main_layout.addLayout(top_button_horiz_layout)
        main_layout.addLayout(table_horiz_layout)
        self.setLayout(main_layout)

        self.show()

    def spin_button_callback(self):
        print("PUSHED")

    def create_pubkey_table(self):
        self.public_key_table = QTableWidget()
        # Column count
        self.public_key_table.setColumnCount(1)
        self.public_key_table.setHorizontalHeaderLabels("Known public keys".split(";"))
        # Table will fit the screen horizontally
        self.public_key_table.horizontalHeader().setStretchLastSection(True)
        self.public_key_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.public_key_table.setShowGrid(False)
        self.public_key_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.public_key_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.refresh_data_in_pubkey_table()

    def refresh_data_in_pubkey_table(self):
        self.public_key_table.setRowCount(0)
        for i in FileSigner().get_pub_keys():
            self.public_key_table.insertRow(self.public_key_table.rowCount())
            self.public_key_table.setItem(self.public_key_table.rowCount() - 1, 0, QTableWidgetItem(i[0]))

    def create_privkey_table(self):
        self.personal_key_table = QTableWidget()
        self.personal_key_table.setColumnCount(1)
        self.personal_key_table.setHorizontalHeaderLabels("My keys/certificates".split(";"))
        self.personal_key_table.setShowGrid(False)
        self.personal_key_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.personal_key_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.personal_key_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.refresh_data_in_privkey_table()

    def refresh_data_in_privkey_table(self):
        self.personal_key_table.setRowCount(0)
        for i in FileSigner().get_my_keys():
            self.personal_key_table.insertRow(self.personal_key_table.rowCount())
            self.personal_key_table.setItem(self.personal_key_table.rowCount() - 1, 0, QTableWidgetItem(i[0]))

    def dialog_file_to_verify(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose file to check signature for...", "",
                                                   "All Files (*)", options=options)
        if file_path:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Verification result")
            msg_box.setStandardButtons(QMessageBox.Ok)

            result = FileSigner().verify_signature(file_path)
            if result!=2 and result:

                msg_box.setIcon(QMessageBox.Information)
                msg_box.setText("File has been signed by "+result)
                msg_box.exec()
            if not(result):

                msg_box.setIcon(QMessageBox.Critical)
                msg_box.setText("WARNING!!! DO NOT TRUST!!! Signature check failed. File has been modified!")
                msg_box.exec()
            if result==2:
                msg_box = QMessageBox.question(self, 'Verification result', "This public key does not exist in your trusted set."
                                "Importing it is a very dangerous thing if you do not know the key, or you are not sure whom this key "
                                "belongs to, as someone may have tampered with the file on it's way. Do you want to import it?"+ open("temp/pkey.key").read(),
                                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if msg_box == QMessageBox.Yes:
                    alias, ok = QInputDialog.getText(self, 'Public Key Alias',
                                                    'Enter alias:')

                    if ok:
                        FileSigner().import_public_key("temp/pkey.key",alias)
                        self.refresh_data_in_pubkey_table()
                        result = FileSigner().verify_signature(file_path)
                        if result==False:
                            msg_box.setText(
                                "WARNING!!! DO NOT TRUST!!! Signature check failed. File has been modified! The key remains imported. If you wish, you can delete it manually")
                        else:
                            msg_box = QMessageBox()
                            msg_box.setWindowTitle("Verification result")
                            msg_box.setStandardButtons(QMessageBox.Ok)
                            msg_box.setIcon(QMessageBox.Information)
                            msg_box.setText("File has been signed by " + result+"(The newly added key)")
                            msg_box.exec()
                else:
                    print('No clicked.')


    def dialog_file_to_sign(self):
        try:
            selected_key = self.personal_key_table.selectedItems()[0].text()
            signed_file_window = SignFileWindow(selected_key)
            signed_file_window.setModal(True)
            signed_file_window.exec()
        except:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText("Please select a key to use for signing!")
            msg_box.setWindowTitle("No key selected")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()

    def generate_certificate(self):
        text, ok = QInputDialog.getText(self, 'Key pair Alias',
                                        'Enter alias:')

        if ok:
            FileSigner().generate_new_key(text)
            self.refresh_data_in_privkey_table()
