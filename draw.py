# Import sys to handle system functions such as sys.exit()
import sys
# Imports class to check active windows and bring Luna.exe to the front and maximised
import pygetwindow as apps
# Import the class to handle drawing graphics and text on screen
from PyQt5.QtGui import QFont, QFontMetricsF, QPainter, QBrush, QColor, QIcon
# Import classes to setup a timer to close overlays or 
from PyQt5.QtCore import QCoreApplication, QRect, QRectF, Qt, QTimer
# Importing classes for building the structure of the GUI (overlay)
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget



# Define a class named GameOverlay, inheriting from the QWidget class
class OverlayManager(QWidget):
    
    """
    Handles any overlays and debug messages over the Luna.exe 
    application to visually show any object targets and to inform 
    the user of the current process being performed by the bot.
    """
    
    # Constructor method for the GameOverlay class
    def __init__(self):
        """
        Initializes a new script manager to handle overlays and debug messages over the Luna.exe application
        """
        # Calls the constructor of the base class (QWidget) to initialize the object
        super().__init__()
        


    def addOverlay(self, overlayX, overlayY, overlayWidth, overlayHeight, overlayRows = 1, overlayColumns = 1, overlayThickness = 2, overlayColor = Qt.white, timeout = 3000):
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

        # Create a new instance of a timer to remove overlay after specified time
        self.timer = QTimer(self)
        # Instructs timer to close this script on timeout
        self.timer.timeout.connect(self.close)
        # Instructs timer to timeout after a specified amount of milliseconds (default = 1000ms)
        self.timer.start(timeout)
        
        # Check if Luna.exe is running and assigns the first instance of it as a class attribute
        luna = apps.getWindowsWithTitle("Luna")
        
        # Checks if an instance of Luna exists and fetches the first
        # first instance of it if more than one client is currently running
        if luna and len(luna) > 0:
            self.luna = luna[0]
            # Activates and maximizes
            self.luna.activate()
            self.luna.maximize()
        
            # Creates a transparent canvas overlay to match the size of the primary screen
            self.setGeometry(self.luna.left, self.luna.top, self.luna.width, self.luna.height)
            self.show()
            
        # Else if no instances of Luna.exe are found
        else:
            # Raise an exception if no instance of Luna.exe is found
            raise RuntimeError("Failed to find Luna.exe! Please ensure there is a \"Luna\" client running before you launch a bot script.")
        
        # Returns this overlay object to allow for later manipulation (not that any manipulation is necessary)
        return self
    


    def debug(self, text):
        """
        Paints debug info to the top of the screen to inform user of current process
        
        Parameters:
        - text (str): The debug message to be displayed at the top of the Luna.exe client to inform the user of the current process being performed
        """
        
        # Return early if text is invalid
        if not text:
            return
        # Calls the paint method to draw the text to the client
        self.update()
        # Initializes a text attribute for later use by the paint method
        self.text = text



    def paintEvent(self, event):
        """
        Overrides the paintEvent handler to draw overlay on top of all other windows
        """
        
        # Initialize painter object to paint overlay with
        overlay = QPainter(self)
        overlay.setRenderHint(QPainter.Antialiasing)
        
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

                # Draws a rectangle filled by a transparent brush so we can only see the outline
                overlay.setPen(QColor(self.overlayColor))
                overlay.setBrush(QBrush(QColor(0, 0, 0, 0)))
                overlay.drawRect(rect)
                
        # Initialize painter object to paint text with
        painter = QPainter(self)

        # Defines the texts design properties
        font = QFont("Arial", 9)
        painter.setFont(font)
        painter.setPen(Qt.white)
        
        # Defines the texts location and size
        textWidth = QFontMetricsF(font).width(self.text)
        textHeight = QFontMetricsF(font).height()
        textX = (self.luna.width - textWidth) // 2
        textY = textHeight - textHeight / 1.5
        
        # Defines the textBox in which the text will be displayed and draws it, along with the text message
        textBox = QRectF(textX, textY, textWidth + 10, textHeight + 10)
        painter.drawText(textBox, Qt.AlignTop | Qt.AlignLeft, self.text)

             
    
    # Overrides the closeEvent to ensure all modules properly exit (prevents continous running)
    def closeEvent(self, event):
        """
        Overrides the closeEvent handler to stop the timer and 
        ensure all modules properly exit (prevents continous running).
        """
        
        # Stops the timer
        self.timer.stop()
        # Triggers the closeEvent for the base class
        super().closeEvent(event)
        # Uses the system exit method to stop this script
        QCoreApplication.quit()



# The main function of this class
def main():
    """
    The main function of this class
    """

    try:
        # Creates a PyQt application allowing for any extra arguments to be passed via the command line in future
        Overlay = QApplication(sys.argv)
        # Sets an empty QIcon to hide the overlay program from the taskbar
        Overlay.setWindowIcon(QIcon())
        
        # Initializes a LunaBot script manager which provides the necessary functions to create a bot script
        LunaBot = OverlayManager()
        # Informs the user of the current process
        LunaBot.debug(text = 'Initializing script... Please Wait...')
        # Adds an overlay to this script to show the user what the bot is looking at or has found
        LunaBot.addOverlay(overlayX = 0, overlayY = 0, overlayWidth = 50, overlayHeight = 50, overlayRows = 2, overlayColumns = 2)
        
        # Runs this script
        Overlay.exec_()
        
    # Else if a RuntimeError occurs
    except RuntimeError as e:
        # Prints an informative error message to the user
        print(f"Error: {e}")
    
    

# Executes the main function if this class is directly executed as the main program (rather than being imported as a module)
if __name__ == '__main__':
    # Calls the test function of this class
    main()