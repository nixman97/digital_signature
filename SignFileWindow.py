from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, QMessageBox
from PyQt5.uic.Compiler.qtproxies import QtGui

from FileSigner import FileSigner
from Utils import Utils


class SignFileWindow(QDialog):


    def __init__(self, alias):
        super().__init__()
        self.name_alias = alias
        self.file_to_sign_path_label = QLabel("File to be signed:")
        self.file_signed_path_label = QLabel("Output file:           ")
        self.open_unsigned_file_button = QPushButton("Open File")
        self.signed_file_button = QPushButton("Open File")
        self.export_button = QPushButton("Export")
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setIcon(QIcon.fromTheme("window-close"))

        self.open_unsigned_file_button.clicked.connect(self.open_file_unsigned)
        self.signed_file_button.clicked.connect(self.file_save_signed)
        self.cancel_button.clicked.connect(self.cancel_dialog)
        self.export_button.clicked.connect(self.export_signed_file)

        unsigned_layout = QHBoxLayout()
        signed_layout = QHBoxLayout()
        bottom_buttons = QHBoxLayout()
        bottom_buttons.addWidget(self.cancel_button)
        bottom_buttons.addWidget(self.export_button)
        unsigned_layout.addWidget(self.file_signed_path_label)
        unsigned_layout.addWidget(self.signed_file_button)
        signed_layout.addWidget(self.file_to_sign_path_label)
        signed_layout.addWidget(self.open_unsigned_file_button)
        main_layout = QVBoxLayout()
        main_layout.addLayout(unsigned_layout)
        main_layout.addLayout(signed_layout)
        main_layout.addLayout(bottom_buttons)
        self.setLayout(main_layout)
        self.setWindowTitle("Sign")

    def file_save_signed(self):
        self.file_save_path = QFileDialog.getSaveFileName(self, 'Save Signed File')
        self.file_signed_path_label.setText(self.file_signed_path_label.text()+ self.file_save_path[0])

    def open_file_unsigned(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        self.file_open_path, _ = QFileDialog.getOpenFileName(self, "Choose File to Sign", "",
                                                             "All files (*)", options=options)

        self.file_to_sign_path_label.setText(self.file_to_sign_path_label.text()+ self.file_open_path)

    def cancel_dialog(self):
        self.close()

    def export_signed_file(self):
        file_signer = FileSigner()
        signature = file_signer.sign(self.name_alias, self.file_open_path)
        Utils().zip_files(self.file_save_path[0], self.file_open_path,self.name_alias, signature)
        self.close()
