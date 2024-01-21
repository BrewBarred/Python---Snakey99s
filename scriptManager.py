# Imports overlay manager to manage drawing rectangles 
# and debug messages on top of the Luna.exe application
from PyQt5.QtWidgets import QApplication
import OverlayManager
#from ImageChecker import image_checker

class ScriptManager:
    
    def __init__(self):
        # Initializes components required to write scripts
        self.app = QApplication([])
        self.debug = OverlayManager.debug
        self.debug('Initializing script manager... Please wait...')

    def debug(self):
        # Use the imported modules here
        self.debug("Debug message")

    def log(self, message, exception = None):
        # Example method for logging messages
        print(f"Error: {message} \n Exception: {exception}'")
