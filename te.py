import sys  # Importing the sys module for system-specific parameters and functions
from datetime import datetime  # Importing the datetime module for working with dates and times

from PyQt5.QtCore import QThread, pyqtSignal as Signal  # Importing necessary classes from PyQt5.QtCore
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QTextEdit, QLabel,
                             QHBoxLayout, QPushButton, QWidget)  # Importing necessary classes from PyQt5.QtWidgets


class MainWindow(QMainWindow):  # Defining a class named MainWindow which inherits from QMainWindow
    splash_text_signal = Signal(str)  # Defining a signal named splash_text_signal
    
    """Main window class, the main window of the application."""
    
    def __init__(self):  # Constructor method for MainWindow class
        """Initializes the main window object."""
        super().__init__()  # Calling the constructor of the parent class (QMainWindow)
        # Set the window title and size
        self.setWindowTitle("Thread Test")  # Setting the window title
        self.setFixedWidth(800)  # Setting the fixed width of the window
        self.setFixedHeight(600)  # Setting the fixed height of the window

        # Create the main widget and set the layout
        main_layout = QVBoxLayout()  # Creating a vertical box layout
        main_layout.addWidget(QLabel("Thread test"))  # Adding a label to the layout

        panel_layout = QHBoxLayout()  # Creating a horizontal box layout
        self.toggle_button = QPushButton("Start")  # Creating a push button with label "Start"
        self.toggle_button.clicked.connect(self.toggle_thread)  # Connecting button click event to toggle_thread method

        panel_layout.addWidget(self.toggle_button)  # Adding the button to the layout
        main_layout.addLayout(panel_layout)  # Adding the layout to the main layout

        self.text_widget = QTextEdit()  # Creating a text edit widget
        self.text_widget.setReadOnly(True)  # Setting the text widget to read-only mode

        main_layout.addWidget(self.text_widget)  # Adding the text widget to the main layout

        main_widget = QWidget()  # Creating a main widget
        main_widget.setLayout(main_layout)  # Setting the main layout for the main widget
        self.setCentralWidget(main_widget)  # Setting the central widget of the main window to the main widget
        self.show()  # Displaying the main window

        # Create the thread worker object and the thread
        self.worker_object = Worker()  # Creating an instance of Worker class
        self.worker_object.text_signal.connect(self.update_text)  # Connecting worker's signal to update_text method

        self.thread_operator = QThread()  # Creating an instance of QThread
        self.worker_object.moveToThread(self.thread_operator)  # Moving worker object to the thread

        # We link the starting of the thread to the run function
        ### WARNING: This cannot be done manually, if you do it manually, the threads will lock up
        ### you can try this by commenting the following line, then uncommenting the line in toggle_thread
        self.thread_operator.started.connect(self.worker_object.run)  # Connecting thread start to worker's run method

    def toggle_thread(self):  # Method to toggle the thread
        # Check if the thread is running
        if self.thread_operator.isRunning():  # Checking if the thread is running
            # If it is running, stop it
            self.worker_object.stop()  # Stopping the worker thread
            self.thread_operator.quit()  # Quitting the thread
            self.toggle_button.setText("Start")  # Setting the button text to "Start"
        else:
            self.thread_operator.start()  # Starting the thread
            ### Uncomment this line to see the threads lock up
            #self.thread_operator.run()  # Running the thread (this is incorrect and should not be done)
            self.toggle_button.setText("Stop")  # Setting the button text to "Stop"
    
    
    def update_text(self, text):  # Method to update the text widget with received text
        self.text_widget.append(text)  # Appending text to the text widget

class Worker(QThread):  # Defining a class named Worker which inherits from QThread
    text_signal = Signal(str)  # Defining a signal named text_signal
    
    def __init__(self, parent=None):  # Constructor method for Worker class
        super().__init__(parent)  # Calling the constructor of the parent class (QThread)
        self.running = True  # Initializing a boolean variable to True indicating the thread is running
    
    def run(self):  # Method representing the main functionality of the worker thread
        self.text_signal.emit("Thread started")  # Emitting a signal indicating the thread is started
        self.running = True  # Setting the running flag to True
        while self.running:  # Looping while the running flag is True
            self.text_signal.emit(f"Time is: {datetime.now()}")  # Emitting the current time
            self.sleep(1)  # Sleeping for 1 second
    
    def stop(self):  # Method to stop the worker thread
        self.running = False  # Setting the running flag to False
        self.text_signal.emit("Thread stopped")  # Emitting a signal indicating the thread is stopped


app = QApplication([])  # Creating an instance of QApplication
window = MainWindow()  # Creating an instance of MainWindow
sys.exit(app.exec_())  # Executing the application event loop and exiting the program when it's done
