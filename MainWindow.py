from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QMessageBox, QTableWidget, \
    QHeaderView, QFileDialog, QInputDialog, QAction, QTableWidgetItem, QSizePolicy, QAbstractItemView, QMainWindow, \
    QMenuBar, QLineEdit
from PyQt5.uic.Compiler.qtproxies import QtGui

from CAWindow import CAWindow
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
        main_menu = menubar.addMenu("Sign")
        pass_menu = menubar.addMenu("Password")
        self.remove_password_item = pass_menu.addAction("Remove password")
        self.remove_password_item.triggered.connect(self.remove_pass)
        self.set_password_item = pass_menu.addAction("Set password")
        self.set_password_item.triggered.connect(self.set_new_pass)
        cancel=False
        if Utils().check_pass_set():
            self.set_password_item.setDisabled(True)

            good=False

            while not(good):
                text, ok = QInputDialog.getText(self, 'Password',
                                                'Enter password:', QLineEdit.Password)
                if ok:
                    if Utils().check_pass_set():
                        if Utils().is_password_good(text):
                            good=True
                else:
                    good=True
                    cancel=True
        else:
            self.remove_password_item.setDisabled(True)



        verify_signature_item = main_menu.addAction("Verify file signature")
        verify_signature_item.triggered.connect(self.dialog_file_to_verify)
        import_ca_cert = main_menu.addAction("Import CA Certificate")
        file_sign = main_menu.addAction("Sign File")
        file_sign.triggered.connect(self.dialog_file_to_sign)
        import_ca_cert.triggered.connect(self.import_certs)
        main_menu.addSeparator()
        quit_action = main_menu.addAction("Quit")
        quit_action.triggered.connect(self.exit_app)

        help_menu = menubar.addMenu("Help")
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about)
        self.open_file_to_sign = QPushButton("Sign File")
        self.generate = QPushButton("Generate new key pair")
        self.remove_my_key_button = QPushButton("Remove")
        self.remove_public_key_button = QPushButton("Remove")
        self.update_my_key_button = QPushButton("Update")
        self.update_public_key_button = QPushButton("Update")
        table_horiz_layout1 = QVBoxLayout()
        table_horiz_layout2 = QVBoxLayout()

        top_button_horiz_layout_1 = QHBoxLayout()
        top_button_horiz_layout_2 = QHBoxLayout()

        top_button_horiz_layout_1.addWidget(self.remove_public_key_button)
        top_button_horiz_layout_2.addWidget(self.generate)
        top_button_horiz_layout_2.addWidget(self.remove_my_key_button)
        self.open_file_to_sign.clicked.connect(self.dialog_file_to_sign)
        self.generate.clicked.connect(self.generate_certificate)
        self.remove_my_key_button.clicked.connect(self.remove_my_key)
        self.remove_public_key_button.clicked.connect(self.remove_public_key)
        self.update_my_key_button.clicked.connect(self.update_my_key)
        self.update_public_key_button.clicked.connect(self.update_public_key)

        main_layout = QVBoxLayout()
        self.create_pubkey_table()
        self.create_privkey_table()
        table_horiz_layout1.addLayout(top_button_horiz_layout_1)
        table_horiz_layout1.addWidget(self.public_key_table)
        table_horiz_layout2.addLayout(top_button_horiz_layout_2)
        table_horiz_layout2.addWidget(self.personal_key_table)
        top_button_horiz_layout_2.addWidget(self.update_my_key_button)
        top_button_horiz_layout_1.addWidget(self.update_public_key_button)

        self.setWindowTitle('RSA Signature')
        main_layout.addWidget(menubar)

        wind_layout = QHBoxLayout()
        wind_layout.addLayout(table_horiz_layout1)
        wind_layout.addLayout(table_horiz_layout2)
        main_layout.addLayout(wind_layout)
        self.setLayout(main_layout)
        self.show()
        if cancel:
            self.exit_app()

    def exit_app(self):
        self.close()

    def set_new_pass(self):
        text, ok = QInputDialog.getText(self, 'Password',
                                        'Enter password:', QLineEdit.Password)
        if ok:
            Utils().set_passkey(text)
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText(
                "All your private keys are and will be encrypted")
            msg_box.setWindowTitle("Password")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()
            self.set_password_item.setDisabled(True)
            self.remove_password_item.setDisabled(False)

    def remove_pass(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText(
            "All your private keys are and will no longer be encrypted")
        msg_box.setWindowTitle("Password")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()
        Utils().remove_passkey()
        self.remove_password_item.setDisabled(True)
        self.set_password_item.setDisabled(False)

    def spin_button_callback(self):
        print("PUSHED")

    def show_about(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(
            "This software is developed by Victor Pogacean and Maria Boian. Licensed unde GPL v3.0. Thank you for your choice")
        msg_box.setWindowTitle("About")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

    def remove_my_key(self):
        try:
            selected_key = self.personal_key_table.selectedItems()[0].text()
            FileSigner().remove_my_key(selected_key)
            self.refresh_data_in_privkey_table()
        except:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText("Please select an item to delete")
            msg_box.setWindowTitle("No item selected")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()

    def remove_public_key(self):
        try:
            selected_key = self.public_key_table.selectedItems()[0].text()
            FileSigner().remove_public_key(selected_key)
            self.refresh_data_in_pubkey_table()
        except:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText("Please select an item to delete")
            msg_box.setWindowTitle("No item selected")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()

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

            fnt = QFont()
            fnt.setPointSize(10)
            fnt.setFamily("Arial Black")
            self.personal_key_table.insertRow(self.personal_key_table.rowCount())
            item = QTableWidgetItem(i[0][1:])
            if i[0][0] == "C":
                item.setFont(fnt)
            self.personal_key_table.setItem(self.personal_key_table.rowCount() - 1, 0, item)

    def import_certs(self):
        signed_file_window = CAWindow()
        signed_file_window.setModal(True)
        signed_file_window.exec()
        self.refresh_data_in_privkey_table()

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

            if result != 2 and result:

                msg_box.setIcon(QMessageBox.Information)
                try:
                    msg_box.setText("File has been signed by " + result)
                except:
                    if result[1] == "11":
                        msg_box.setText(
                            "File has been signed by " + str(result[0][0]) + " using a certificate issued by " + str(
                                result[0][1]))
                    if result[1] == "01":
                        msg_box.setIcon(QMessageBox.Warning)
                        msg_box.setText(
                            "Warning! File has been signed by " + str(
                                result[0][0]) + " using a certificate issued by " + str(
                                result[0][1]) + ", but the root CA is NOT TRUSTED by your system ")
                    if result[1] == "00":
                        msg_box.setIcon(QMessageBox.Critical)
                        msg_box.setText(
                            "Warning! File has been signed by " + str(
                                result[0][0]) + " using a certificate issued by " + str(
                                result[0][
                                    1]) + ", but the root CA is NOT TRUSTED by your system. Certificate is expired")
                    if result[1] == "00":
                        msg_box.setIcon(QMessageBox.Critical)
                        msg_box.setText(
                            "Warning! File has been signed by " + str(
                                result[0][0]) + " using a certificate issued by " + str(
                                result[0][1]) + ". Certificate is expired")
                msg_box.exec()
            if not (result):
                msg_box.setIcon(QMessageBox.Critical)
                msg_box.setText("WARNING!!! DO NOT TRUST!!! Signature check failed. File has been modified!")
                msg_box.exec()
            if result == 2:
                msg_box = QMessageBox.question(self, 'Verification result',
                                               "This public key does not exist in your trusted set."
                                               "Importing it is a very dangerous thing if you do not know the key, or you are not sure whom this key "
                                               "belongs to, as someone may have tampered with the file on it's way. Do you want to import it?" + open(
                                                   "temp/pkey.key").read(),
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if msg_box == QMessageBox.Yes:
                    alias, ok = QInputDialog.getText(self, 'Public Key Alias',
                                                     'Enter alias:')

                    if ok:
                        FileSigner().import_public_key("temp/pkey.key", alias)
                        self.refresh_data_in_pubkey_table()
                        result = FileSigner().verify_signature(file_path)
                        if result == False:
                            msg_box = QMessageBox()
                            msg_box.setWindowTitle("Verification result")
                            msg_box.setStandardButtons(QMessageBox.Ok)
                            msg_box.setIcon(QMessageBox.Critical)
                            msg_box.setText(
                                "WARNING!!! DO NOT TRUST!!! Signature check failed. File has been modified! The key remains imported. If you wish, you can delete it manually")
                            msg_box.exec()

                    else:
                        msg_box = QMessageBox()
                        msg_box.setWindowTitle("Verification result")
                        msg_box.setStandardButtons(QMessageBox.Ok)
                        msg_box.setIcon(QMessageBox.Information)
                        msg_box.setText("File has been signed by " + result[0] + "(The newly added key)")
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

    def update_my_key(self):
        text, ok = QInputDialog.getText(self, 'New key Name',
                                        'Enter new key name:')

        if ok:
            try:
                FileSigner().update_my_key(text, self.personal_key_table.selectedItems()[0].text())
            except:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setText("Please select a key update")
                msg_box.setWindowTitle("No key selected")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec()
            self.refresh_data_in_privkey_table()

    def update_public_key(self):
        text, ok = QInputDialog.getText(self, 'New key Name',
                                        'Enter new key name:')

        if ok:
            try:
                FileSigner().update_public_key(text, self.public_key_table.selectedItems()[0].text())
            except:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setText("Please select a key update")
                msg_box.setWindowTitle("No key selected")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec()
            self.refresh_data_in_pubkey_table()
