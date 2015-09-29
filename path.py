import os

class Path():
    
    home = os.path.expanduser('~')

    def __init__(self):
        self.path = self.home

    def back_traverse(self):
        if not os.path.samefile(self.path, '/home') and not os.path.samefile(self.path, '/'):
            holder = self.path.split('/')
            self.path = '/'.join(holder[0:-1])
        else:
            self.path = '/'


