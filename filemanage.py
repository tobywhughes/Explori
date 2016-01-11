#Manages files

import os, shutil

def delete_file(file_path):
    try:
        os.remove(file_path)
    except:
        try:
            os.rmdir(file_path)
        except:
            print("Error - Directory not empty")

def copy_file(file_path, file_name, current_path, del_flag):
    new_file_path = current_path + '/' + file_name
    if not os.path.exists(new_file_path):
        shutil.copy(file_path, new_file_path)
        if del_flag:
            delete_file(file_path)
