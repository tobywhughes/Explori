#Manages files

import os, shutil

def delete_file(file_path):
    #Trys to remove file
    try:
        os.remove(file_path)
    except:
        #Tries to remove directory
        try:
            os.rmdir(file_path)
        #Error if directory isn't empty
        except:
            print("Error - Directory not empty")

def copy_file(file_path, file_name, current_path, del_flag):
    new_file_path = current_path + '/' + file_name
    #Checks if it is replacing a file
    if not os.path.exists(new_file_path):
        shutil.copy(file_path, new_file_path)
        
        #If it is a cut and not a copy, also call delete_file
        if del_flag:
            delete_file(file_path)
