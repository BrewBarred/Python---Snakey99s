# This is required to instantiate the OverlayManager class
from PyQt5.QtWidgets import QApplication
# Imports window manager class to check, access and manipulate active windows
from WindowManager import WindowManager
# Imports overlay manager to manage drawing rectangles and debug messages on top of the game client
from OverlayManager import OverlayManager
# Imports the debugger class to log error messages and handle raised exceptions
from Debugger import Debugger
# Imports the mouse manager class to handle automatic mouse movements/actions
from MouseManager import MouseManager


class ScriptManager():
    """
    Class that centralizes all of the botting script functions so that all botting 
    scripts will only need to import this one class to string everything together.
    """


    """       -----------------------       """
    ##!         Script Manager Functions:        
    """       -----------------------       """


    
    def __init__(self, debugMode = False):
        """
        Initializes components required for writing scripts
        """
        
        # Writes debug info to console if debugmode is enabled
        print('Initializing script manager...')
        # Enables/Disables debug mode instance attribute based on passed paramater
        self._debugMode = debugMode
        # Sets the first found active instance of a luna client found in the active windows as an instance attribute, this is the client that the scripts will be applied to
        debugMsg, self._lunaClient = WindowManager.getLunaClient()
        # Checks if an error was raised
        if debugMsg is not None:
            # Prints any returned error messages
            self.logError(debugMsg)
        # Creates an instance attribute for the overlay manager which will handle drawing overlays/debug messages to the client
        self._overlayManager = OverlayManager(self._lunaClient)
        # Creates an instance attribute for the mouse manager which will handle automated mouse movements/actions
        self._mouse = MouseManager(self._lunaClient)


    def debugMode(self, debugMode = None):
        """
        Gets or sets the debugMode boolean If no debugMode boolean is passed, this function will return the current debugMode state (True or False)
        
         Parameters:
        - debugMode (optional bool): True if debugMode should be toggled on, False if debugMode should be toggled off
        
         Returns:
        - The current debugMode state (True or False) if no boolean was passed, else returns None by default
        """
        
        # If no debugMode boolean was passed
        if debugMode is None:
            # Returns the current debugMode
            return self._debugMode
        
        else:
            
            # Else if a debugMode boolean 'was' passed, sets debugMode to match the passed bool
            self._debugMode = debugMode
            # Force prints the debugMode to be written to console (otherwise when being disabled there will be no confirmation message)
            print(f"Debug mode has been {'enabled' if self._debugMode else 'disabled'}!")
    
    
    
    """       -----------------------       """
    ##!         Window Manager Functions:        
    """       -----------------------       """



    def getLunaClient(self):
        """
        Method that checks if the current active window is an instance of luna, if not, calls another method to handle its activation
        """
        
        # If debugMode is enabled
        if self._debugMode:
            # Writes debug info to console
            self.drawDebug('Checking for any open instances of \"Luna\" client...')

        # Returns the first active instance of luna if any exist
        debugInfo, lunaClient = WindowManager.checkLuna()
        
        # If no active instances of luna could be found
        if lunaClient is None:
            
            # If debug mode is enabled
            if self._debugMode:
                # Writes debug info to console
                self.logError(debugInfo)
        
        # Else calls another method to fetch the first instance of Luna found in the active apps
        else:
            
            # Calls the fetch method to activate the first instance of Luna found in the active windows
            return ('Successfully retrieved an active \"Luna\" client!'), lunaClient
    
    
    
    """       ------------------------       """
    ##!         Overlay Manager Functions:        
    """       ------------------------       """
   
    
            
    def setDebugColor(self, newColor = 'white'):
        """
        Sets the color of the debug overlays
        
         Parameters:
        - color (QColor str): The desired overlay color (default = 'white')
        """
            
        # Sets the debug paint brush to the passed color
        colorError = self._overlayManager.setDebugColor(newColor)
        
        # If an error message is returned
        if colorError:
            # Throws error
            self.logError(colorError)
            

    def drawDebug(self, debugMsg, drawDebug = True, delay = 1500):
        """
        Paints debug info to the screen to inform the user of the action currently being undertaken by the bot
        
         Parameters:
        - debugMsg (str): The debug message to be displayed at the top of the game client to inform the user of the current process being performed
        - drawDebug (optional bool): False if this debug message should not be drawn to the screen, else true (default = True)
        - delay (optional int): The time in milliseconds before the overlay is automatically removed (default = 1500, None = Permanent)
        """
        
        try:
            
            # If no debug message has been passed, returns early
            if debugMsg is None:
                return
            
            # Uses Debugger class to print messages to the console if debug mode is enabled
            self.debug(debugMsg)
            
            # Ensures luna is still the active window before drawing overlays
            if not WindowManager.lunaIsActive():
                
                # Fetches the first active instance of luna
                getClientError, self._lunaClient = WindowManager.getLunaClient()
                # If the getLunaClient method returns an error
                if getClientError:
                    # sends error message to debugger
                    self.logError(getClientError)
                    
            # If this debug message should be painted to the screen
            if drawDebug:
                
                # Runs the overlay managers add debug method to handle the debug drawing on-screen
                debugError = self._overlayManager.addDebug(debugMsg, delay)
                # If the debug function returns a fatal error
                if debugError:
                    # Logs the error to the console and exits
                    self.logError(debugError)
                
        # Catches any errors gracefully
        except Exception as e:
            
            # Prints an informative error message to the console
            self.logError(f'Error handling debug message: {e}')
            

    def setOverlayColor(self, newColor = 'white'):
        """
        Sets the color of the overlays
        
         Parameters:
        - color (QColor str): The desired overlay color (default = 'white')
        """
            
        # Sets the overlay paint brush to the passed color
        colorError = self._overlayManager.setOverlayColor(newColor)
        
        # If an error message is returned
        if colorError:
            # Throws error
            self.logError(colorError)


    def drawOverlay(self, overlayX = 0, overlayY = 0, overlayWidth = 200, overlayHeight = 200, overlayRows = 1, overlayColumns = 1, overlayThickness = 2, overlayDelay = 3000):
        """
        Adds a new overlay on top of the game client at the specified location and size for the specified amount of time
        
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
            
            # Uses the overlay manager to add an overlay to the screen
            overlayResult = self._overlayManager.addOverlay(overlayX, overlayY, overlayWidth, overlayHeight, overlayRows, overlayColumns, overlayThickness, overlayDelay)
            
            # If the overlay manager returns an error
            if overlayResult:
                # Logs the error
                self.logError(overlayResult)

        # Catches any errors gracefully
        except Exception as e:
            
            # Prints an informative error message to the console
            self.logError(f'Error calling add overlay method: {e}')
    
    
    
    """       ------------------       """
    ##!         Debugger Functions:         
    """       ------------------       """    
    
    

    def debug(self, debugMsg):
        """
        Calls the debugger class to write debug info to the console
        """
        
        # If this debug message should be drawn to the console too
        if self._debugMode:
            # Uses Debugger class to print messages to the console
            Debugger.debug(debugMsg)


    def logError(self, errorMsg):
        """
        Calls the debugger class to write an error to the console then quits the application to ensure it exits when an exception has been raised
        
         Parameters:
        - errorMsg (str): The error message to print to the console before exiting
        """
        
        # Returns early if no error message has been provided to avoid calling debugger class for no reason
        if errorMsg is None:
            self.drawDebug('Empty error message was passed to logger so the logError function has ignored it and returned early', False)
            return
        
        # Sends debug message to debugging class to print error and exit
        Debugger.logError(f"Error: {errorMsg}")
        


    """       --------------       """
    ##!         Test Function:        
    """       --------------       """    
    
    

async def __test():
    """
    Executes the available functions this class has to offer in order to ensure that they are working correctly.
    
    This method is automatically called when executing this class directly from a command line
    """
    
    try:
        
        ### INITIALIZE COMPONENTS ###
        
        # Instantiates a QApplication for PyQt compatibility, otherwise, the eventLoop will not be able to execute
        Overlay = QApplication([])
        # Instantiates the ScriptManager class with a test instance
        test = ScriptManager(debugMode=True)
        
        ### OVERLAYMANAGER FUNCTION TESTS ###
        
        test.debug('\nScript Manager is now testing the overlaymanagers drawDebug function...')
        # Tests the debug feature which should draw the passed text on top of the game client
        test.drawDebug(debugMsg='Testing scripts... Please Wait...', delay=2000)
        # Tests the default overlay function with no kwargs passed
        test.drawOverlay()
        print('Overlay with default parameters should now be visible on-screen in the top left corner of the client')
        test.setOverlayColor('red')
        test.setDebugColor('green')
        print(f'Overlay colors have been changed! Overlay Color = Red, Debug Color = Green')
        # Tests the overlay feature with some kwargs passed
        test.drawOverlay(overlayX=500, overlayY=500, overlayWidth=100, overlayHeight=100, overlayRows=4, overlayColumns=4, overlayDelay=5000)
        print('Overlay with passed kwargs should now be visible on-screen in red and debug messages should be green now.')
        
        ### SCRIPT MANAGER FUNCTION TESTS ###
        
        test.debug('\nScript Manager is now testing the local debugMode getter/setter...')
        # Tests that debug mode can be disabled
        test.debugMode(False)
        # Calls the default debugMode function to check that it returns the current debugMode correctly
        print(f'Debug mode: {test._debugMode} (Should be False) \n')
        # Tests that debug mode can be enabled again
        test.debugMode(True)
        # Calls the default debugMode function to check that it returns the current debugMode correctly
        print(f'Debug mode: {test._debugMode} (Should be True) \n')
        
        # Executes the above instructions
        Overlay.exec_()
        
        ### DEBUGGER FUNCTION TESTS ###
        
        # Had to test the debugger functions after the event loop to prevent the paint event being blocked by the logError function exiting the QApplication before painting
        test.debug('Script test has been successfully completed! Application should now exit via the logError function...')
        test.logError('High risk of happy coding detected! Exiting test function before it\'s too late...')

    # Else if a RuntimeError occurs
    except RuntimeError as e:
        
        # Prints an informative error message to the user
        print(f"Error performing test: {e}")
        
# Executes the test() function if this class is directly executed as the main program (rather than being imported as a module)
if __name__ == '__main__':
    # Calls the test function of this class
    __test()
