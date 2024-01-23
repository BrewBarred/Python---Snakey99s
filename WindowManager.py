# Imports the pygetwindow class to check and manipulate the os's active windows
import pygetwindow as apps


class WindowManager():
    """
    Class that handles window management such as checking the active windows, bringing the forward and maximizing them etc.,
    """

    @staticmethod
    def activeWindow():
        """
        Returns the current active window
        """
        return apps.getActiveWindow()
    

    @staticmethod
    def activeWindowTitle():
        """
        Returns the current active windows title
        """
        
        return apps.getActiveWindowTitle()
    

    @staticmethod
    def activeLunaClient():
        """
        Returns the active luna client if any exists, else returns none
        """
        
        return WindowManager.activeWindow() if WindowManager.activeWindow().__name__.startswith('Luna - ') else None


    @staticmethod
    def lunaIsActive():
        """
        Method that checks if the current active window is an instance of luna, if not, calls another method to handle its activation
        """
        
        # Returns true if luna is the current active window
        if WindowManager.activeLunaClient():
            return True
        
        # Returns false if luna is not the current active window
        return False
    

    @staticmethod
    def checkLuna():
        """
        Method that checks if the current active window is an instance of luna, if not, calls another method to handle its activation
        """
        
        # Writes debug info to console
        debug('Checking for any open instances of \"Luna\" client...', False)
        
        # Returns early if the current active window is a Luna client
        if WindowManager.activeLunaClient():
            
            # Writes debug info to console
            debug('Active instance of luna detected, fetch method will be bypassed...', False)
            return WindowManager.activeLunaClient()
        
        # Else calls another method to fetch the first instance of Luna found in the active apps
        else:
            
            # Writes debug info to console
            debug('Failed to find active instance of \"Luna\", attempting to fetch a client from active windows...', False)
            # Calls the fetch method to activate the first instance of Luna found in the active windows
            return WindowManager.fetchLuna()


    @staticmethod
    def fetchLuna():
        """
        Method that searches all active windows and fetches the first instance of the 
        \"Luna\" game client that is found, then brings it to the foreground and maximizes it
        """
        
        try:
            # Fetches all active instances of the Luna game client and stores them in a list
            lunaList = [window for window in apps.getWindows() if window.title.startswith("Luna - ")]
        
            # If lunaList is not empty
            if lunaList:
                
                # Fetches the first instance of Luna.exe that was found and creates a class attribute for it
                lunaClient = lunaList[0]
                # Activates and maximizes this instance of Luna.exe
                lunaClient.activate()
                lunaClient.maximize()
        
                # Creates a transparent canvas overlay over the luna application, matching its dimensions
                # This allows us to draw on top of the app whilst still being able to see and use the app as per normal
                lunaClient.setGeometry(WindowManager.activeLunaClient().left, WindowManager.activeLunaClient.top, WindowManager.activeLunaClient.width, WindowManager.activeLunaClient.height)
                # Paints the transparent canvas that was just created
                lunaClient.show()
                
                # Writes debug info to the screen informing user that an overlay is being cleared
                debug(f'Successfully retrieved \"Luna\" client!')
                
                # Returns the active luna application
                return lunaClient
            
            # Else if no instances of Luna.exe are found
            else:
                # Raises an exception informing the user that they need to open an instance of Luna.exe first
                raise RuntimeError("Failed to find any instances of the \"Luna\" game client! Please ensure there is an instance of \"Luna\" running before you launch a bot script.")
        
        # Catches any errors gracefully
        except Exception as e:
            
            # Prints an informative error message to the console
            logError(f'Error displaying luna app: {e}')