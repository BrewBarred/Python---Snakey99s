# Imports overlay manager to manage drawing rectangles 
# and debug messages on top of the Luna.exe application
import OverlayManager
#from ImageChecker import image_checker

class ScriptManager:
    
    def __init__(self):
        # Initializes components required to write scripts
        self.debug = OverlayManager.debug
        self.debug('Initializing script manager... Please wait...')

    def debug(self):
        # Use the imported modules here
        self.debug("Debug message")

    def log(self, message, exception = None):
        # Example method for logging messages
        print(f"Error: {message} \n Exception: {exception}'")

# mining_bot.py
class MiningBot:
    def __init__(self, script_manager):
        self.script_manager = script_manager

    def mine(self):
        # Mining logic goes here
        self.script_manager.log_message("Mining in progress...")
        self.script_manager.run_script()

# Example usage in mining_bot_script.py:
from script_manager import ScriptManager
from mining_bot import MiningBot

script_manager = ScriptManager()
mining_bot = MiningBot(script_manager)

# Use ScriptManager methods to build the mining script
mining_bot.mine()
