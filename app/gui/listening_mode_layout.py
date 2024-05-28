from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import app.services.data_service as data_service
from app.models.sentence import Sentence

class ListeningModeLayout(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize the Sentence object to hold the current sentence
        self.currSentence: Sentence = data_service.getOneKnownSentenceFromDb()
        # Setup the user interface
        self.initUI()
        # Initialize the media player
        self.player = QMediaPlayer()
        # Start playing the sound associated with the current sentence
        self.playSound()

    def initUI(self):
        """Initialize the GUI components."""
        layout = QVBoxLayout()
        layout.addStretch()

        # Sentence in original language (Norwegian)
        self.originalSentenceBox = QLabel("")
        self.originalSentenceBox.setFont(QFont('Arial', 15))
        layout.addWidget(self.originalSentenceBox, alignment=Qt.AlignCenter)

        # Translated sentence
        self.translatedSentenceBox = QLabel("")
        self.translatedSentenceBox.setFont(QFont('Arial', 15))
        layout.addWidget(self.translatedSentenceBox, alignment=Qt.AlignCenter)

        # Button to toggle display of the Norwegian sentence
        showButton = QPushButton("Show Norsk")
        showButton.clicked.connect(self.on_show_button_clicked)
        layout.addWidget(showButton, alignment=Qt.AlignCenter)

        # Button to show the English translation
        translateButton = QPushButton("Translate")
        translateButton.clicked.connect(self.on_translate_button_clicked)
        layout.addWidget(translateButton, alignment=Qt.AlignCenter)

        # Initialize progress buttons (e.g., mark as learned)
        self.initProgressButtons(layout)

        # Button to play sound
        playButton = QPushButton('Play Sound', self)
        playButton.clicked.connect(self.playSound)
        layout.addWidget(playButton, alignment=Qt.AlignCenter)

        layout.addStretch()
        self.setLayout(layout)

    def playSound(self, speed=1.0):
        """Fetch and play sound for the current sentence at the specified speed."""
        soundFile = data_service.getSoundFile(self.currSentence.id)
        if not soundFile or soundFile == "None":
            # Handle the case where sound file is not found
            print("No sound file found, reloading sentence.")
            self.getSentence()

        try:
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(soundFile)))
            self.player.setPlaybackRate(speed)
            self.player.play()
        except Exception as e:
            print(f"An error occurred: {e}")

    def on_show_button_clicked(self):
        """Toggle the display of the Norwegian sentence."""
        if self.originalSentenceBox.text() == self.currSentence.norwegian:
            self.originalSentenceBox.setText("")
        else:
            self.originalSentenceBox.setText(self.currSentence.norwegian)

    def on_translate_button_clicked(self):
        """Toggle the display of the English translation."""
        if self.translatedSentenceBox.text():
            self.translatedSentenceBox.setText("")
        else:
            self.translatedSentenceBox.setText(self.currSentence.english)

    def initProgressButtons(self, layout):
        """Initialize the progress buttons layout."""
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()

        learnedButton = QPushButton("Continue")
        learnedButton.setStyleSheet("background-color: lightgreen;")
        learnedButton.clicked.connect(lambda: self.on_progress_button_clicked(True))
        buttonLayout.addWidget(learnedButton)

        buttonLayout.addStretch()
        layout.addLayout(buttonLayout)

    def on_progress_button_clicked(self, knewIt):
        """Handle progress update and fetch the next sentence."""
        self.originalSentenceBox.setText("")
        self.translatedSentenceBox.setText("")
        self.getSentence()
        self.playSound()

    def getSentence(self):
        """Retrieve a known sentence from the database."""
        self.currSentence = data_service.getOneKnownSentenceFromDb()
