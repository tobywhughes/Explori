#Explori File Explorer
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *



class Screen(QWidget):

    path = "~\\"
    home = "~\\"
    input_holder = ""
    
    def __init__(self):
        super(Screen, self).__init__()
        self.initScreen()
 
    def initScreen(self):
        self.setGeometry(0,0,500,900)
        self.setWindowTitle("Explori File Explorer")
        self.label = QLabel(self.path)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.show()
    
    def keyPressEvent(self,event):
        if event.key() == Qt.Key_Shift:
            try:
                self.line_edit
            except AttributeError:
                self.get_input()
         
        if event.key() == Qt.Key_Backspace:
            self.path = self.back_traverse()
            self.label.setText(self.path)            

        if event.key() == Qt.Key_Home:
            self.path = self.home
            self.label.setText(self.path)
    
    def get_input(self):
        self.line_edit = QLineEdit()
        self.line_edit.grabKeyboard()
        self.line_edit.grabMouse()
        self.layout.addWidget(self.line_edit)
        self.line_edit.returnPressed.connect(self.send_line_edit)

    def send_line_edit(self):
        self.path = self.path + str(self.line_edit.text()) + "\\"
        self.label.setText(self.path)
        self.layout.removeWidget(self.line_edit)
        self.line_edit.deleteLater()

    def back_traverse(self):
        holder = self.path.split("\\")
        return "\\".join(holder[0:-2]) + "\\"


def run_gui():
    app = QApplication(sys.argv)
    screen = Screen()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_gui()


   
