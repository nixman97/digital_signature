import os
import shutil

import rsa

from Utils import Utils


class FileSigner:
    def __init__(self):
        pass

    def import_public_key(self,key_path,alias):
        shutil.move(key_path,"Pubkeys/"+alias+"_publickey.key")
    def _check_name_existance(self, name, my_key):
        dir_name="Pubkeys"
        if my_key==True:
            dir_name="MyKeys"
        for filename in os.listdir(dir_name):
            if filename.split("_")[0]==name:
                return filename
        return False

    def generate_new_key(self,name):
        if (self._check_name_existance(name, True)):
            return False
        (pubkey,privkey) = rsa.newkeys(2048)
        pub_key_file = open("MyKeys/"+name+'_publickey.key','wb')
        pub_key_file.write(pubkey.save_pkcs1('PEM'))
        privkey_file = open("MyKeys/"+name+'_privkey.key','wb')
        privkey_file.write(privkey.save_pkcs1('PEM'))
        return True

    def get_my_keys(self):
        keys=[]
        for filename in os.listdir("MyKeys"):
            if filename.__contains__("publickey.key"):
                key_entry=(filename.split("_")[0],open("MyKeys/"+filename,'r').read())
                keys.append(key_entry)
        return keys

    def get_pub_keys(self):
        keys=[]
        for filename in os.listdir("Pubkeys"):
            if filename.__contains__("publickey.key"):
                key_entry=(filename.split("_")[0],open("Pubkeys/"+filename,'r').read())
                keys.append(key_entry)
        return keys


    def _sign(self, key_file, file_to_sign):
        key_file = open("MyKeys/"+key_file,'rb')
        key_data = key_file.read()
        key_file.close()
        file_to_sign = open(file_to_sign,'rb')
        file_data = file_to_sign.read()
        file_to_sign.close()
        hash_value=rsa.compute_hash(file_data,'SHA-512')
        privkey=rsa.PrivateKey.load_pkcs1(key_data)
        signature=rsa.sign(file_data,privkey,'SHA-512')
        return signature

    def sign(self,key_alias,file_to_sign):
        return self._sign(key_alias+"_privkey.key",file_to_sign)

    def _verify_signature(self,pubkey_alias,file_to_be_verified):
        pubkey=open("Pubkeys/"+pubkey_alias+"_publickey.key",'rb').read()
        file_to_be_verified = open(file_to_be_verified,'rb')
        pubkey=rsa.PublicKey.load_pkcs1(pubkey)

        signature=open('temp/signature','rb').read()
        file_to_be_verified_data = file_to_be_verified.read()
        file_to_be_verified.close()
        try:
            rsa.verify(file_to_be_verified_data,signature , pubkey)
            return pubkey_alias
        except:
            return False

    def verify_signature(self, file_to_be_verified):
        Utils().unzip_files(file_to_be_verified)

        pubkey=open('temp/pkey.key').read()
        for filename in os.listdir("temp"):
            if filename not in ["pkey.key","signature"]:
                file_to_be_verified="temp/"+filename
        for filename in os.listdir("Pubkeys"):
            file=open("Pubkeys/"+filename)
            if file.read()==pubkey:
                return self._verify_signature(filename.split("_")[0],file_to_be_verified)
        return 2