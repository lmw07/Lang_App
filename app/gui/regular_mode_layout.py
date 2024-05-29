import random
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt,QUrl
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import app.services.data_service as data_service
from app.gui.clickable_label import ClickableLabel
import app.constants as constants

class RegularModeLayout(QWidget):
    def __init__(self):
        super().__init__()
        self.fullWorkingSetSize = constants.WORKING_SET_SIZE  # Default size of the working set
        self.fractionOld =constants.FRACTION_OLD_SENTENCES  # Fraction of old sentences in the working set
        self.workingSet = []  # List to hold the current set of sentences
        self.labels = []  # List to hold references to label widgets
        self.updateWorkingSet(self.fullWorkingSetSize)  # Initialize the working set
        self.initUI()
        self.player = QMediaPlayer()  # Media player for playing sounds

    def initUI(self):
        """Initializes the user interface for regular mode."""
        layout = QVBoxLayout()
        layout.addStretch()

        # Label to display the count of remaining sentences
        self.counterBox = QLabel(f"Sentences left in set: {len(self.workingSet)}")
        layout.addWidget(self.counterBox, alignment=Qt.AlignCenter)

        # Horizontal layout for displaying sentence words as clickable labels
        self.sentenceLayout = QHBoxLayout()
        self.initLabels()
        layout.addLayout(self.sentenceLayout)

        # Label to display the translation
        self.translatedSentenceBox = QLabel("")
        self.translatedSentenceBox.setFont(QFont('Arial', 12))
        layout.addWidget(self.translatedSentenceBox, alignment=Qt.AlignCenter)

        # Button to toggle translation display
        translateButton = QPushButton("Translate")
        translateButton.clicked.connect(self.on_translate_button_clicked)
        layout.addWidget(translateButton, alignment=Qt.AlignCenter)

        # Progress buttons (for marking learning progress)
        self.initProgressButtons(layout)

        # Button to randomize the current set of sentences
        changeSetButton = QPushButton("Randomize the current sentence set")
        changeSetButton.clicked.connect(self.on_change_set_button_clicked)
        layout.addWidget(changeSetButton, alignment=Qt.AlignCenter)

        # Button to play sound
        playButton = QPushButton('Play Sound', self)
        playButton.clicked.connect(self.playSound)
        layout.addWidget(playButton, alignment=Qt.AlignCenter)

        layout.addStretch()
        self.setLayout(layout)

    def updateWorkingSet(self, size):
        """Updates the working set of sentences."""
        self.workingSet = data_service.getMultipleRandomSentencesFromDb(size, self.fractionOld)

    def getASentenceFromWorkingSet(self):
        """Returns a random sentence from the working set."""
        return random.choice(self.workingSet) if self.workingSet else None

    def initLabels(self):
        """Initializes clickable labels for the words in the current sentence."""
        # Clear existing widgets from the sentence layout
        while self.sentenceLayout.count():
            layoutItem = self.sentenceLayout.takeAt(0)
            if layoutItem.widget():
                layoutItem.widget().deleteLater()
        
        self.sentenceLayout.addStretch()
        self.currSentence = self.getASentenceFromWorkingSet()
        
        if self.currSentence:
            for word, translation in self.currSentence.word_map.items():
                label = ClickableLabel(word, translation)
                self.sentenceLayout.addWidget(label)
                self.labels.append(label)

        self.sentenceLayout.addStretch()
        self.playSound()

    def on_translate_button_clicked(self):
        """Toggles the display of the English translation."""
        if self.translatedSentenceBox.text():
            self.translatedSentenceBox.setText("")
        else:
            self.translatedSentenceBox.setText(self.currSentence.english)

    def on_change_set_button_clicked(self):
        """Randomizes the sentences in the current set."""
        self.updateWorkingSet(self.fullWorkingSetSize)
        self.counterBox.setText(f"Sentences left in set: {len(self.workingSet)}")
        self.translatedSentenceBox.setText("")
        self.initLabels()

    def initProgressButtons(self, layout):
        """Initializes progress buttons to mark sentences as known or unknown."""
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()

        learnedButton = QPushButton("I knew it!")
        learnedButton.setStyleSheet("background-color: lightgreen;")
        learnedButton.clicked.connect(lambda: self.on_progress_button_clicked(True))
        buttonLayout.addWidget(learnedButton)

        didNotLearnButton = QPushButton("I didn't know it :(")
        didNotLearnButton.setStyleSheet("background-color: crimson;")
        didNotLearnButton.clicked.connect(lambda: self.on_progress_button_clicked(False))
        buttonLayout.addWidget(didNotLearnButton)

        buttonLayout.addStretch()
        layout.addLayout(buttonLayout)

    def on_progress_button_clicked(self, knewIt):
        """Updates the learning status of the current sentence and fetches a new one."""
        data_service.updateSentenceClass(self.currSentence.id, knewIt)
        if knewIt:
            self.workingSet.remove(self.currSentence)
            self.counterBox.setText(f"Sentences left in set: {len(self.workingSet)}")
        if not self.workingSet:
            QMessageBox.information(self, "End of Set Reached", "Great Job! You finished this set!")
            self.on_change_set_button_clicked()
        self.initLabels()

    def playSound(self, speed=1.0):
        """Plays the sound associated with the current sentence."""
        soundFile = data_service.getSoundFile(self.currSentence.id)
        try:
            if not hasattr(self, 'player'):
                self.player = QMediaPlayer()
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(soundFile)))
            self.player.setPlaybackRate(speed)
            self.player.play()
        except Exception as e:
            print("An error occurred:", e)
