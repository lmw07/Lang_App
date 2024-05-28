from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLabel

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, word, translation):
        super().__init__()
        self.word = word
        self.translation = translation
        self.isTranslationShown = False
        self.setText(word)
        self.setAlignment(Qt.AlignCenter)
        self.setMouseTracking(True)
        self.setFontSize(14)

    def mousePressEvent(self, event):
        self.setText(self.translation if not self.isTranslationShown else self.word)
        self.isTranslationShown = not self.isTranslationShown
        self.clicked.emit()

    def enterEvent(self, event):
        self.setStyleSheet("QLabel { color : blue; }")

    def leaveEvent(self, event):
        self.setStyleSheet("QLabel { color : black; }")

    def setFontSize(self, size):
        font = self.font()
        font.setPointSize(size)
        self.setFont(font)