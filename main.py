#Explori File Explorer
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *



class Screen(QWidget):

    path = "~\\"
    input_holder = ""
    
    def __init__(self):
        super(Screen, self).__init__()
        self.initScreen()
 
    def initScreen(self):
        self.setGeometry(300,300,300,300)
        self.setWindowTitle("Explori File Explorer")
        self.label = QLabel(self.path)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.show()
    
    def keyPressEvent(self,event):
        if event.key() == Qt.Key_Shift:
            self.input_holder = self.get_input()
            if self.input_holder == "..\\":
                pass #temp for going backwards
            else:
                self.path = self.path + self.input_holder
            self.label.setText(self.path)

    def get_input(self):
        #Temp Value
        return "Downloads\\"


def run_gui():
    app = QApplication(sys.argv)
    screen = Screen()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_gui()


    
