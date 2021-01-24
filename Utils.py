import os
import shutil
from os.path import basename
from zipfile import ZipFile


class Utils:
    def zip_files(self, name, file_path,public_key_alias, signature):
        zip_obj = ZipFile(name,'w')
        zip_obj.write(file_path, basename(file_path))
        open("signature",'wb').write(signature)
        zip_obj.write(os.path.abspath("signature"),"signature")
        zip_obj.write(os.path.abspath("MyKeys/"+public_key_alias+"_publickey.key"), "pkey.key")
        zip_obj.close()
        os.remove("signature")


    def unzip_files(self, zip_file_path):
        zip_obj = ZipFile(zip_file_path,'r')
        zip_obj.extractall('temp')
        zip_obj.close()
