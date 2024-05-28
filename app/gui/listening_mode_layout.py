
import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QMainWindow, QAction, QInputDialog
from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import app.services.dbmanager as dbmanager
from app.gui.clickable_label import ClickableLabel
import app.services.data_service as data_service
from app.models.sentence import Sentence

class ListeningModeLayout(QWidget):
    def __init__(self):
        super().__init__()
        self.centralWidget = QWidget()
        self.getSentence()
        self.initUI()
        
        self.player = QMediaPlayer()
        self.playSound()

    def getSentence(self):
        self.currSentence : Sentence = data_service.getOneKnownSentenceFromDb()
   

    def initUI(self):
       # self.centralWidget = QWidget()  # Create a central widget #DRY candidate
        layout = QVBoxLayout()
        layout.addStretch()

        self.originalSentenceBox = QLabel("")
        self.originalSentenceBox.setFont(QFont('Arial', 15)) 
        layout.addWidget(self.originalSentenceBox, alignment=Qt.AlignCenter)

        self.translatedSentenceBox = QLabel("")
        self.translatedSentenceBox.setFont(QFont('Arial', 15)) 
        layout.addWidget(self.translatedSentenceBox, alignment=Qt.AlignCenter)

        showButton = QPushButton("Show Norsk")
        showButton.clicked.connect(self.on_show_button_clicked)
        layout.addWidget(showButton, alignment=Qt.AlignCenter)

        translateButton = QPushButton("Translate")
        translateButton.clicked.connect(self.on_translate_button_clicked)
        layout.addWidget(translateButton, alignment=Qt.AlignCenter)

        self.initProgressButtons(layout)

        # Button to play sound
        playButton = QPushButton('Play Sound', self)
        playButton.clicked.connect(self.playSound)
        
        # Add the button to the layout
        layout.addWidget(playButton, alignment=Qt.AlignCenter)


        layout.addStretch()
        self.setLayout(layout)


    def on_show_button_clicked(self):
        if self.originalSentenceBox.text() == self.currSentence.norwegian:
            self.originalSentenceBox.setText("")
        else:
            self.originalSentenceBox.setText(self.currSentence.norwegian)

  
    def playSound(self, speed = 1.0):
        soundFile = data_service.getSoundFile(self.currSentence.id)
        if soundFile == None or soundFile == "None":
            self.getSentence()
        #soundFile = 'speechfiles/' + str(self.currSentence.id ) + '.mp3'
        try:
            if not hasattr(self, 'player'):
                self.player = QMediaPlayer()
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(soundFile)))
            self.player.setPlaybackRate(speed)
            self.player.play()
        except Exception as e:
            print("An error occurred:", e)


    


    def initProgressButtons(self, layout):
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()

        
        learnedButton = QPushButton("Continue")
        learnedButton.setStyleSheet("background-color: lightgreen;")
        learnedButton.clicked.connect(lambda: self.on_progress_button_clicked(True))
        buttonLayout.addWidget(learnedButton)

        buttonLayout.addStretch()
        layout.addLayout(buttonLayout)



    def on_translate_button_clicked(self):
        self.translatedSentenceBox.setText(self.currSentence.english if not self.translatedSentenceBox.text() else "")

    def on_progress_button_clicked(self, knewIt):
        self.originalSentenceBox.setText("")
        self.translatedSentenceBox.setText("")
        self.getSentence()
        self.playSound()
 