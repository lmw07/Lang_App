
from collections import deque
import random
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QInputDialog, QApplication
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import app.services.dbmanager as dbmanager
from app.gui.clickable_label import ClickableLabel
import app.services.data_service as data_service
from app.models.sentence import Sentence
from app.constants import SENTENCES_TO_GET_PER_WORD


class TargetedModeLayout(QWidget):
    def __init__(self):
        super().__init__()
        self.workingSet = []
        self.labels = []
        self.centralWidget = QWidget()
        self.sentenceTuple = data_service.getOneRandomSentenceFromDb()
        self.sentenceQueue = deque([self.sentenceTuple])
        self.popAndGatherSentenceData()
        #words to generate sentences for
        self.queueCandidates = deque()
        self.initUI()
        #self.player = QMediaPlayer()
        
    def popAndGatherSentenceData(self):
        self.currSentence : Sentence= self.sentenceQueue.popleft()        


    def initUI(self):
       # self.centralWidget = QWidget()  # Create a central widget #DRY candidate
        layout = QVBoxLayout()
        layout.addStretch()

        self.counterBox = QLabel(f"Sentences left in set: {len(self.sentenceQueue)}")
        layout.addWidget(self.counterBox, alignment=Qt.AlignCenter)

        self.sentenceLayout = QHBoxLayout()
        self.initLabels()
        layout.addLayout(self.sentenceLayout)

        self.translatedSentenceBox = QLabel("")
        self.translatedSentenceBox.setFont(QFont('Arial', 12)) 
        layout.addWidget(self.translatedSentenceBox, alignment=Qt.AlignCenter)

        self.translateButton = QPushButton("Translate")
        self.translateButton.clicked.connect(self.on_translate_button_clicked)
        layout.addWidget(self.translateButton, alignment=Qt.AlignCenter)

        self.initProgressButtons(layout)

        self.queuedCandidatesLayout = QHBoxLayout()
        self.initQueueLayout()
        layout.addLayout(self.queuedCandidatesLayout)

            #Maybe add in later
        # changeSetButton = QPushButton("Randomize the current sentence set")
        # changeSetButton.clicked.connect(self.on_change_set_button_clicked)
        # layout.addWidget(changeSetButton, alignment=Qt.AlignCenter)

        

                # Button to play sound -- not currently used but possible in future
        # playButton = QPushButton('Play Sound', self)
        # playButton.clicked.connect(self.playSound)
        
        # Add the button to the layout
        #layout.addWidget(playButton)


        layout.addStretch()
        self.setLayout(layout)



        # Not currently used, might be used in future if real time sound generation is added to this mode
    # def playSound(self, speed = 1.0):
    #     soundFile = data_service.getSoundFile(self.currSentence.id)
        
    #     try:
    #         if not hasattr(self, 'player'):
    #             self.player = QMediaPlayer()
    #         self.player.setMedia(QMediaContent(QUrl.fromLocalFile(soundFile)))
    #         self.player.setPlaybackRate(speed)
    #         self.player.play()
    #     except Exception as e:
    #         print("An error occurred:", e)



    def initQueueLayout(self):
        while self.queuedCandidatesLayout.count():
            layoutItem = self.queuedCandidatesLayout.takeAt(0)
            if layoutItem.widget():
                layoutItem.widget().deleteLater()
        # Reapply stretch to ensure labels are centered
        self.queuedCandidatesLayout.addStretch()
        if len(self.queueCandidates) == 0:
            label = QLabel("")
            label.setFont(QFont('Arial', 18)) 
            self.queuedCandidatesLayout.addWidget(label)
        for word in self.queueCandidates:
            label = QLabel(word)
            label.setFont(QFont('Arial', 18)) 
            self.queuedCandidatesLayout.addWidget(label)
        self.queuedCandidatesLayout.addStretch()


    def initLabels(self):
        # Clear existing widgets from the sentence layout
        while self.sentenceLayout.count():
            layoutItem = self.sentenceLayout.takeAt(0)
            if layoutItem.widget():
                layoutItem.widget().deleteLater()
        
        # Reapply stretch to ensure labels are centered
        self.sentenceLayout.addStretch()

        
        for word, translation in self.currSentence.word_map.items():
            label = ClickableLabel(word, translation)

            label.clicked.connect(lambda word=word: self.updateQueueCandidates(word))
            self.sentenceLayout.addWidget(label)
            self.labels.append(label)

        # Add stretch after labels to keep them centered
        self.sentenceLayout.addStretch()
        #self.playSound()

    def updateQueueCandidates(self,norskWord):
        if norskWord in self.queueCandidates:
            self.queueCandidates.remove(norskWord)
        else:
            self.queueCandidates.append(norskWord)
        self.initQueueLayout()

    def initProgressButtons(self, layout):
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()

        self.learnedButton = QPushButton("Continue")
        self.learnedButton.setStyleSheet("background-color: lightgreen;")
        self.learnedButton.clicked.connect(lambda: self.on_continue_clicked())
        buttonLayout.addWidget(self.learnedButton)

        buttonLayout.addStretch()
        layout.addLayout(buttonLayout)

    def on_change_set_button_clicked(self):
        self.sentenceQueue.clear()
        sentenceTuple = data_service.getOneRandomSentenceFromDb()
        self.sentenceQueue = deque([sentenceTuple])
        self.popAndGatherSentenceData()
        self.counterBox.setText(f"Sentences left in set: {len(self.sentenceQueue)}")
        self.translatedSentenceBox.setText("")
        self.initLabels()

    def on_translate_button_clicked(self):
        self.translatedSentenceBox.setText(self.currSentence.english if not self.translatedSentenceBox.text() else "")

    def generateNewSentencesAndClearCandidates(self):
        if len(self.queueCandidates) == 0:
            return
        newSentences = data_service.getSentencesFromWords(self.queueCandidates, SENTENCES_TO_GET_PER_WORD)
        if newSentences:
            self.sentenceQueue = self.sentenceQueue + deque(newSentences)
        self.queueCandidates.clear()
        self.counterBox.setText(f"Sentences left in set: {len(self.sentenceQueue)}")
        self.initQueueLayout()
        
    def disableButtons(self):
        self.learnedButton.setDisabled(True)
        self.learnedButton.setText("Loading")
        self.learnedButton.setStyleSheet("background-color: red;")

        self.translateButton.setDisabled(True)

    def enableButtons(self):
        self.learnedButton.setDisabled(False)
        self.learnedButton.setText("Continue")
        self.learnedButton.setStyleSheet("background-color: lightgreen;")

        self.translateButton.setDisabled(False)

    def on_continue_clicked(self):
        if len(self.queueCandidates) == 0:
            #mark sentence as learned if queueCandidates is empty
            data_service.updateSentenceClass(self.currSentence.id, True)
        else:
            #mark sentence as unlearned if there are unknown words in it
            data_service.updateSentenceClass(self.currSentence.id, False)

        if len(self.sentenceQueue) == 0 and len(self.queueCandidates) == 0:
            QMessageBox.information(self, "End of Set Reached", "Great Job! You finished this set!")
            self.on_change_set_button_clicked()
        else:
            self.disableButtons()

            # Force the GUI to update
            QApplication.processEvents()
            self.generateNewSentencesAndClearCandidates()

            self.enableButtons()
    
            self.popAndGatherSentenceData()
            self.counterBox.setText(f"Sentences left in set: {len(self.sentenceQueue)}")
            self.initLabels()
            

        
        #self.counterBox.setText(f"Sentences left in set: {len(self.workingSet)}")
        #self.translatedSentenceBox.setText("")
        #self.initLabels()