#Explori File Explorer

import sys, os, webbrowser
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import path

class Screen(QWidget):


    current_level_list = []
   
    #Flags
    hidden_flag = True

    def __init__(self):
        self.path = path.Path()
        #initial gui setup
        super(Screen, self).__init__()
        self.get_current_level()
        self.setGeometry(0,0,0,0)
        self.setWindowTitle('Explori File Explorer')
        self.setFocus()

        #Creates widgets for screen
        self.path_label = QLabel(self.path.path)

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
        
        #Scrolls through list_widget. May (probably) not the best way to do this with Qt/PyQt. 
        #Still looking for a cleaner alternative
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
            self.path.back_traverse()
            self.path_label.setText(self.path.path)            
            self.path_update_event()
 
        #Go to home directory  
        if event.key() == Qt.Key_Home:
            self.path.path = self.home
            self.path_label.setText(self.path.path)
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
        self.path.path = self.path.path + '/' + str(self.line_edit.text())
        self.path_label.setText(self.path.path)
        self.layout.removeWidget(self.line_edit)
        self.line_edit.releaseKeyboard()
        self.setFocus()
        self.line_edit.close()
        self.line_edit = None
        self.path_update_event()

    def list_view_enter(self):
        current_item = self.list_widget.currentItem()
        self.path.path = self.path.path + '/' + current_item.text()
        self.path_update_event(current_item.whatsThis())

    #Grabs all files and directories from current directory
    def get_current_level(self):
        del self.current_level_list[:]
        for items in os.listdir(self.path.path):
            item_type = self.get_item_type(items)
            item_tuple = (items, item_type)
            if self.hidden_flag:
                if items[0] != '.':
                    self.current_level_list.append(item_tuple)
                    
            else:
                self.current_level_list.append(item_tuple)
    
    #Simple algorithm to determine filetype. Currently no method to weed out directories with periods in their names
    def get_item_type(self, item):
        #Ignore if file/dir is hidden or not
        if item[0] == '.':
            item = item[1:]
        item_index = len(item) - item[::-1].find('.')
        if (item_index > len(item)):
            return 'Directory'
        else:
            return item[item_index:]

    def update_list_widget(self):
        self.list_widget.clear()
        for item in self.current_level_list:
            list_item = QListWidgetItem(item[0])
            list_item.setBackground(self.assign_color(item[1]))
            list_item.setWhatsThis(item[1])
            self.list_widget.addItem(list_item)

    #Color codes QListWidget items.
    #Will eventually create customizable system
    def assign_color(self, file_type):
            if file_type != 'Directory':
                return QColor(255,0,0,150)
            else:
                return QColor(255,255,255)

    def path_update_event(self, file_type = 'Directory'):
        try:
            if file_type == 'Directory':
                self.get_current_level()
                self.update_list_widget()
                self.path_label.setText(self.path.path)
            else:
                try:
                    webbrowser.open(self.path.path)
                except Error:
                    print('Debug - File Cannot Open')
                    self.path.back_traverse()
        except NotADirectoryError:
            print('Debug - Path Error')
            self.path.back_traverse()

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


   
