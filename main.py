import sys

from bitarray import bitarray
from Crypto.PublicKey import RSA
from Sha256 import Sha256
import hashlib

keyPair = RSA.generate(bits=1024)
print(f"Public key: (n={hex(keyPair.n)}, e={hex(keyPair.e)})")
print(f"Private key: (n={hex(keyPair.n)}, d={hex(keyPair.d)})")
msg = b'A message for signing'
from hashlib import sha512
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
import MainWindow
ex = MainWindow.MainWindow(app)
sys.exit(app.exec_())

hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
signature = pow(hash, keyPair.d, keyPair.n)
print("Signature:", hex(signature))

if __name__ == '__main__':

    a = bitarray()
    a.fromfile(open("test_file.odt", 'rb'))
    print(a)
    msg = b'A message for signing'
    keyPair = RSA.generate(bits=1024)

    hash = int.from_bytes(Sha256().calculate_hash_from_file("test_file.odt"), byteorder='big')
    signature = pow(hash, keyPair.d, keyPair.n)
    print("Signature:", hex(signature))
