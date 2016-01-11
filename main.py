#Explori File Explorer

import sys, os, webbrowser
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import path, superconfig, filemanage

    
class Screen(QWidget):   

    current_level_list = []
   
    #Flags
    hidden_flag = True

    def __init__(self):
        
        self.config = superconfig.Config()

        self.path = path.Path()
        #initial gui setup
        super(Screen, self).__init__()
        self.get_current_level()
        self.setGeometry(0,0,0,0)
        self.setWindowTitle(self.config.title)
        self.setFocus()

        #Creates widgets for screen
        self.path_label = QLabel(self.path.path)


        self.list_widget = QListWidget()
        self.get_current_level()
        self.update_list_widget()
        self.list_widget.setGridSize(QSize(self.config.tab_width, self.config.tab_height))
        self.list_widget.setMinimumSize(self.config.width, self.config.height)
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
       
        self.setFocus()

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

        #Delete File
        if event.key() == Qt.Key_Delete:
            self.delete_prompt()

        #Copy file to clipboard - no delete
        if event.key() == Qt.Key_C and Qt.ControlModifier:
            self.path.copy_file_name = self.list_widget.currentItem().text()
            self.path.copy_path = self.path.path + '/' + self.path.copy_file_name
            self.path.copy_flag = True
            self.path.del_flag = False

        #Copy file to clipboard - delete
        if event.key() == Qt.Key_X and Qt.ControlModifier:
            self.path.copy_file_name = self.list_widget.currentItem().text()
            self.path.copy_path = self.path.path + '/' + self.path.copy_file_name
            self.path.copy_flag = True
            self.path.del_flag = True

        #Paste copy
        if event.key() == Qt.Key_V and Qt.ControlModifier:
            if self.path.copy_flag:
                if not self.path.del_flag:
                    filemanage.copy_file(self.path.copy_path, self.path.copy_file_name, self.path.path, self.path.del_flag)
                    self.path_update_event()
                else:
                    self.delete_prompt('cut_paste')

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
            return 'FOLDER'
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
                if file_type in self.config.color_dict:
                    QValue = self.config.color_dict[file_type]
                    return QColor(QValue[0], QValue[1], QValue[2], QValue[3])
                else:
                    return QColor(255, 255, 255, 255)
    def path_update_event(self, file_type = 'FOLDER'):
        try:
            if file_type == 'FOLDER':
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

    def delete_prompt(self, tag = 'normal'):
        self.dconf_label = QDialog()
        self.dconf_label.layout = QVBoxLayout()
        self.dconf_label.setLayout(self.dconf_label.layout)
        self.dconf_label.setWindowFlags(Qt.FramelessWindowHint)
        self.dconf_label.setFixedSize(150, 120)
        self.dconf_label.setGeometry(0,0,0,0)

        self.warn_label = QLabel()
        self.warn_label.setText("Confirm Delete?")    
        self.warn_label.setGeometry(0,0,150, 20)
        self.warn_label.setAlignment(Qt.AlignCenter)

        self.push_confirm = QPushButton()
        self.push_confirm.setText("Confirm")
        self.push_confirm.setGeometry(0,0,100,20)

        self.push_decline = QPushButton()
        self.push_decline.setText("Decline")
        self.push_decline.setGeometry(0,0,100,20)

        for widget_item in [self.warn_label, self.push_confirm, self.push_decline]:
            self.dconf_label.layout.addWidget(widget_item)
        self.dconf_label.show()
	
        if tag == 'normal':
            self.push_confirm.clicked.connect(self.confirm_pressed)
        elif tag == 'cut_paste':
             self.push_confirm.clicked.connect(self.cut_confirm_pressed)
        self.push_decline.clicked.connect(self.decline_pressed)

    def confirm_pressed(self):
        filemanage.delete_file(self.path.path + '/' + self.list_widget.currentItem().text())
        self.path_update_event()
        self.dconf_label.releaseKeyboard()
        self.dconf_label.close()
        self.setFocus()

    def decline_pressed(self):
        self.dconf_label.releaseKeyboard()
        self.dconf_label.close()
        self.setFocus()

    def cut_confirm_pressed(self):
        filemanage.copy_file(self.path.copy_path, self.path.copy_file_name, self.path.path, self.path.del_flag)
        self.path_update_event()
        self.dconf_label.releaseKeyboard()
        self.dconf_label.close()
        self.setFocus()


def run_gui():
    app = QApplication(sys.argv)    

    screen = Screen()
    sys.exit(app.exec())


if __name__ == '__main__':
    run_gui()


   
