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
    Class that handles any overlays and debug messages over the Luna.exe application to visually show objects that the bot can see 
    and to inform the user of the current action that the bot is performing
    """

    # Stores any existing instances of this class to prevent multiple instances being executed simultaneously
    instance = None

    
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
        
        # Calls the default initialization method to ensure the default initialization behaviour is executed
        super().__init__()
        
        # Both of these booleans returns true when there is no screen overlay or debug message currently
        # on the screen. This is what prevents one another from prematurely closing eachother.
        self.overlayCleared = False
        self.debugCleared = False   
        
        # Creates a list to store each overlay that should be drawn to the screen when the paint event is called
        self.overlayList = []
    

    def paintEvent(self, event):
        """
        Overrides the paintEvent handler to draw the overlays/debug messages to the screen
        """
        
        # Calls the parent classes paintEvent to ensure the default painting behaviour is executed
        super().paintEvent(event)
        
        # Creates an painter object to paint the screen with overlays or text
        painter = QPainter(self)
        # Enables antialiasing to smooth out any jagged or pixelated lines or edges
        painter.setRenderHint(QPainter.Antialiasing)
        # Sets the outline color of the rectangles to match the default color unless another color has been passed
        painter.setPen(QColor(self.overlayColor))
        # Sets the fill color to transparent so we can only see the outline of each overlay
        painter.setBrush(QBrush(QColor(0, 0, 0, 0)))
        
        # Draws the debug message to the screen (if one exists)
        self.__drawDebugMsg(painter)
        # Draws each overlay in the overlayList
        self.__drawOverlays(painter)
          

    def __drawDebugMsg(self, painter):
        """
        Method to draw a debug message to the screen.
        This method has been __nameMangled to reduce accidental usage outside of this class
        """
        
        # Returns early if there is no debug message to paint
        if (self.text is None):
            return
        
        # Sets the debug messages text properties (font style and font size)
        font = QFont("Arial", 9)
        # Applies debug messages text properties to the painter
        painter.setFont(font)
        
        # Defines the texts location and size
        textWidth = QFontMetricsF(font).width(self.text)
        textHeight = QFontMetricsF(font).height()
        textX = (self.luna.width - textWidth) // 2
        textY = textHeight - textHeight / 1.5
        
        # Defines the textBox in which the text will be displayed and draws it, along with the text message
        textBox = QRectF(textX, textY, textWidth + 10, textHeight + 10)
        painter.drawText(textBox, Qt.AlignTop | Qt.AlignLeft, self.text)


    def __drawOverlays(self, painter):
        """
        Method to draw each overlay currently stored in the overlayList to the screen.
        This method has been __nameMangled to reduce accidental usage outside of this class
        """
        
        # Ensures the overlayList is populated before trying to iterate through it
        if self.overlayList:
            # For each rectangle (overlay) in the overlay list
            for thisRect in self.overlayList:
                # Draws this rectangle to the screen
                painter.drawRect(thisRect)


    def showLuna(self):
        """
        Method to active the Luna.exe app, bringing it to the foreground and maximizing it
        """
        
        # Fetches all instances of Luna.exe currently running and stores them in a list
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
            
        # Else if no instances of Luna.exe are found
        else:
            # Raises an exception informing the user that they need to open an instance of Luna.exe first
            raise RuntimeError("Failed to find Luna.exe! Please ensure there is a \"Luna\" client running before you launch a bot script.")
    
    
    def checkLuna(self):
        """
        Method that checks if Luna.exe is the current active application, if not, calls another method to handle its activation.
        """
        
        # Checks if the active window contains the string "Luna"
        if "Luna" in apps.getActiveWindow:
            # If the active window contains "Luna", returns early
            return
        # Else, luna must not be the active window
        else:
            # Calls the method that activates the Luna.exe app
            self.showLuna()
                
        
    def addOverlay(self, overlayX, overlayY, overlayWidth, overlayHeight, overlayRows = 1, overlayColumns = 1, overlayThickness = 2, overlayColor = Qt.white, duration = 3000):
        """
        Adds a new overlay on top of the Luna.exe application at the specified location and size for a specified amount of time
        
         Parameters:
        - overlayX (int): The x coordinate of the top-left corner of the overlay
        - overlayY (int): The ycoordinate of the top-left corner of the overlay
        - overlayWidth (int): The total width of the overlay
        - overlayHeight (int): The total height of the overlay
        - overlayRows (optional int): The number of rows in the grid layout of the overlay (default = 1)
        - overlayColumns (optional int): Number of columns in the grid layout of the overlay (default = 1)
        - overlayThickness (optional int): The thickness of the overlay border (default = 2)
        - overlayColor (optional Qt Color): The color of the overlay (default is Qt.white)
        - timeout (optional int): The time in milliseconds before the overlay automatically closes (default = 3000)
        """
        
        # Calls the method that ensures Luna.exe is the active application before proceeding
        self.checkLuna()
        
        # Initializes class attributes for class-wide accessibility
        self.overlayRows = overlayRows
        self.overlayColumns = overlayColumns
        self.overlayColor = overlayColor

        # Creates a rectangle to define the overlay dimensions using the passed parameters for easier reference throughout the class
        self.overlayBox = QRect(overlayX, overlayY, overlayWidth, overlayHeight)
        
        # Set window flags for the overlay to hide it from the taskbar
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        # Set attribute for a translucent background
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        
        
        
        # Calculate the width and height of each rectangle
        rectWidth = int(self.overlayBox.width() / self.overlayColumns)
        rectHeight = int(self.overlayBox.height() / self.overlayRows)
        
         # Draws a grid of tiles representing the inventory if rows/columns have been passed to the addOverlay method, else draws a single rectangle
        for currentRow in range(self.overlayRows):
            for currentColumn in range(self.overlayColumns):
                # Calculates the position for the current rectangle
                rect_x = currentRow * int(self.overlayBox.width() / self.overlayColumns)
                rect_y = currentColumn * int(self.overlayBox.height() / self.overlayRows)
        
                # Creates a QRect for the current rectangle
                rect = QRect(rect_x, rect_y, rectWidth, rectHeight)
        
        # Adds the created overlay to the overlay list so it can be painted later
        self.overlayList.add(rect)
                
        # Starts a single shot timer that will clear this rectangle after the passed duration
        # Note: The "lambda:" expression is preventing the clearOverlay parameters from being 
        # prematurely evaluated, I don't think it would matter in this situation but it's good practice.
        QTimer.singleShot(duration, lambda: self.clearOverlay(rect, duration))



    def clearOverlay(self, rect, duration):
        
        print(f'clear overlay {self.debugCleared}')
        if not self.overlayCleared:
            print('clearing...')
            # Calls the closeEvent method
            self.overlayBox = QRect()
            self.update()
            self.overlayCleared = True
            #self.close()
    


    def debug(self, text, duration = 3000):
        """
        Paints debug info to the top of the screen to inform user of current process
        
        Parameters:
        - text (str): The debug message to be displayed at the top of the Luna.exe client to inform the user of the current process being performed
        """
        
        print('debug')
        # Return early if text is invalid
        if not text:
            return
        
        # Initializes a text attribute for later use by the paint method
        self.text = text
        
        # Calls the paint method to draw the text to the client
        self.update()
        
        QTimer.singleShot(duration, self.clearDebug)
        


    def clearDebug(self):
        
        print(f'clear Debug {self.debugCleared}')
        if not self.debugCleared:
            print('clearing debug...')
            self.text = ""
            #self.update()
            self.debugCleared = True
            self.close()


    # Overrides the closeEvent to ensure all modules properly exit (prevents continous running)
    def closeEvent(self, event):
        """
        Overrides the closeEvent handler to stop the timer and 
        ensure all modules properly exit (prevents continous running).
        """
        print('closeEvent triggered... testing...')
        if (not self.overlayCleared or not self.debugCleared):
            print('test failed, returning early')
            return
        
        self.overlayCleared = False
        self.debugCleared = False
        
        print('test passed, should exit now...')

        # Triggers the closeEvent for the base class
        super().closeEvent(event)
        # Uses the system exit method to stop this script
        QApplication.quit()

def test():
    """
    Executes the available functions this class has to offer to ensure they are working correctly.
    This method is only called when executing this class directly rather than being imported as a module.
    """
    
    try:
        print('test()')
        # Instantiates a QApplication for PyQt compatibility
        Overlay = QApplication([])
        # Sets an empty QIcon to hide the overlay program from the taskbar when the transparent overlay window is opened
        Overlay.setWindowIcon(QIcon())
        
        # Initializes a LunaBot script manager which provides the necessary functions to create a bot script
        LunaBot = OverlayManager()
        # Informs the user of the current process
        LunaBot.debug(text = 'Initializing script... Please Wait...', duration = 5000)
        # Adds an overlay to this script to show the user what the bot is looking at or has found
        LunaBot.addOverlay(overlayX = 0, overlayY = 0, overlayWidth = 50, overlayHeight = 50, overlayRows = 2, overlayColumns = 2, duration = 1000)
        
        # Executes the above instructions
        Overlay.exec_()

    # Else if a RuntimeError occurs
    except RuntimeError as e:
        # Prints an informative error message to the user
        print(f"Error: {e}")
        
# Executes the main function if this class is directly executed as the main program (rather than being imported as a module)
if __name__ == '__main__':
    print('main entry point')
    # Calls the test function of this class
    test()
    print('finished test(), exiting now...')
    QApplication.exit()