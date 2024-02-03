# Imports window manager class to check, access and manipulate active windows
from datetime import datetime
from PyQt5.QtWidgets import QApplication
from WindowManager import WindowManager
# Imports overlay manager to manage drawing rectangles 
# and debug messages on top of the game client
from OverlayManager import OverlayManager
# Imports the debugger class to log error messages and handle raised exceptions
from Debugger import Debugger

class ScriptManager():
    """
    Class that centralizes all of the botting script functions so that all botting 
    scripts will only need to import this one class to string everything together.
    """
    
    # Attribute that toggles debug mode on or off to print statements to the console
    debugMode = False
    lunaClient = None
    overlayManager = None
    

    # python scriptmanager.py
    def __init__(self, debugMode = False):
        """
        Initializes components required for writing scripts
        """
        
        # Writes debug info to console if debugmode is enabled
        print('Initializing script manager... Please wait...')
        # Enables/Disables debug mode based on passed paramater on initialization
        self.debugMode = debugMode
        # Attributes the first found active instead of a luna found in the active windows, this is the client that the scripts will be applied to
        debugMsg, self.lunaClient = WindowManager.getLunaClient()
        # Checks if an error was raised
        if debugMsg is not None:
            # Prints any returned error messages
            self.logError(debugMsg)
        # Sets an attribute for an instance of the overlay manager whilst passing it the active luna client
        self.overlayManager = OverlayManager(self.lunaClient)
        

    def getLunaClient(self):
        """
        Method that checks if the current active window is an instance of luna, if not, calls another method to handle its activation
        """
        
        if self.debugMode:
            # Writes debug info to console
            self.debug('Checking for any open instances of \"Luna\" client...')

        # Returns the first active instance of luna if any exist
        debugInfo, lunaClient = WindowManager.checkLuna()
        
        # If no active instances of luna could be found
        if lunaClient is None:
            
            # If debug mode is enabled
            if self.debugMode:
                # Writes debug info to console
                self.logError(debugInfo)
        
        # Else calls another method to fetch the first instance of Luna found in the active apps
        else:
            
            # Calls the fetch method to activate the first instance of Luna found in the active windows
            return ('Successfully retrieved an active \"Luna\" client!'), lunaClient

        
    def getDebugMode(self):
        """
        Returns whether or not debugMode is currently enabled
        """
        
        return self.debugMode


    def setDebugMode(self, debugBool = None):
        """
        Sets the debugMode of the passed boolean, if no boolean is passed, toggles the debugMode to it's opposite state
        
         Parameters:
        - debugBool (optional bool): True if debugMode should be toggled on, False if debugMode should be toggled off
        """
        
        # If a debugBool was passed, sets debugMode to match the passed bool, else toggles debugMode to its opposite state
        self.debugMode = not self.debugMode if debugBool is None else debugBool
        # Ignores debugMode and prints new debug status straight to the console
        print(f"Debug mode has been {'enabled' if self.debugMode else 'disabled'}")
    
    
    def addOverlay(self, overlayX, overlayY, overlayWidth, overlayHeight, overlayRows = 1, overlayColumns = 1, overlayThickness = 2, overlayDelay = 3000):
        """
        Adds a new overlay on top of the game client at the specified location and size for a specified amount of time
        
         Parameters:
        - overlayX (int): The x coordinate of the top-left corner of the overlay
        - overlayY (int): The ycoordinate of the top-left corner of the overlay
        - overlayWidth (int): The total width of the overlay
        - overlayHeight (int): The total height of the overlay
        - overlayRows (optional int): The number of rows in the grid layout of the overlay (default = 1)
        - overlayColumns (optional int): Number of columns in the grid layout of the overlay (default = 1)
        - overlayThickness (optional int): The thickness of the overlay border (default = 2)
        - overlayDelay (optional int): The time in milliseconds before the overlay automatically closes (default = 3000, None = Permanent)
        """
        
        try:
            
            # Uses the overlaymanager to add an overlay to the screen
            overlayResult = self.overlayManager.addOverlay(overlayX, overlayY, overlayWidth, overlayHeight, overlayRows, overlayColumns, overlayThickness, overlayDelay)
            
            # If the overlay manager returns an error
            if overlayResult:
                # Logs the error
                self.logError(overlayResult)

        # Catches any errors gracefully
        except Exception as e:
            
            # Prints an informative error message to the console
            self.logError (f'Error calling add overlay method: {e}')
    
        
    def debug(self, debugMsg, drawDebug = True, delay = 1500):
        """
        Paints debug info to the screen to inform the user of the action currently being undertaken by the bot
        
         Parameters:
        - debugMsg (str): The debug message to be displayed at the top of the game client to inform the user of the current process being performed
        - drawDebug (optional bool): False if this debug message should not be drawn to the screen, else true (default = True)
        - delay (optional int): The time in milliseconds before the overlay is automatically removed (default = 1500, None = Permanent)
        """
        
        try:
            # If no debug message has been passed, there is no need to execute this method
            if debugMsg is None:
                return
                
            # If this debug message should be drawn to the console too
            if self.debugMode:
                # Uses Debugger class to print messages to the console
                Debugger.debug(debugMsg)
                
            # Ensures luna is still the active window before drawing overlays
            if not WindowManager.lunaIsActive:
                # Fetches the first active instance of luna
                getClientError, self.lunaClient = WindowManager.getLunaClient
                # If the getLunaClient method returns an error
                if getClientError:
                    # sends error message to debugger
                    self.logError(getClientError)
                    
            # If this debug message should be painted to the screen
            if drawDebug:
                
                # Uses Overlaymanager class to draw debug messages to the screen
                debugError = self.overlayManager.addDebug(debugMsg, delay)
                # If the debug function returns a fatal error
                if debugError:
                    # Logs the error to the console and exits
                    self.logError(debugError)
                
        # Catches any errors gracefully
        except Exception as e:
            
            # Prints an informative error message to the console
            self.logError(f'Error handling debug message: {e}')
    

    def logError(self, errorMsg):
        """
        Method that writes an error to the console then quits the application to ensure it exits after an exception is handled
        
         Parameters:
        - errorMsg (str): The error message to print to the console before exiting
        """
        
        # Returns early if no error message has been provided to avoid calling debugger class for no reason
        if errorMsg is None:
            return
        
        # Sends debug message to debugging class to print error and exit
        Debugger.logError(f"Error: {errorMsg}")
        
def test():
    """
    Executes the available functions this class has to offer to ensure they are working correctly.
    This method is only called when executing this class directly as opposed to being imported as a module.
    """
    
    try: 
        # Instantiates a QApplication for PyQt compatibility, otherwise, the eventLoop will not be able to execute
        Overlay = QApplication([])
        # Sets an empty QIcon to hide the overlay program from the taskbar when the transparent overlay window is opened
        #Overlay.setWindowIcon(QIcon())
        
        # Instantiates the ScriptManager class with a test instance
        test = ScriptManager(debugMode=True)
        
        print(f'Started debug timer @ {datetime.now()}')
        
        # Tests the debug feature which should draw the passed text on top of the game client
        test.debug(debugMsg='Testing scripts... Please Wait...', delay=4200)
        print(f'Started overlay timer @ {datetime.now()}')
        # Tests the overlay feature which should draw a rectangle to show the user what the bot has found
        test.addOverlay(overlayX=0, overlayY=0, overlayWidth=500, overlayHeight=500, overlayRows=2, overlayColumns=2, overlayDelay=2500)
        
        # Executes the above instructions
        Overlay.exec_()

    # Else if a RuntimeError occurs
    except RuntimeError as e:
        
        # Prints an informative error message to the user
        print(f"Error performing test: {e}")
        
# Executes the test() function if this class is directly executed as the main program (rather than being imported as a module)
if __name__ == '__main__':
    # Calls the test function of this class
    test()