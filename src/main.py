import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMenu, QAction, QVBoxLayout, QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from modes.RegularModeLayout import RegularModeLayout
from modes.TargetedModeLayout import TargetedModeLayout
from modes.ListeningModeLayout import ListeningModeLayout
from PyQt5.QtCore import QThread, pyqtSignal

import datafiles.data_service as data_service

class DatabaseWorker(QThread):
    finished = pyqtSignal()  # Signal to indicate completion

    def __init__(self, db_function, *args, **kwargs):
        super().__init__()
        self.db_function = db_function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        # Call the existing database operation function with provided arguments
        try:
            self.db_function(*self.args, **self.kwargs)
        except Exception as e:
            print(f"Error during database operation: {e}")
        finally:
            self.finished.emit()  # Emit the finished signal when done


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.startBackgroundTask()

    def startBackgroundTask(self):
        # Initialize and start the worker thread
        self.db_worker = DatabaseWorker(data_service.get_sounds_for_all_sentences)
        self.db_worker.finished.connect(self.onBackgroundTaskFinished)
        self.db_worker.start()


    #Stub, might need later
    def onBackgroundTaskFinished(self):
        print("Database update completed!")


    def initUI(self):
        self.setWindowTitle('Language Learning App')
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height

        # Set central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        self.main_layout.addStretch()

        # Create mode switch buttons
        self.mode1_button = QPushButton('Regular Mode', self)
        self.mode2_button = QPushButton('Targeted Mode', self)
        self.mode3_button = QPushButton('Listening Mode', self)
        
        # Connect buttons to the switch_mode method with the corresponding layout class
        self.mode1_button.clicked.connect(lambda: self.switch_mode(RegularModeLayout))
        self.mode2_button.clicked.connect(lambda: self.switch_mode(TargetedModeLayout))
        self.mode3_button.clicked.connect(lambda: self.switch_mode(ListeningModeLayout))
        
        # Add buttons to the main layout
        self.main_layout.addWidget(self.mode1_button, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.mode2_button, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.mode3_button, alignment=Qt.AlignCenter)

        self.main_layout.addStretch()

        # Menu Bar setup
        menubar = self.menuBar()
        change_mode_menu = menubar.addMenu('Change Mode')

        # Add mode actions to menu
        self.add_mode_action(change_mode_menu, 'Regular Mode', RegularModeLayout)
        self.add_mode_action(change_mode_menu, 'Targeted Mode', TargetedModeLayout)
        self.add_mode_action(change_mode_menu, 'Listening Mode', ListeningModeLayout)

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
