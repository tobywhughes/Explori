#Class to deal with the path
import os

class Path():
    
    home = os.path.expanduser('~')

    #Gives default values to variables related to path
    def __init__(self):
        self.path = self.home
        self.copy_path = ''
        self.copy_file_name = ''
        clipboard_flag = False
        del_flag = False

    #Traverses back a directory
    def back_traverse(self):
        if not os.path.samefile(self.path, '/home') and not os.path.samefile(self.path, '/'):
            holder = self.path.split('/')
            self.path = '/'.join(holder[0:-1])
        else:
            self.path = '/'


