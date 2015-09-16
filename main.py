#Explori File Explorer

import sys, os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Screen(QWidget):


    home = os.path.expanduser('~')
    path = home 
    current_level_list = []
    
    def __init__(self):
        super(Screen, self).__init__()
        self.get_current_level()
        self.initScreen()
 
    def initScreen(self):
        self.setGeometry(0,0,500,600)
        self.setWindowTitle('Explori File Explorer')
        self.path_label = QLabel(self.path)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.path_label)
        self.setLayout(self.layout)
        self.show()
    
    def keyPressEvent(self,event):
        
        #Path Input
        if event.key() == Qt.Key_Shift:
            try:
                if self.line_edit == None:
                    self.get_input()
            except AttributeError:
                self.get_input()

        #Backwards Traversal
        if event.key() == Qt.Key_Backspace:
            self.path = self.back_traverse()
            self.path_label.setText(self.path)            
            self.get_current_level()
 
        #Go to home directory  
        if event.key() == Qt.Key_Home:
            self.path = self.home
            self.path_label.setText(self.path)
            self.get_current_level()
    
    #Creates input bar to get path input
    def get_input(self):
        self.line_edit = QLineEdit()
        self.line_edit.grabKeyboard()
        self.layout.addWidget(self.line_edit)
        self.line_edit.returnPressed.connect(self.send_line_edit)

    #Edits path after return is pressed
    def send_line_edit(self):
        self.path = self.path + '/' + str(self.line_edit.text())
        self.path_label.setText(self.path)
        self.layout.removeWidget(self.line_edit)
        self.line_edit.releaseKeyboard()
        self.line_edit.close()
        self.line_edit = None
        self.get_current_level()

    #Returns to the directory one level up
    def back_traverse(self):
        holder = self.path.split('/')
        return '/'.join(holder[0:-1])

    #Grabs all files and directories from current directory
    def get_current_level(self):
        del self.current_level_list[:]
        for items in os.listdir(self.path):
            self.current_level_list.append(items)
            print(items)


def run_gui():
    app = QApplication(sys.argv)
    screen = Screen()
    sys.exit(app.exec())


if __name__ == '__main__':
    run_gui()


   
