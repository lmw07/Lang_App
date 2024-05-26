
import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QMainWindow, QAction, QInputDialog
from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import datafiles.dbmanager as dbmanager
from modes.ClickableLabel import ClickableLabel
import datafiles.data_service as data_service


class RegularModeLayout(QWidget):
    def __init__(self):
        super().__init__()
        self.workingSet = []
        self.fullWorkingSetSize = 8
        self.labels = []
        self.centralWidget = QWidget()
        self.updateWorkingSet(self.fullWorkingSetSize)
        self.initUI()
        
        self.player = QMediaPlayer()
        

 
    def onChangeSetSizeClicked(self):
        newSize, ok = QInputDialog.getInt(self, "Change Set Size", "Enter the new set size:", value=self.fullWorkingSetSize, min=2)
        if ok:
            self.fullWorkingSetSize = newSize
            self.on_change_set_button_clicked()

    def updateWorkingSet(self, size):
        self.workingSet = data_service.getMultipleRandomSentencesFromDb(size)

    def getATupleFromWorkingSet(self):
        return random.choice(self.workingSet) if self.workingSet else None

    def initUI(self):
       # self.centralWidget = QWidget()  # Create a central widget #DRY candidate
        layout = QVBoxLayout()
        layout.addStretch()

        self.counterBox = QLabel(f"Sentences left in set: {len(self.workingSet)}")
        layout.addWidget(self.counterBox, alignment=Qt.AlignCenter)

        self.sentenceLayout = QHBoxLayout()
        self.initLabels()
        layout.addLayout(self.sentenceLayout)

        self.translatedSentenceBox = QLabel("")
        self.translatedSentenceBox.setFont(QFont('Arial', 12)) 
        layout.addWidget(self.translatedSentenceBox, alignment=Qt.AlignCenter)

        translateButton = QPushButton("Translate")
        translateButton.clicked.connect(self.on_translate_button_clicked)
        layout.addWidget(translateButton, alignment=Qt.AlignCenter)

        self.initProgressButtons(layout)

        changeSetButton = QPushButton("Randomize the current sentence set")
        changeSetButton.clicked.connect(self.on_change_set_button_clicked)
        layout.addWidget(changeSetButton, alignment=Qt.AlignCenter)

        

        # Button to play sound
        playButton = QPushButton('Play Sound', self)
        playButton.clicked.connect(self.playSound)
        
        # Add the button to the layout
        layout.addWidget(playButton, alignment=Qt.AlignCenter)


        layout.addStretch()
        self.setLayout(layout)


    #TODO fix so it follows abstraction rules
    def playSound(self, speed = 1.0):
        soundFile = data_service.getSoundFile(self.currSentenceID)
        #soundFile = 'speechfiles/' + str(self.currSentenceID ) + '.mp3'
        try:
            if not hasattr(self, 'player'):
                self.player = QMediaPlayer()
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(soundFile)))
            self.player.setPlaybackRate(speed)
            self.player.play()
        except Exception as e:
            print("An error occurred:", e)


    def initLabels(self):
        # Clear existing widgets from the sentence layout
        while self.sentenceLayout.count():
            layoutItem = self.sentenceLayout.takeAt(0)
            if layoutItem.widget():
                layoutItem.widget().deleteLater()
        
        # Reapply stretch to ensure labels are centered
        self.sentenceLayout.addStretch()

        sentenceTuple = self.getATupleFromWorkingSet()
        if sentenceTuple:
            self.currNorskSentence, self.currEngSentence, dictionary, self.currSentenceID = sentenceTuple
            for word, translation in dictionary.items():
                label = ClickableLabel(word, translation)
                self.sentenceLayout.addWidget(label)
                self.labels.append(label)

        # Add stretch after labels to keep them centered
        self.sentenceLayout.addStretch()
        self.playSound()


    def initProgressButtons(self, layout):
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()

        didNotLearnButton = QPushButton("I didn't know it :(")
        didNotLearnButton.setStyleSheet("background-color: crimson;")
        didNotLearnButton.clicked.connect(lambda: self.on_progress_button_clicked(False))
        buttonLayout.addWidget(didNotLearnButton)

        learnedButton = QPushButton("I knew it!")
        learnedButton.setStyleSheet("background-color: lightgreen;")
        learnedButton.clicked.connect(lambda: self.on_progress_button_clicked(True))
        buttonLayout.addWidget(learnedButton)

        buttonLayout.addStretch()
        layout.addLayout(buttonLayout)

    def on_change_set_button_clicked(self):
        self.updateWorkingSet(self.fullWorkingSetSize)
        self.counterBox.setText(f"Sentences left in set: {len(self.workingSet)}")
        self.translatedSentenceBox.setText("")
        self.initLabels()

    def on_translate_button_clicked(self):
        self.translatedSentenceBox.setText(self.currEngSentence if not self.translatedSentenceBox.text() else "")

    def on_progress_button_clicked(self, knewIt):
        data_service.updateSentenceClass(self.currSentenceID, knewIt)
        if knewIt:
            for tup in self.workingSet:
                if self.currNorskSentence == tup[0]:
                    tupeToRemove = tup
            self.workingSet.remove(tupeToRemove)
            if not self.workingSet:
                QMessageBox.information(self, "End of Set Reached", "Great Job! You finished this set!")
                self.on_change_set_button_clicked()
        self.counterBox.setText(f"Sentences left in set: {len(self.workingSet)}")
        self.translatedSentenceBox.setText("")
        self.initLabels()