# Imports the pygetwindow class to check and manipulate the os's active windows
import pygetwindow as apps
# Imports QtWidgets classes which I believe to be necessary for the QtGui library to draw graphics (but not 100% sure on this one)
from PyQt5.QtWidgets import QApplication, QWidget
# Imports QtGui classes that handle drawing overlays and text to the screen
from PyQt5.QtGui import QFont, QFontMetricsF, QPainter, QBrush, QColor, QIcon
# Imports QtCore classes that handle the creation of shapes and timers
from PyQt5.QtCore import QRect, QRectF, Qt, QTimer


class OverlayManager(QWidget):
    
    """
    Class that handles any overlays and debug messages over the game client to visually show objects that the bot can see 
    and to inform the user of the current action that the bot is performing
    """

    # Stores any existing instances of this class to prevent multiple instances being executed simultaneously, a.k.a simple singleton implementation
    instance = None
    # Returns true if there is no self debugMsg currently being displayed
    debugCleared = False
    # Returns true if there are no overlays being displayed
    overlaysCleared = False
    
    
    def __new__(self):
        """
        Method that manages the different instances of this class being created, ensuring only one instance exists at any given time
        """
        
        # Checks if the class instance variable has an instance stored in it
        if not self.instance:
            # Creates a new instance of this class and stores it in the instance attribute
            self.instance = super().__new__(self)
        
        # Returns either the newly created instance of this class or if one previously existed, returns that instance instead
        return self.instance


    def __init__(self):
        """
        Method that creates/initializes any instance variables that this class may require
        """
        
        # Calls the default initialization method to ensure proper initialization behaviour is executed
        super().__init__()
        
        # Set window flags for the overlay to hide it from the taskbar
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        # Set attribute for a translucent background
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Stores the first instance of luna found in the active windows
        self.luna = self.fetchLuna()
        
        # Sets a default overlay/debug color to prevent the paintEvent trying to paint with an undefined color
        self.debugColor = self.textColor = Qt.white
        
        # Stores the debug message that is currently being displayed
        self.debugMsg = None
        
        # List to store each overlay that should be drawn to the screen when the paint event is called
        self.overlayList = []
        
          

    def __drawDebugMsg(self, painter):
        """
        Method to draw a debug message to the screen.
        This method has been __nameMangled to reduce accidental usage outside of this class
        """
        
        try:
            # Returns early if there is no debug message to paint (shouldn't be possible but doesn't hurt to check it anyway)
            if self.debugMsg is None:
                return
        
            # Sets the text properties of the debug message (font style and font size)
            font = QFont("Arial", 9)
            # Applies debug messages text properties to the painter
            painter.setFont(font)
        
            # Defines the texts location and size
            textWidth = QFontMetricsF(font).width(self.debugMsg)
            textHeight = QFontMetricsF(font).height()
            textX = (self.luna.width - textWidth) // 2
            textY = textHeight - textHeight / 1.5
        
            # Defines the textBox in which the debug message will be displayed
            textBox = QRectF(textX, textY, textWidth + 10, textHeight + 10)
            # Draws the textBox to the screen along with the passed debug message
            painter.drawText(textBox, Qt.AlignTop | Qt.AlignLeft, self.debugMsg)
        
        # Catches any errors gracefully
        except Exception as e:
            
            # Informs user that an error has occured
            self.addDebug('Error drawing debug message! Please see console output for more information...')
            # Prints an informative error message to the console
            print(f'Error drawing debug message: {e}')


    def __drawOverlays(self, painter):
        """
        Method to draw each overlay currently stored in the overlayList to the screen.
        This method has been __nameMangled to reduce accidental usage outside of this class
        """
        
        try:
            # Sets the outline color of the overlay grid to match the default color unless another color has been passed
            painter.setPen(QColor(self.overlayColor))
            # Ensures the overlayList is populated before trying to iterate through it
            if self.overlayList:
                # For each grid (overlay) in the overlay list
                for thisGrid in self.overlayList:
                    # Draws this grid to the screen
                    painter.drawRect(thisGrid)
        
        # Catches any errors gracefully
        except Exception as e:
            
            # Informs user that an error has occured
            self.addDebug(f'Error drawing overlays! Please see console output for more information...')
            # Prints an informative error message to the console
            print(f'Error drawing overlay: {e}')
            
    def setOverlayColor(self, newColor):
        """
        Method that changes the color of the overlays
        
         Parameters:
        - color (Qt.color): The desired overlay color
        """
        
        # Sets the overlay paint brush to the passed color
        self.debugColor = QColor(newColor)
        # Calls repaint method to instantly repaint this control
        self.Repaint()
        

    def setDebugColor(self, newColor):
        """
        Method that changes the color of the debug messages
        
         Parameters:
        - color (Qt.color): The desired debug message color
        """
        
        # Sets the debug message paint brush to the passed color
        self.debugColor = QColor(newColor)
        # Calls repaint method to instantly repaint this control
        self.Repaint()

        
    def paintEvent(self, event):
        """
        Overrides the default paintEvent to draw the overlays/debug messages to the screen on paint
        """
        
        try:
            # Calls the parent classes paintEvent to ensure the default painting behaviour is executed
            super().paintEvent(event)
        
            # Creates an painter object to paint the screen with overlays or text
            painter = QPainter(self)
            # Enables antialiasing to smooth out any jagged or pixelated lines or edges
            painter.setRenderHint(QPainter.Antialiasing)
            # Sets the outline color of the overlay grid to match the default color unless another color has been passed
            painter.setPen(QColor(self.debugColor))
            # Sets the fill color to transparent so we can only see the outline of each overlay
            painter.setBrush(QBrush(QColor(0, 0, 0, 0)))
        
            # Draws the debug message to the screen (if one exists)
            self.__drawDebugMsg(painter)
            # Draws each overlay in the overlayList
            self.__drawOverlays(painter)
        
        # Catches any errors gracefully
        except Exception as e:
            
            # Informs user that an error has occured
            self.addDebug(f'Error painting overlays! Please see console output for more information...')
            # Prints an informative error message to the console
            print(f'Error painting overlays: {e}')
    
    
    def checkLuna(self):
        """
        Method that checks if Luna.exe is the current active application, if not, calls another method to handle its activation.
        """
        
        # Checks if the active window contains the string "Luna"
        if "Luna" in apps.getActiveWindow.Title():
            # If luna is already the current active window, returns early
            return
        # Else, if luna is not the current active window
        else:
            # Calls the method that activates the game client
            self.fetchLuna()


    def fetchLuna(self):
        """
        Method that searches all active windows and fetches the first instance of the 
        \"Luna\" game client that is found, then brings it to the foreground and maximizes it
        """
        
        try:
            # Fetches all active instances of the Luna game client and stores them in a list
            lunaList = apps.getWindowsWithTitle("Luna")
        
            # If lunaList is not empty
            if lunaList:
                # Fetches the first instance of Luna.exe that was found and creates a class attribute for it
                self.luna = lunaList[0]
                # Activates and maximizes this instance of Luna.exe
                self.luna.activate()
                self.luna.maximize()
        
                # Creates a transparent canvas overlay over the luna application, matching its dimensions
                # This allows us to draw on top of the app whilst still being able to see and use the app as per normal
                self.setGeometry(self.luna.left, self.luna.top, self.luna.width, self.luna.height)
                # Paints the transparent canvas that was just created
                self.show()
                
                # Writes debug info to the screen informing user that an overlay is being cleared
                self.addDebug(f'Successfully retrieved Luna Client!')
                
                # Returns the active luna application
                return self.luna
            
            # Else if no instances of Luna.exe are found
            else:
                # Raises an exception informing the user that they need to open an instance of Luna.exe first
                raise RuntimeError("Failed to find any instances of the Luna game client! Please ensure there is a \"Luna client\" running before you launch a bot script.")
        
        # Catches any errors gracefully
        except Exception as e:
            
            # Prints an informative error message to the console
            print(f'Error displaying luna app: {e}')
                
        
    def addOverlay(self, overlayX, overlayY, overlayWidth, overlayHeight, overlayRows = 1, overlayColumns = 1, overlayThickness = 2, duration = 3000):
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
        - overlayColor (optional Qt Color): The color of the overlay (default is Qt.white)
        - duration (optional int): The time in milliseconds before the overlay automatically closes (default = 3000, None = Permanent)
        """
        
        try:
            # Writes debug info to the screen informing user that an overlay is being added
            self.addDebug(f'Adding overlay grid at {grid.x()}, {grid.y()}')
            
            # Calls the checkLuna method which ensures a luna game client is the active application before proceeding
            self.checkLuna()

            # Creates a rectangle which represents the outer boundries of this grid using the passed parameters
            self.overlayBox = QRect(overlayX, overlayY, overlayWidth, overlayHeight)
        
            # Stores the grid being drawn inside the for loop 
            # Calculates the width and height of the grid to draw, based on the passed rows and columns
            gridWidth = int(self.overlayBox.width() / self.overlayColumns)
            gridHeight = int(self.overlayBox.height() / self.overlayRows)
        
            # Draws a grid using the passed rows and columns, if no rows or columns were passed, this will create a 1x1 grid by default
            for currentRow in range(self.overlayRows):
                for currentColumn in range(self.overlayColumns):
                
                    # Calculates this position of the grid slot being drawn (or outline if its a 1x1 grid)
                    gridX = currentRow * int(self.overlayBox.width() / self.overlayColumns)
                    gridY = currentColumn * int(self.overlayBox.height() / self.overlayRows)
                
                    # Creates a rectangle representing this grid/grid slot
                    grid = (QRect(gridX, gridY, gridWidth, gridHeight))
                
                    # Adds the created grid/grid slot to the overlay list
                    self.overlayList.append(grid)
                
                    # If the user has not passed 'None' for the duration...
                    if duration:
                        # Starts a single shot timer that will clear this grid after the passed duration in ms has passed.
                        # Note: The "lambda:" expression is preventing the clearOverlay parameters from being prematurely 
                        # evaluated, I don't think it would matter in this situation but it's good practice.
                        QTimer.singleShot(duration, lambda: self.clearOverlay(grid))
                        
        # Catches any errors gracefully
        except Exception as e:
            
            # Informs user that an error has occured
            self.addDebug('Error adding overlay! Please see console output for more information...')
            # Prints an informative error message to the console
            print(f'Error adding overlay: {e}')


    def clearOverlay(self, grid):
        """
        Method to remove an overlay from the screen after its timer has expired
        
         Parameters:
        - grid (Qrect): The grid/grid slot to remove from the overlayList
        """
        
        try:
            # Returns early if the overlayList is empty
            if self.overlaysCleared:
                return
            
            # Writes debug info to the screen informing user that an overlay is currently being cleared
            self.addDebug(f'Attempting to remove overlay at {grid.x()}, {grid.y()}')
            
            # Checks if the overlayList contains the passed grid before attempting to remove it
            if grid in self.overlayList:
                # Sets the passed grid overlay to an empty rectangle in order to delete it from the screen
                grid = QRect()
                # Updates the canvas which will draw all of the overlays contained within the list
                self.update()
                # Removes the passed grid from the overlay list since it is no longer needed
                self.overlayList.remove(grid)
                # Informs user of successful overlay removal
                self.addDebug(f'Successfully removed overlay at {grid.x()}, {grid.y()}')
                
            # Else if the passed grid is not in the overlay list
            else:
                # Informs user of failed overlay removal
                self.addDebug(f'Failed to find overlay in the overlayList! Overlay: x = {grid.x()}, y = {grid.y()}, width = {grid.width()}, height = {grid.height()}')
                return
                        
            # Returns true if there are no overlays left to display
            self.overlaysCleared = not self.overlayList
            # Closes this application if there are no overlays left to draw
            self.tryClose()

        # Catches any errors gracefully
        except Exception as e:
            
            # Informs user that an error has occured
            self.addDebug('Error adding overlay! Please see console output for more information...')
            # Prints an informative error message to the console
            print(f'Error adding overlay: {e}')
    

    def addDebug(self, debugMsg, duration = 3000):
        """
        Paints debug info to the screen to inform the user of the action currently being undertaken by the bot
        
         Parameters:
        - debugMsg (str): The debug message to be displayed at the top of the game client to inform the user of the current process being performed
        - duration (optional int): The time in milliseconds before the overlay is automatically removed (default = 3000, None = Permanent)
        """
        
        try:
            # Return early if no debug message has been passed since there is nothing to display
            if debugMsg is None:
                print('Error: Attempted to paint an empty debug message to the screen!')
                return
        
            # If a debug message is currently being displayed
            if self.debugMsg is not None:
                # Clears the current debug message before displaying the new one to prevent overlapping
                self.clearDebug(self.debugMsg)
                
            # Sets the debug message attribute to match the passed debug message
            self.debugMsg = debugMsg
        
            # Calls the paint method to draw the passed debug message to the screen
            self.update()
            
            # Starts at timer to remove this debug message after the passed amount of time
            QTimer.singleShot(duration, self.clearDebug)
        
        # Catches any errors gracefully
        except Exception as e:
            
            # Informs user that an error has occured
            self.addDebug('Error adding debug message! Please see console output for more information...')
            # Prints an informative error message to the console
            print(f'Error adding debug message: {e}')
        

    def clearDebug(self):
        """
        Method to remove the debug message from the screen after it's timer has expired
        """
        
        # Sets the debug message to an empty string
        self.debugMsg = None
        # Repaints this control to remove the current debug message from the screen
        self.update()
        # Sets boolean to true if there is no debug message currently being displayed
        self.debugCleared = self.debugMsg
        # Closes this application if there are no more overlays left on the screen
        self.tryClose()

    def tryClose(self):
        """
        Method that exits if there are no more overlays to paint on the screen
        """
        
        # Ensures debug message and all overlays have been cleared before exiting
        if self.debugCleared and self.overlaysCleared:
            # Writes close message to console
            print('Overlay Manager tasks complete! Exiting overlay manager...')
            # Resets overlay booleans to prevent them being true the next time this instance is used
            self.debugCleared = self.overlaysCleared = False
            # Exits the event loop, closing this widget
            QApplication.quit()


def test():
    """
    Executes the available functions this class has to offer to ensure they are working correctly.
    This method is only called when executing this class directly as opposed to being imported as a module.
    """
    
    try:
        # Instantiates a QApplication for PyQt compatibility, otherwise the eventLoop will not be able to execute
        Overlay = QApplication([])
        # Sets an empty QIcon to hide the overlay program from the taskbar when the transparent overlay window is opened
        Overlay.setWindowIcon(QIcon())
        
        # Instantiates this class with a test instance
        test = OverlayManager()
        # Tests the debug feature which should draw the passed text on top of the game client
        test.addDebug(debugMsg = 'Initializing script... Please Wait...', duration = 5000)
        # Tests the overlay feature which should draw a rectangle to show the user what the bot is has found
        test.addOverlay(overlayX = 0, overlayY = 0, overlayWidth = 50, overlayHeight = 50, overlayRows = 2, overlayColumns = 2, duration = 1000)
        
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
    #QApplication.exit()