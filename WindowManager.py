# Imports the pygetwindow class to check and manipulate the os's active windows
import pygetwindow as apps
# Imports win32gui to handle the activation/maximization of the fetched luna client
import win32gui as appControls

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
    def getLunaClient():
        """
        Returns the active luna client if any exists, otherwise, calls the fetchLuna() function to attempt to fetch the first found instance of it
        """
        
        # Get the currently active window using pygetwindow
        activeWindow = WindowManager.activeWindow()

        # Check if an active window exists and its title starts with 'Luna -'
        if activeWindow and activeWindow.title.startswith('Luna - '):
            # If the conditions are met, return the active Luna client
            return ('Active instance of luna already exists, bypassing fetch method...'), activeWindow
        
        # Else if no active luna window exists
        else:
            
            # Calls the fetchluna method to return an error message (if any errors occur) along with the fetched lunaClient (if any is found)
            return WindowManager.fetchLuna()

    @staticmethod
    def lunaIsActive():
        """
        Returns true if luna is the current active window, else returns false
        """
        
        return WindowManager.getLunaClient() is not None
    

    @staticmethod
    def checkLuna():
        """
        Method that checks if the current active window is an instance of luna, if not, calls another method to handle its activation
        """
        
        # Returns early if the current active window is a Luna client
        if WindowManager.getLunaClient() is not None:
            # Writes debug info to console
            return ('Active instance of luna detected, fetch method will be bypassed...'), WindowManager.getLunaClient()
        
        # Else calls another method to fetch the first instance of Luna found in the active apps
        else:
            
            # Writes debug info directly to console
            print('Failed to find active instance of \"Luna\", attempting to fetch a client from active windows...')
            # Calls the fetch method to activate the first instance of Luna found in the active windows or return none with a debug message
            return None, WindowManager.fetchLuna()


    @staticmethod
    def fetchLuna():
        """
        Method that searches all active windows and fetches the first instance of the 
        \"Luna\" game client that is found, then brings it to the foreground and maximizes it
        """
        
        try:
            # Fetches all active instances of the Luna game client and stores them in a list
            lunaList = [window for window in apps.getAllWindows() if window.title.startswith("Luna")]
            
            # If lunaList is not empty
            if lunaList:
            
                # Fetches the first instance of Luna.exe that was found and creates a class attribute for it
                lunaClient = lunaList[0]

                # Activates and maximizes this instance of Luna.exe
                lunaClient.activate()
                lunaClient.maximize()
                
                # Paints the transparent canvas that was just created
                lunaClient.show()
                
                # Returns the a debug message and the fetched luna client
                return None, lunaClient
            
            # Else if no instances of Luna.exe are found
            else:
                # Raises an exception informing the user that they need to open an instance of Luna.exe first
                return ("Failed to find any instances of the \"Luna\" game client! Please ensure there is an instance of \"Luna\" running before you launch a bot script."), None
        
        # Catches any errors gracefully
        except Exception as e:
            
            # Prints an informative error message to the console
            return (f'Error displaying luna app: {e}'), None