import sys
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import *
from pygame import event
from Dino_Run import Iniciar

class JanelaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Super Mário Recife")
        self.setWindowIcon(QIcon('icone.png'))
        self.setGeometry(150,150,500,500)
        self.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.setFixedSize(self.size())
        self.Interface()

    def Interface(self):
        #texto1 = QLabel('Olá mundo!', self)
        #texto1.move(100,50)

        botao1 = QPushButton("Iniciar jogo", self)
        botao1.setStyleSheet("background-color: rgb(255, 255, 255);")
        botao1.setGeometry(150,150,200,80)

        botao1.clicked.connect(self.sair)

        #texto2 = QLabel("Wilhams", self)
        #texto2.move(200,50)

        self.show()

    def sair(self):
        self.hide()
        Iniciar() 
     
       


qt = QApplication(sys.argv)
app = JanelaPrincipal()
sys.exit(qt.exec())