import os
import shutil
from datetime import datetime

import rsa
from OpenSSL import crypto

from Utils import Utils


class FileSigner:
    def remove_my_key(self, key_alias):

        for filename in os.listdir("MyKeys"):
            if filename.split("_")[0] == key_alias:
                os.remove("MyKeys/" + filename)

    def __init__(self):
        pass



    def get_pub_key(self):
        crt_obj = crypto.load_certificate(crypto.FILETYPE_PEM, open("cert/certificate.crt", 'rb').read())
        pub_key_object = crt_obj.get_pubkey()
        pub_key_string = crypto.dump_publickey(crypto.FILETYPE_PEM, pub_key_object)
        return pub_key_string

    def verify_cert(self):
        result=""
        if os.popen("openssl verify -CAfile temp/ca_bundle.crt temp/certificate.crt").read().__contains__("OK"):
            result+="1"
        else:
            result+="0"
        crt_obj = crypto.load_certificate(crypto.FILETYPE_PEM, open("temp/certificate.crt", 'rb').read())
        if int(crt_obj.get_notAfter()[2:-1])-int(datetime.now().strftime("%y%m%d%H%M%S"))>0:
            result+="1"
        else:
            result+="0"
        return result
    def get_subject(self):
        crt_obj = crypto.load_certificate(crypto.FILETYPE_PEM, open("temp/certificate.crt", 'rb').read())
        pub_key_object = crt_obj.get_pubkey()
        pub_key_string = crypto.dump_publickey(crypto.FILETYPE_PEM, pub_key_object)
        return (crt_obj.get_subject().CN, crt_obj.get_issuer().CN)

    def import_certificate(self, ca_bundle, private_key, cert, alias):
        shutil.copy2(private_key, "MyKeys/" + alias + "_privkey.key")
        shutil.copy2(cert, "MyKeys/" + alias + "_certificate.crt")
        shutil.copy2(ca_bundle, "MyKeys/" + alias + "_ca_bundle.crt")
        Utils().encrypt_file("MyKeys/" + alias + "_privkey.key")

    def import_public_key(self, key_path, alias):
        shutil.copy2(key_path, "Pubkeys/" + alias + "_publickey.key")

    def _check_name_existance(self, name, my_key):
        dir_name = "Pubkeys"
        if my_key == True:
            dir_name = "MyKeys"
        for filename in os.listdir(dir_name):
            if filename.split("_")[0] == name:
                return filename
        return False

    def generate_new_key(self, name):
        if (self._check_name_existance(name, True)):
            return False
        (pubkey, privkey) = rsa.newkeys(2048)
        pub_key_file = open("MyKeys/" + name + '_publickey.key', 'wb')
        pub_key_file.write(pubkey.save_pkcs1('PEM'))
        privkey_file = open("MyKeys/" + name + '_privkey.key', 'wb')
        privkey_file.write(privkey.save_pkcs1('PEM'))
        privkey_file.close()
        pub_key_file.close()
        Utils().encrypt_file("MyKeys/" + name + '_privkey.key')
        return True

    def get_my_keys(self):
        keys = []
        for filename in os.listdir("MyKeys"):
            if filename.__contains__("privkey.key"):
                key_entry=""
                if os.path.exists("MyKeys/"+filename.split("_")[0]+"_certificate.crt"):
                    key_entry = ("C"+filename.split("_")[0], open("MyKeys/" + filename, 'rb').read())
                else:
                    key_entry = ("G" + filename.split("_")[0], open("MyKeys/" + filename, 'rb').read())
                keys.append(key_entry)
        return keys

    def get_pub_keys(self):
        keys = []
        for filename in os.listdir("Pubkeys"):
            if filename.__contains__("publickey.key"):
                key_entry = (filename.split("_")[0], open("Pubkeys/" + filename, 'r').read())
                keys.append(key_entry)
        return keys

    def _sign(self, key_file, file_to_sign):
        file_to_sign = open(file_to_sign, 'rb')
        file_data = file_to_sign.read()
        file_to_sign.close()
        hash_value = rsa.compute_hash(file_data, 'SHA-512')
        privkey = rsa.PrivateKey.load_pkcs1(Utils().decrypt_file("MyKeys/"+key_file))
        signature = rsa.sign(file_data, privkey, 'SHA-512')
        return (signature)

    def sign(self, key_alias, file_to_sign):
        return self._sign(key_alias + "_privkey.key", file_to_sign)

    def _verify_signature(self, pubkey_alias, file_to_be_verified):
        if pubkey_alias == None:
            pubkey = self.get_pub_key()
            pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(pubkey)

        else:
            pubkey = open("Pubkeys/" + pubkey_alias + "_publickey.key", 'rb').read()
            pubkey = rsa.PublicKey.load_pkcs1(pubkey)

        file_to_be_verified = open(file_to_be_verified, 'rb')

        signature = open('temp/signature', 'rb').read()
        file_to_be_verified_data = file_to_be_verified.read()
        file_to_be_verified.close()
        try:
            rsa.verify(file_to_be_verified_data, signature, pubkey)
            if pubkey_alias == None:
                return (self.get_subject(),self.verify_cert())
            return pubkey_alias
        except:
            return False

    def verify_signature(self, file_to_be_verified):
        Utils().unzip_files(file_to_be_verified)
        pubkey = ""
        for filename in os.listdir("temp"):
            if filename not in ["pkey.key", "signature", "certificate.crt", "ca_bundle.crt"]:
                file_to_be_verified = "temp/" + filename
        if (os.path.exists("temp/certificate.crt")):
            return self._verify_signature(None, file_to_be_verified)
        else:
            pubkey = open('temp/pkey.key').read()

        for filename in os.listdir("Pubkeys"):
            file = open("Pubkeys/" + filename)
            if file.read() == pubkey:
                return self._verify_signature(filename.split("_")[0], file_to_be_verified)
        return 2

    def remove_public_key(self, selected_key):
        for filename in os.listdir("Pubkeys"):
            if filename.split("_")[0] == selected_key:
                os.remove("Pubkeys/" + filename)

    def update_my_key(self, new_key, selected_key):
        for filename in os.listdir("MyKeys"):
            if filename.split("_")[0] == selected_key:
                last_name = ""
                for i in filename.split("_")[1:]:
                    last_name += "_" + i
                shutil.move("MyKeys/" + filename, "MyKeys/" + new_key + last_name)


    def update_public_key(self, new_key, selected_key):
        for filename in os.listdir("Pubkeys"):
            if filename.split("_")[0] == selected_key:
                last_name = ""
                for i in filename.split("_")[1:]:
                    last_name += "_" + i
                shutil.move("Pubkeys/" + filename, "Pubkeys/" + new_key + last_name)
