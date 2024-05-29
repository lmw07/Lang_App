'''
Creates the GUI for the language learning app
'''
import sys
import dbmanager
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QMessageBox, QMenuBar, QAction
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPalette
import random

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, word, translation):
        super(ClickableLabel, self).__init__()
        self.word = word
        self.translation = translation
        self.setText(word)
        self.setMouseTracking(True)
        self.clickTracker = False
        
    def mousePressEvent(self, event):
        if not(self.clickTracker):
            self.setText(self.translation)
            self.clickTracker = not(self.clickTracker)
        else:
            self.setText(self.word)
            self.clickTracker = not(self.clickTracker)
        
        
        self.clicked.emit()

    def enterEvent(self, event):
        # Change the font color to blue when the mouse hovers over
        self.setStyleSheet("QLabel { color : blue; }")

    def leaveEvent(self, event):
        # Revert to the default font color when the mouse leaves
        self.setStyleSheet("QLabel { color : black; }")
        #self.setText(self.word)  # Optional: revert to original word

    def setFontSize(self, size):
        font = self.font()
        font.setPointSize(size)
        self.setFont(font)



class MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Language Learning App')
       




        self.workingSet= []
        self.fullWorkingSetSize = 8
        #change parameter to adjust number of sentences to put in working set. Must be less than the size of the sentences table
        self.updateWorkingSet(self.fullWorkingSetSize)
        self.initUI()       
        
    
    def updateWorkingSet(self, numberOfSentencesToGet):
        self.workingSet = dbmanager.getSentences(numberOfSentencesToGet)
       # print(self.workingSet)

    def getATupleFromWorkingSet(self) -> tuple:
        tupToGet =  random.randint(0, len(self.workingSet) - 1)
        return self.workingSet[tupToGet]



    def clear_layout(layout):
        # Loop in reverse to avoid shifting indices
        for i in range(layout.count()-1, -1, -1):
            item = layout.itemAt(i)
            widget = item.widget()
            if widget is not None:
                # Remove the widget from the layout
                widget.setParent(None)
                # Delete the widget
                widget.deleteLater()
            

    def initLabels(self, hbox : QHBoxLayout) -> None:
        self.labels.clear()
        tup = self.getATupleFromWorkingSet()
        self.currNorskSentence = tup[0]
        self.currEngSentence = tup[1]
        self.currSentenceID = tup[3]
        dictionary = tup[2]
        for word in dictionary.keys():
             # Create a ClickableLabel for each word
            label = ClickableLabel(word, dictionary.get(word, "N/A"))
            label.clicked.connect(self.on_word_clicked)
            #label.setFontSize(max(self.width() // 50, 10))
            label.setFontSize(14)
            self.labels.append(label)

        
        for i in range(hbox.count()-1, -1, -1):
            item = hbox.itemAt(i)
            if item.widget():
                # Handle QWidget items
                widget = item.widget()
                widget.setParent(None)
                widget.deleteLater()
            elif item.spacerItem():
                # Handle QSpacerItem items
                # No need to delete spacer items, just remove them
                hbox.removeItem(item)
        hbox.addStretch()
        for label in self.labels:
            hbox.addWidget(label)
        hbox.addStretch()
        return hbox

        
    
    

    def initUI(self):
        
        self.setGeometry(100,100,800,900)
        
        #menubar = self.menuBar()
        #saveMenu = menubar.addMenu("Save State")
        #modifySetMenu = menubar.addMenu("Adjust Set Configuration")

        #saveAction = QAction('&Save', self)
        #saveAction.setShortcut('Ctrl+S')
        
        
        
        
        
        
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.addStretch()
        

        self.counterBox = QLabel("Sentences left in set: " + str(len(self.workingSet)))
        
        
        vbox.addWidget(self.counterBox, 0, Qt.AlignCenter)



        #hbox.addStretch()
        
        #self.layout.addStretch()
        #self.setLayout(self.layout)

        #self.layout.addStretch()

        
       

        self.labels = []
        self.buttons = []
        
        hbox = self.initLabels(hbox)

        #for label in self.labels:
        #    hbox.addWidget(label)
            
        #hbox.addStretch()
        vbox.addLayout(hbox)
        self.translatedSentenceBox = QLabel("")
        vbox.addWidget(self.translatedSentenceBox, 0, Qt.AlignCenter)


        translateButton =QPushButton("Translate")
        
        translateButton.clicked.connect(self.on_translate_button_clicked)
        vbox.addWidget(translateButton, 0, Qt.AlignCenter)
        self.buttons.append(translateButton)


        #add progress buttons
        buttonHBox = QHBoxLayout()
        buttonHBox.addStretch()
        didNotLearnButton =QPushButton("I didn't know it :(")
        didNotLearnButton.setStyleSheet("QPushButton { background-color: crimson; }")
        didNotLearnButton.clicked.connect(self.on_dont_know_button_clicked)
        self.buttons.append(didNotLearnButton)
        buttonHBox.addWidget(didNotLearnButton)
        learnedButton = QPushButton("I knew it!")
        learnedButton.setStyleSheet("QPushButton { background-color: lightgreen; }")
        learnedButton.clicked.connect(self.on_knew_it_button_clicked)
        self.buttons.append(learnedButton)
        buttonHBox.addWidget(learnedButton)
        buttonHBox.addStretch()
        vbox.addLayout(buttonHBox)

        changeWorkingSetButton = QPushButton("Randomize the current sentence set")
        changeWorkingSetButton.clicked.connect(self.on_change_set_button_clicked)
        self.buttons.append(changeWorkingSetButton)
        vbox.addWidget(changeWorkingSetButton, 0, Qt.AlignCenter)

        vbox.addStretch()
        self.layout = vbox
        self.setLayout(self.layout)




    def show_message_box(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("End of Set Reached")
        msg_box.setText("Great Job! You finished this set!")
        msg_box.setInformativeText("Click on the randomize button to generate a new set.")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)

        msg_box.buttonClicked.connect(lambda btn: self.on_change_set_button_clicked() if msg_box.standardButton(btn) == QMessageBox.Ok else None)
        msg_box.exec_()  # Show the message box



    def on_change_set_button_clicked(self):
        self.updateWorkingSet(self.fullWorkingSetSize)
        self.counterBox.setText("Sentences left in set: " + str(len(self.workingSet))) 
        self.translatedSentenceBox.setText("")
        hbox = self.layout.itemAt(2)
        self.initLabels(hbox)
        
        
    def on_translate_button_clicked(self):
        if self.translatedSentenceBox.text() == "":
            self.translatedSentenceBox.setText(self.currEngSentence)
            #self.translatedSentenceBox.setFont(QFont("Arial", max(self.width() // 70, 10)))
            self.translatedSentenceBox.setFont(QFont("Arial", 12))
        else:
            self.translatedSentenceBox.setText("")
    
    
    
   
    #TODO interface with db to mark sentences as learned or not
    def on_knew_it_button_clicked(self):
        tupeToRemove = tuple()
        #update database to reflect that sentence was learned
        dbmanager.updateSentenceClass(self.currSentenceID, True)

        if len(self.workingSet) > 1:
            for tup in self.workingSet:
                if self.currNorskSentence == tup[0]:
                    tupeToRemove = tup
            self.workingSet.remove(tupeToRemove)
        else:
            self.show_message_box()
            #self.updateWorkingSet(self.fullWorkingSetSize)
        self.counterBox.setText("Sentences left in set: " + str(len(self.workingSet)))  
        hbox = self.layout.itemAt(2)
        self.initLabels(hbox)
        self.translatedSentenceBox.setText("")


    
    def on_dont_know_button_clicked(self):
        #update database to reflect that sentence was not learned
        dbmanager.updateSentenceClass(self.currSentenceID, False)
        hbox = self.layout.itemAt(2)
        self.initLabels(hbox)
        self.translatedSentenceBox.setText("")



    def on_word_clicked(self):
        # Handle the word click event if needed
        pass

'''
    def resizeEvent(self, event):
        # Call the base class method to ensure the default behavior is preserved
        super().resizeEvent(event)


        self.counterBox.setFont(QFont("Arial", max(self.width() // 100, 8)))
        #resize button and button font
        for button in self.buttons:
            if button.text() == "Translate":
                button.setFixedWidth(self.width() // 3)
                button.setFont(QFont("Arial", max(self.width() // 70, 10)))
            elif button.text() == "Randomize the current sentence set":
                button.setFont(QFont("Arial", max(self.width() // 70, 10)))
            else:
                button.setFixedWidth(self.width() // 5)
                button.setFont(QFont("Arial", max(self.width() // 90, 10)))

       #resize labels 
        # Calculate new font size here based on the window size
        newLabelFontSize = max(self.width() // 60, 10)
        #Calculate new spacing based on font size
        self.layout.setSpacing(newLabelFontSize)
    
        
        for label in self.labels:
            label.setFontSize(newLabelFontSize)
            '''
            

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()



























'''
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()  # Setup the UI elements
        self.connectSignals()  # Connect signals and slots

    def initializeUI(self):
        """Setup the initial UI of the main window."""
        self.setWindowTitle('Toggle Text')
        self.setGeometry(100, 100, 800, 800)

        # Initialize QLabel
        self.label1 = QLabel('Hello, PyQt5!', self)
        self.label1.move(90, 50)
        self.label1.resize(200, 20)

        # Initialize QPushButton
        self.button = QPushButton('Change Text', self)
        self.button.move(90, 100)

        # Toggle state
        self.toggle_state = False

    def connectSignals(self):
        """Connect signals and slots."""
        self.button.clicked.connect(self.toggle_text)

    def toggle_text(self):
        """Toggle the text of the label."""
        if self.toggle_state:
            self.label1.setText('Hello, PyQt5!')
        else:
            self.label1.setText('Text Changed!')
        self.toggle_state = not self.toggle_state




def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

    '''