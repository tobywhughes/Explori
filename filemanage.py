#Manages files

import os

def delete_file(file_path):
    try:
        os.remove(file_path)
    except:
        try:
            os.rmdir(file_path)
        except:
            print("Error - Directory not empty")
