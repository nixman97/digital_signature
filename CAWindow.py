from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QFileDialog, QVBoxLayout, QDialog, QLineEdit

from FileSigner import FileSigner
from Utils import Utils


class CAWindow(QDialog):


    def __init__(self):
        super().__init__()

        self.ca_bundle_label = QLabel("CA Bundle: ")
        self.private_key_label = QLabel("Private key:")
        self.certificate_file_label = QLabel("Certificate file: ")
        self.alias_label= QLabel("Alias")
        self.line_edit_alias = QLineEdit()

        self.open_CA_file_button = QPushButton("Open File")
        self.open_private_key_button = QPushButton("Open File")
        self.open_certificate_button = QPushButton("Open File")
        self.import_button = QPushButton("Import")
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setIcon(QIcon.fromTheme("window-close"))

        self.open_CA_file_button.clicked.connect(self.open_CA_file)
        self.open_private_key_button.clicked.connect(self.open_private_key_file)
        self.open_certificate_button.clicked.connect(self.open_certificate_file)

        self.cancel_button.clicked.connect(self.cancel_dialog)
        self.import_button.clicked.connect(self.import_cert)

        certificate_layout = QHBoxLayout()
        CA_layout = QHBoxLayout()
        alias_layout = QHBoxLayout()
        private_layout = QHBoxLayout()
        bottom_buttons = QHBoxLayout()
        bottom_buttons.addWidget(self.cancel_button)
        bottom_buttons.addWidget(self.import_button)
        certificate_layout.addWidget(self.certificate_file_label)
        certificate_layout.addWidget(self.open_certificate_button)
        CA_layout.addWidget(self.ca_bundle_label)
        CA_layout.addWidget(self.open_CA_file_button)
        alias_layout.addWidget(self.alias_label)
        alias_layout.addWidget(self.line_edit_alias)
        private_layout.addWidget(self.private_key_label)
        private_layout.addWidget(self.open_private_key_button)
        main_layout = QVBoxLayout()
        main_layout.addLayout(certificate_layout)
        main_layout.addLayout(CA_layout)
        main_layout.addLayout(private_layout)
        main_layout.addLayout(alias_layout)
        main_layout.addLayout(bottom_buttons)

        self.setLayout(main_layout)
        self.setWindowTitle("Sign")

    def open_private_key_file(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        self.private_path, _ = QFileDialog.getOpenFileName(self, "Choose private key file", "",
                                                             "Key file (*.key)", options=options)
        self.private_key_label.setText(self.private_key_label.text()+self.private_path)
    def open_certificate_file(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        self.certificate_path, _ = QFileDialog.getOpenFileName(self, "Choose Certificate file", "",
                                                             "Certificate file (*.crt)", options=options)
        self.certificate_file_label.setText(self.certificate_file_label.text() + self.certificate_path)
    def open_CA_file(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        self.CA_path, _ = QFileDialog.getOpenFileName(self, "Choose CA file", "",
                                                             "CA file (*.crt)", options=options)

        self.ca_bundle_label.setText(self.ca_bundle_label.text() + self.CA_path)

    def cancel_dialog(self):
        self.close()

    def import_cert(self):
        file_signer = FileSigner()
        file_signer.import_certificate(self.CA_path,self.private_path,self.certificate_path,self.line_edit_alias.text())
        self.close()
