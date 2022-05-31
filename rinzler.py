from PyQt6.QtWidgets import QMainWindow,QPushButton,QApplication,QMenu,QFrame,QTextEdit,QLabel,QFileDialog,QComboBox
from PyQt6.QtGui import QIcon,QAction,QPixmap
import sys
from io import StringIO
from subprocess import call
from os import getcwd

class Rinzler(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        
        self.setWindowTitle("Rinzler's Editor")
        self.setWindowOpacity(.9)
        self.setWindowIcon(QIcon("tron.png"))
        self.setFixedSize(1200,700)
        self.setStyleSheet("background-color:grey;")
        
        self.menu_Bar = self.menuBar()
        self.menu_Bar.setStyleSheet("background-color:#FF6EC7;color:yellow;")

        self.fileMenu = QMenu("&File", self)

        self.newfile = QAction(QIcon("1.png"),"New File", self)
        self.newfile.setShortcut("CTRL+B")
        
        self.newwindow = QAction(QIcon("2.png"),"New Window", self)
        self.newwindow.setShortcut("CTRL+N")
        
        self.openfile = QAction(QIcon("3.png"),"Open File", self)
        self.openfile.setShortcut("CTRL+O")
        
        self.savefile = QAction(QIcon("4.png"),"Save File", self)
        self.savefile.setShortcut("CTRL+S")
        
        self.exitfile = QAction(QIcon("5.png"),"Close | Exit", self)
        self.exitfile.setShortcut("CTRL+E")
        
        self.fileMenu.addActions([self.newfile,self.newwindow])
        self.fileMenu.addSeparator()
        self.fileMenu.addActions([self.openfile,self.savefile])
        self.fileMenu.addSeparator()
        self.fileMenu.addActions([self.exitfile])
        
        self.editMenu = QMenu("&Edit", self)
        self.finditem = QAction(QIcon("1.png"),"Find", self)
        self.finditem.setShortcut("CTRL+F")
        self.editMenu.addActions([self.finditem])
        self.editMenu.addSeparator()
        self.replaceitem = QAction(QIcon("2.png"),"Replace", self)
        self.replaceitem.setShortcut("CTRL+R")
        self.editMenu.addActions([self.replaceitem])
                
        self.menu_Bar.addMenu(self.fileMenu)
        self.menu_Bar.addMenu(self.editMenu)
        for i in self.fileMenu.actions() + self.editMenu.actions():
            i.triggered.connect(self.do)
        
        self.main_work1 = QFrame(self)
        self.main_work1.setGeometry(0,22,600,688)
        self.main_work1_textarea = QTextEdit(self.main_work1)
        self.main_work1_textarea.setFixedSize(600,688)
        self.main_work1_textarea.setStyleSheet("background-color:white;color:crimson;border:0px groove yellow;font-size:20px;")
        self.main_work1_textarea.setTabStopDistance(16)
        self.main_work1_textarea.setPlaceholderText("Python Code : ")
        
        self.main_work2 = QFrame(self)
        self.main_work2.setGeometry(600,22,600,688)
        self.main_work2_textarea = QTextEdit(self.main_work2)
        self.main_work2_textarea.setFixedSize(600,688)
        self.main_work2_textarea.setStyleSheet("background-color:black;color:blue;border:0px groove yellow;font-size:20px;padding-top:25px;padding-left:25px;")
        self.main_work2_textarea.setReadOnly(True)
        self.main_work2_textarea.setPlaceholderText("OUTPUT :\nNOTE : This Is A Simple GUI For Python 3.10.4\nInterpreter So Please Avoid Infinite Loops (Ex : while True: ...)\nAnd inputs (Like : x = input('Enter A Word') , Instead Of Using Input Use A Random Value (Ex : x = randint(1,10) But Before That You Must Import The Random Module (Ex from random import randint)))\n... Thanks ♥ Hope It Helps")
        
        self.run = QPushButton("Run",self)
        self.run.setGeometry(570,22,60,30)
        self.run.setStyleSheet("background-color:green;color:gold;font-size:14px;font-weight:bold;")
        self.run.clicked.connect(self.execute)
        
        self.color = QLabel(self)
        self.color.setGeometry(575,60,50,50)
        self.color.setStyleSheet("background-color:transparent;border-radius:25px;")
        self.color.setPixmap(QPixmap("color.png").scaled(self.color.width(),self.color.height()))
        self.color.mousePressEvent = self.theme_change
        
        self.main_color_1,self.main_color_2 = "white","black"
        
        self.languages = QComboBox(self)
        self.languages.addItem(QIcon("python.png"),"Python","The High Level Programming Language Python...")
        self.languages.addItem(QIcon("c.png"),"C","The Programming Language C...")
        self.languages.setGeometry(560,670,80,30)
        self.languages.setStyleSheet("background-color:grey;color:cyan;border-radius:15px;")
        
        self.show()
    
    def do(self):
        if self.sender().text().lower() == "new file":
            self.main_work1_textarea.setText("")
        elif self.sender().text().lower() == "new window":
            self.main_work1_textarea.setText("")
        elif self.sender().text().lower() == "open file":
            x = QFileDialog.getOpenFileName()
            y = open(x[0])
            self.main_work1_textarea.setText(y.read())
            y.close()
        elif self.sender().text().lower() == "save file":
            QFileDialog.getSaveFileName()
        elif self.sender().text().lower() == "close | exit":
            self.close()
        elif self.sender().text().lower() == "find":
            ...
        elif self.sender().text().lower() == "replace":
            ...
        
    def theme_change(self,e):
        self.main_work1_textarea.setStyleSheet(self.main_work1_textarea.styleSheet().replace(self.main_color_1,self.main_color_2,1))
        self.main_work2_textarea.setStyleSheet(self.main_work2_textarea.styleSheet().replace(self.main_color_2,self.main_color_1,1))
        self.main_color_1,self.main_color_2 = self.main_color_2,self.main_color_1
        
    def execute(self):
        try:
            if self.languages.currentIndex() == 0:
                self.main_work1_textarea.setPlaceholderText("Python Code : ")
                old_stdout = sys.stdout
                new_stdout = StringIO()
                sys.stdout = new_stdout

                exec(self.main_work1_textarea.toPlainText())

                output = new_stdout.getvalue()

                sys.stdout = old_stdout

                self.main_work2_textarea.setText(output)
            else:
                self.main_work1_textarea.setPlaceholderText("C Code : ")
                c_file = open(getcwd().replace("\\","/") + "/" + "c_file.c","w")
                print(c_file.name)
                c_file.write(self.main_work1_textarea.toPlainText())
                call(["gcc",c_file.name])
                call("./a.out")
                c_file.close()
                
        except Exception as e:
            self.main_work2_textarea.setText(str(e))
        
if __name__ == "__main__":
    application = QApplication(sys.argv)
    rinz = Rinzler()
    application.exec()