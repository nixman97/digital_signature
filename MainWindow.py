from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QMessageBox, QTableWidget, \
    QHeaderView, QFileDialog, QInputDialog, QAction, QTableWidgetItem, QSizePolicy, QAbstractItemView

from FileSigner import FileSigner


class MainWindow(QWidget):

    def _callable(self, l):
        print(l)

    def crete_menu_bar(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(QAction(QIcon('new.png'), '&New', self))

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.open_file_to_sign = QPushButton("Sign File")
        self.verify_file_signature = QPushButton("Verify Signature")
        self.generate = QPushButton("Generate certificate")
        self.verify_file_signature = QPushButton("Import certificate")

        table_horiz_layout = QHBoxLayout()
        top_button_horiz_layout = QHBoxLayout()
        top_button_horiz_layout.addWidget(self.open_file_to_sign)
        top_button_horiz_layout.addWidget(self.verify_file_signature)
        top_button_horiz_layout.addWidget(self.generate)

        self.verify_file_signature.clicked.connect(self.dialog_file_to_verify)
        self.generate.clicked.connect(self.generate_certificate)
        main_layout = QVBoxLayout()
        self.create_pubkey_table()
        self.create_privkey_table()
        table_horiz_layout.addWidget(self.public_key_table)
        table_horiz_layout.addWidget(self.private_key_table)

        self.setWindowTitle('RSA Signature')

        main_layout.addLayout(top_button_horiz_layout)
        main_layout.addLayout(table_horiz_layout)
        self.setLayout(main_layout)

        self.show()

    def spin_button_callback(self):
        print("PUSHED")

    def create_pubkey_table(self):
        self.public_key_table = QTableWidget()
        # Column count
        self.public_key_table.setColumnCount(2)
        self.public_key_table.setHorizontalHeaderLabels("Alias;Key".split(";"))
        # Table will fit the screen horizontally
        self.public_key_table.horizontalHeader().setStretchLastSection(True)
        self.public_key_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.refresh_data_in_pubkey_table()
    def refresh_data_in_pubkey_table(self):
        self.public_key_table.setRowCount(0)
        for i in FileSigner().get_pub_keys():
            self.public_key_table.insertRow(self.public_key_table.rowCount())
            self.public_key_table.setItem(self.public_key_table.rowCount() - 1, 0, i[0])
            self.public_key_table.setItem(self.public_key_table.rowCount() - 1, 1, i[1])

    def create_privkey_table(self):
        self.private_key_table = QTableWidget()
        self.private_key_table.setColumnCount(2)
        self.private_key_table.setHorizontalHeaderLabels("Alias;Key".split(";"))
        self.private_key_table.setShowGrid(False)
        self.private_key_table.horizontalHeader().setSectionResizeMode()
        self.private_key_table.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.private_key_table.horizontalHeader().setStretchLastSection(True)
        self.private_key_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.refresh_data_in_privkey_table()
    def refresh_data_in_privkey_table(self):
        self.private_key_table.setRowCount(0)
        for i in FileSigner().get_my_keys():
            self.private_key_table.insertRow(self.private_key_table.rowCount())
            self.private_key_table.setItem(self.private_key_table.rowCount() - 1, 0, QTableWidgetItem(i[0]))
            self.private_key_table.setItem(self.private_key_table.rowCount() - 1, 1, QTableWidgetItem(i[1]))

    def dialog_file_to_verify(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose file to check signature for...", "",
                                                   "All Files (*)", options=options)
        if file_path:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText(FileSigner().verify_signature(file_path))
            msg_box.setWindowTitle("QMessageBox Example")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()

    def dialog_file_to_sign(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose file to check signature for...", "",
                                                   "All Files (*)", options=options)
        if file_path:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText(FileSigner().verify_signature(file_path))
            msg_box.setWindowTitle("QMessageBox Example")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()

    def generate_certificate(self):
        text, ok = QInputDialog.getText(self, 'Certificate Alias',
                                        'Enter certificate alias:')

        if ok:
            FileSigner().generate_new_key(text)
            self.refresh_data_in_privkey_table()