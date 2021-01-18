from bitarray import bitarray

from Sha256 import Sha256
import hashlib

filename = "hello world"
with open(filename, "rb") as f:
    bytes = f.read()  # read entire file as bytes
    readable_hash = hashlib.sha256(bytes).hexdigest()
    print(readable_hash)
if __name__ == '__main__':
    a=bitarray()
    a.fromfile(open("hello world",'rb'))
    print(a)
    print(Sha256().calculate_hash_from_file("hello world"))


