import os
import random
import shutil
import rsa

import struct
from os.path import basename
from zipfile import ZipFile
import pyAesCrypt
import io
from Crypto.Cipher import AES

from Sha256 import Sha256


class Utils:
    password = ""

    def zip_files(self, name, file_path, alias, signature):
        zip_obj = ZipFile(name, 'w')
        zip_obj.write(file_path, basename(file_path))
        open("signature", 'wb').write(signature)
        zip_obj.write(os.path.abspath("signature"), "signature")
        if os.path.exists("MyKeys/" + alias + "_publickey.key"):
            zip_obj.write(os.path.abspath("MyKeys/" + alias + "_publickey.key"), "pkey.key")
        else:
            zip_obj.write(os.path.abspath("MyKeys/" + alias + "_certificate.crt"), "certificate.crt")
            zip_obj.write(os.path.abspath("MyKeys/" + alias + "_ca_bundle.crt"), "ca_bundle.crt")

        zip_obj.close()
        os.remove("signature")

    def unzip_files(self, zip_file_path):
        os.system("rm temp/*")
        zip_obj = ZipFile(zip_file_path, 'r')
        zip_obj.extractall('temp')
        zip_obj.close()

    def encrypt_file(self, in_filename):
        if Utils.password == "":
            return
        bufferSize = 64 * 1024
        password = Utils.password

        # binary data to be encrypted

        pbdata = open(in_filename, 'rb').read()

        # input plaintext binary stream
        fIn = io.BytesIO(pbdata)

        # initialize ciphertext binary stream
        fCiph = io.BytesIO()

        # initialize decrypted binary stream
        fDec = io.BytesIO()

        # encrypt stream
        pyAesCrypt.encryptStream(fIn, fCiph, password, bufferSize)

        # print encrypted data
        print("This is the ciphertext:\n" + str(fCiph.getvalue()))
        l = open(in_filename, 'wb')
        l.write(fCiph.getvalue())
        l.close()

    def decrypt_file(self, in_filename):
        if Utils.password=="":
            return open(in_filename, 'rb').read()
        f_dec = io.BytesIO()
        buffer_size = 64 * 1024
        try:
            pyAesCrypt.decryptStream(io.BytesIO(open(in_filename, 'rb').read()), f_dec, Utils.password, buffer_size,
                                     1991)

        except:
            f_dec.seek(0)
            pyAesCrypt.decryptStream(io.BytesIO(open(in_filename, 'rb').read()), f_dec, Utils.password, buffer_size,
                                     2007)
        return f_dec.getvalue()

    def file_encrypted(self, file_path):
        try:
            open(file_path, 'r').read()
            return False
        except:
            return True

    def encypt_all(self):
        for filename in os.listdir("MyKeys"):
            if filename.__contains__("privkey.key"):
                key_entry = ""
                if not (self.file_encrypted("MyKeys/" + filename)):
                    self.encrypt_file("MyKeys/" + filename)

    def decrypt_all(self):
        for filename in os.listdir("MyKeys"):
            if filename.__contains__("privkey.key"):
                if (self.file_encrypted("MyKeys/" + filename)):
                    decrypted = self.decrypt_file("MyKeys/" + filename)
                    os.remove("MyKeys/" + filename)
                    open("MyKeys/" + filename, 'wb').write(decrypted)

    def set_passkey(self, key):
        open("pass", 'w').write("T")
        Utils.password = key
        self.encrypt_file("pass")

        self.encypt_all()

    def remove_passkey(self):
        os.remove("pass")
        self.decrypt_all()
        Utils.password=""

    def check_pass_set(self):
        if (os.path.exists("pass")):
            return True
        return False

    def is_password_good(self,password):
        f_dec = io.BytesIO()
        buffer_size = 64 * 1024
        try:
            pyAesCrypt.decryptStream(io.BytesIO(open("pass", 'rb').read()), f_dec, password, buffer_size,311)
            if (str(f_dec.getvalue()).__contains__("T")):
                Utils.password=password
                return True
        except:
            return False
        return False

