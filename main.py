#Explori File Explorer

import sys, os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Screen(QWidget):


    home = os.path.expanduser('~')
    path = home 
    current_level_list = []
   
    #Flags
    hidden_flag = True

    def __init__(self):
        #initial gui setup
        super(Screen, self).__init__()
        self.get_current_level()
        self.setGeometry(0,0,0,0)
        self.setWindowTitle('Explori File Explorer')
        self.setFocus()

        #Creates widgets for screen
        self.path_label = QLabel(self.path)

        self.list_widget = QListWidget()
        self.get_current_level()
        self.update_list_widget()
        self.list_widget.setGridSize(QSize(150,20))
        self.list_widget.setMinimumSize(150,415)
        #Creates Layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.path_label)
        self.layout.addWidget(self.list_widget)
        self.setLayout(self.layout)
        self.show()
 
    def keyPressEvent(self,event):
        
        #Scrolls through list_widget. May (probably) not the best way to do this with Qt/PyQt. Still looking for a cleaner alternative
        if event.key() == Qt.Key_Down or Qt.Key_Up:
            self.list_widget.keyPressEvent(event)
        
        #Key to toggle hidden
        if event.key() == Qt.Key_Q:
            self.toggle_hidden()

        #Path Input
        if event.key() == Qt.Key_Shift:
            try:
                if self.line_edit is None:
                    self.get_input()
            except AttributeError:
                self.get_input()

        #Backwards Traversal
        if event.key() == Qt.Key_Backspace:
            self.path = self.back_traverse()
            self.path_label.setText(self.path)            
            self.path_update_event()
 
        #Go to home directory  
        if event.key() == Qt.Key_Home:
            self.path = self.home
            self.path_label.setText(self.path)
            self.path_update_event()

        #Go to selection
        if event.key() == Qt.Key_Return:
            self.list_view_enter()
    
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
        self.setFocus()
        self.line_edit.close()
        self.line_edit = None
        self.path_update_event()

    def list_view_enter(self):
        current_item = self.list_widget.currentItem()
        self.path = self.path + '/' + current_item.text()
        self.path_update_event()

    #Returns to the directory one level up
    def back_traverse(self):
        holder = self.path.split('/')
        return '/'.join(holder[0:-1])

    #Grabs all files and directories from current directory
    def get_current_level(self):
        del self.current_level_list[:]
        for items in os.listdir(self.path):
            if self.hidden_flag:
                if items[0] != '.':
                    self.current_level_list.append(items)
                    
            else:
                self.current_level_list.append(items)

    def update_list_widget(self):
        self.list_widget.clear()
        for item in self.current_level_list:
            self.list_widget.addItem(item)

    def path_update_event(self):
        try:
            self.get_current_level()
            self.update_list_widget()
            self.path_label.setText(self.path);
        except NotADirectoryError:
            print('Debug - Path Error')
            self.back_traverse()

    def toggle_hidden(self):
        if self.hidden_flag:
            self.hidden_flag = False
        else:
            self.hidden_flag = True
        self.path_update_event()



def run_gui():
    app = QApplication(sys.argv)    

    screen = Screen()
    sys.exit(app.exec())


if __name__ == '__main__':
    run_gui()


   
