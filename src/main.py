import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMenu, QAction, QVBoxLayout, QWidget, QLabel

# Mode specific layout classes
class Mode1Layout(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("This is Mode 1")
        layout.addWidget(label)
        self.setLayout(layout)

class Mode2Layout(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("This is Mode 2")
        layout.addWidget(label)
        self.setLayout(layout)

class Mode3Layout(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("This is Mode 3")
        layout.addWidget(label)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Language Learning App')
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height

        # Set central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Create mode switch buttons
        self.mode1_button = QPushButton('Mode 1', self)
        self.mode2_button = QPushButton('Mode 2', self)
        self.mode3_button = QPushButton('Mode 3', self)
        
        # Connect buttons to the switch_mode method with the corresponding layout class
        self.mode1_button.clicked.connect(lambda: self.switch_mode(Mode1Layout))
        self.mode2_button.clicked.connect(lambda: self.switch_mode(Mode2Layout))
        self.mode3_button.clicked.connect(lambda: self.switch_mode(Mode3Layout))
        
        # Add buttons to the main layout
        self.main_layout.addWidget(self.mode1_button)
        self.main_layout.addWidget(self.mode2_button)
        self.main_layout.addWidget(self.mode3_button)

        # Menu Bar setup
        menubar = self.menuBar()
        change_mode_menu = menubar.addMenu('Change Mode')

        # Add mode actions to menu
        self.add_mode_action(change_mode_menu, 'Mode 1', Mode1Layout)
        self.add_mode_action(change_mode_menu, 'Mode 2', Mode2Layout)
        self.add_mode_action(change_mode_menu, 'Mode 3', Mode3Layout)

    def add_mode_action(self, menu, mode_name, mode_class):
        action = QAction(mode_name, self)
        action.triggered.connect(lambda: self.switch_mode(mode_class))
        menu.addAction(action)

    def switch_mode(self, mode_class):
        # Clear the existing layout content
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Load the new mode layout
        mode_layout = mode_class()
        self.main_layout.addWidget(mode_layout)

# Application setup
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
