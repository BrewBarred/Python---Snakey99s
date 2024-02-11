# Imports QtWidget/QApplication classes which are required to execute this classes event-loop
from PyQt5.QtWidgets import QApplication, QWidget
# Imports QtGui classes that handle drawing overlays and text to the screen
from PyQt5.QtGui import QFont, QFontMetricsF, QPainter, QColor
# Imports QtCore classes that handle the creation of shapes and timers
from PyQt5.QtCore import QRect, QRectF, Qt, QTimer
# Imports the deepcopy class from the copy library to make deepcopies of our lists
from copy import deepcopy as deepcopy



"""       --------------------       """
##!         Overlay Manager Class:        
"""       --------------------       """    
    

class OverlayManager(QWidget):
    """
    Class that handles any overlays and debug messages over the game client to visually show objects that the bot can see 
    and to inform the user of the current action that the bot is performing
    """
    

    def __init__(self, lunaClient, *args, **kwargs):
        """
        Method that creates/initializes any instance variables that this class may require
        """
        
        try:
            
            # Writes initialization info to console
            print(f'Initializing overlay manager...')
            # Calls the default initialization method to ensure proper initialization behaviour is executed
            super().__init__(*args, **kwargs)
            
            # Initializes the transparent canvas which will be used for drawing
             
            # Sets instance attribute that stores the passed lunaClient which is where the overlays and debug messages will be drawn to
            self.lunaClient = lunaClient
            # Sets the size of the transparent canvas to draw on
            self.setGeometry(lunaClient.left, lunaClient.top, lunaClient.width, lunaClient.height)
            # Sets window flags for the overlay to hide it from the taskbar
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
            # Sets attribute for a translucent background
            self.setAttribute(Qt.WA_TranslucentBackground)
            # Ensures the canvas is visible
            self.show()
            
            # Initializes other necessary instance attributes
            
            # Creates a debug list which queues any debug messages needing to be displayed
            self.debugMsgList = []
            # Stores the timer that is used to remove debug messages after a set amount of time
            self.debugTimer = QTimer()    
            # Returns true if there is no self debugMsg currently being displayed
            self.debugCleared = False
            # Creates an overlay list which queues any debug messages needing to be displayed
            self.overlayList = []
            # Returns true if there are no overlays being displayed
            self.overlaysCleared = False
            # Stores the overlay that is used to remove debug messages after a set amount of time
            self.overlayTimer = QTimer()
            # Sets a default overlay/debug color to prevent the paintEvent trying to paint with an undefined color
            self.debugColor = self.overlayColor = QColor(Qt.white)
        
        # Catches any errors gracefully
        except Exception as e:
            
            # Writes error info to console if an exception is thrown during initialization
            print(f'Init exception raised: {e}')

        
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
            
            # If there is a debug message in the drawing queue
            if self.debugMsgList is not None:
                # Draws the debug message to the screen (if one exists)
                self.__drawDebugMsg(painter)
                
            # If there is an overlay in the drawing queue
            if self.overlayList is not None:
                # Draws each overlay in the overlayList
                self.__drawOverlays(painter)
        
        # Catches any errors gracefully
        except Exception as e:
            
            # Prints an informative error message to the console
            return (f'Error painting overlays: {e}')
            
    
    def __drawDebugMsg(self, painter):
        """
        Method to draw a debug message to the screen.
        This method has been __nameMangled to reduce accidental usage outside of this class
        """
        
        try:
            
            # Returns early if there is no debug message to paint (shouldn't be possible but doesn't hurt to check it anyway)
            if len(self.debugMsgList) > 0:
                
                # Sets the text properties of the debug message (font style and font size)
                font = QFont("Arial", 9)
                # Sets the outline color of the overlay grid to match the default color unless another color has been passed
                painter.setPen(self.debugColor)
                # Applies debug messages text properties to the painter
                painter.setFont(font)
        
                # Defines the texts location and size
                textWidth = QFontMetricsF(font).width(self.debugMsgList[0])
                textHeight = QFontMetricsF(font).height()
                textX = (self.lunaClient.width - textWidth) // 2
                textY = textHeight - textHeight / 1.5
        
                # Defines the textBox in which the debug message will be displayed
                textBox = QRectF(textX, textY, textWidth + 10, textHeight + 10)
                # Draws the textBox to the screen along with the passed debug message
                painter.drawText(textBox, Qt.AlignTop | Qt.AlignLeft, self.debugMsgList[0])
                
                # Sets debug message bool to false since we just drew another debug message
                self.debugCleared = not self.debugMsgList
            
        
        # Catches any errors gracefully
        except Exception as e:
            
            # Prints an informative error message to the console
            return (f'Error drawing debug message: {e}')
            
    
    def addDebug(self, debugMsg, delay = 1500):
        """
        Paints debug info to the screen to inform the user of the action currently being undertaken by the bot
        
         Parameters:
        - debugMsg (str): The debug message to be displayed at the top of the game client to inform the user of the current process being performed
        - delay (optional int): The time in milliseconds before the overlay is automatically removed (default = 1500, None = Permanent)
        """
        
        try:
            
            # Returns early if there is no debug messages to display
            if debugMsg is None and self.debugMsgList is None:
                return
            
            # Adds the passed debug message to the message list to queue it
            self.debugMsgList.append(debugMsg)
            # Sets debugCleared bool to False since we just added a debug message to the queue
            self.debugCleared = False
            
            # Creates a timer to remove this debug message after the passed amount of time (ms)
            self.debugTimer.singleShot(delay, self.clearDebug)

        # Catches any errors gracefully
        except Exception as e:
            
            # Prints an informative error message to the console
            return (f'Error adding debug message: {e}')
           

    def clearDebug(self):
        """
        Method to remove the debug message from the screen after it's timer has expired
        """
        
        # Checks if the debug message list has any messages in the queue
        if self.debugMsgList: 
            
            # Sets the message at the start of the queue to an empty string
            self.debugMsgList[0] = None
            # Repaints this control to remove the current debug message from the screen before deleting it otherwise it will stay there permanently
            self.update()
            # Pops the first element of the debugMsgList
            self.debugMsgList.pop(0)
            
        # Sets debug cleared bool to true if the debug message list is now empty
        self.debugCleared = not self.debugMsgList
        # Attempts to exit this instance
        self.tryClose()
        

    def setDebugColor(self, newColor = 'white'):
        """
        Method that changes the color of the debug overlays
        
         Parameters:
        - color (QColor): The desired debug overlay color (default = 'white')
        """
        
        # Attempts to convert the passed color string into a QColor
        convertedColor = QColor(newColor)
        
        # Ensures the passed color is of type QColor before proceeding
        if convertedColor.isValid():
            
            # Sets the debug overlay paint brush to the passed color
            self.debugColor = convertedColor
            # Calls repaint method to instantly repaint this control
            self.repaint()
         
        # Else if passed color is not of the correct type
        else:
            # Returns an error message
            return (f'Failed to set debug overlay color - Invalid QColor of \"{newColor}" was passed!')       
        
    
    def __drawOverlays(self, painter):
        """
        Method to draw each overlay currently stored in the overlayList to the screen.
        This method has been __nameMangled to reduce accidental usage outside of this class
        """
        
        try:
            
            # Sets the outline color of the overlay grid to match the default color unless another color has been passed
            painter.setPen(self.overlayColor)
            
            # Ensures the overlayList is populated before trying to iterate through it
            if self.overlayList:
                # For each grid (overlay) in the overlay list
                for grid in self.overlayList:

                    # Draws this grid to the screen
                    painter.drawRect(grid)
                    # Writes debug info to the screen informing user that an overlay is currently being cleared
                    self.addDebug(f'Added overlay at x: {grid.x()}, y: {grid.y()}', delay = 1000)
                    
            # Sets overlays cleared bool to false since we just added some
            self.overlaysCleared = not self.overlayList
            
        # Catches any errors gracefully
        except Exception as e:
            
            # Prints an informative error message to the console
            return (f'Error drawing overlay: {e}')
        

    def addOverlay(self, overlayX = 0, overlayY = 0, overlayWidth = 200, overlayHeight = 200, overlayRows = 1, overlayColumns = 1, overlayThickness = 2, overlayDelay = 3000):
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
            
            # Creates a rectangle which represents the outer boundries of this grid using the passed parameters
            overlayBox = QRect(overlayX, overlayY, overlayWidth, overlayHeight)
        
            # Stores the grid being drawn inside the for loop 
            # Calculates the width and height of the grid to draw, based on the passed rows and columns
            gridWidth = int(overlayBox.width() / overlayColumns)
            gridHeight = int(overlayBox.height() / overlayRows)
            
            # Creates a list to collectively store any grids created into the overlay list, 
            # this way if multiple grids are paired together, we can remove all of them at once
            gridRemovalList = []
                
            # Draws a grid using the passed rows and columns, if no rows or columns were passed, this will create a 1x1 grid by default
            for currentRow in range(overlayRows):
                for currentColumn in range(overlayColumns):
                    
                    # Calculates this position of the grid slot being drawn (or outline if its a 1x1 grid)
                    gridX = overlayBox.left() + currentRow * gridWidth
                    gridY = overlayBox.top() + currentColumn * gridHeight
                    # Creates a rectangle representing this grid/grid slot
                    grid = (QRect(gridX, gridY, gridWidth, gridHeight))
                    # Adds this grid to the gridRemovalList, if this loop is creating multiple grid 
                    # slots, this grouping allows us to remove every grid slot later, instead of the last one only
                    gridRemovalList.append(grid)
            
            # Extends the overList class attribute to combine this gridRemovalList to it for painting when the paintEvent is called
            self.overlayList.extend(gridRemovalList)
            # Sets overlays cleared bool to False again since we just added one
            self.overlaysCleared = False
            
            # Starts a single shot timer that will clear this grid after the passed overlayDelay in ms has passed.
            # Note: The "lambda:" expression is preventing the clearOverlay parameters from being prematurely 
            # evaluated, I don't think it would matter in this situation but it's good practice.
            self.overlayTimer.singleShot(overlayDelay, lambda: self.clearOverlay(gridRemovalList)) 
                        
        # Catches any errors gracefully
        except Exception as e:
            
            # Informs user that an error has occured
            self.addDebug('Error adding overlay! Please see console output for more information...')
            # Prints an informative error message to the console
            return (f'Error adding overlay: {e}')


    def clearOverlay(self, gridRemovalList):
        """
        Method to remove an overlay from the screen after its timer has expired
        
         Parameters:
        - grid (QRect): The grid/grid slot to remove from the overlayList
        - gridRemovalList (List[QRect]): A list containing a group of grids/grid slots to remove from the overlayList
        """
        
        try:
            
            # If the overlay list is empty
            if self.overlaysCleared is False:
                # Iterates through the passed list of overlay grids and removes them one-by-one
                for grid in gridRemovalList:
                    # Ensure the passed grid removal list is not empty to prevent index errors
                    if gridRemovalList:
                        # Writes debug info to the screen informing user that an overlay is currently being cleared
                        self.addDebug(f'Removed overlay at x: {grid.x()}, y: {grid.y()}', delay = 1000)
                        # Removes the last element of the grid removal list
                        self.overlayList.remove(grid)
            
                    # Else if gridRemovalList is empty
                    else:
                        # Breaks out of the loop since there are no more overlays to remove
                        break
               
            # Updates the canvas which will draw all of the overlays contained within the list
            self.repaint()
            # Returns true if there are no overlays left to display
            self.overlaysCleared = not self.overlayList
            # Attempts to exit this instance
            self.tryClose()
            
        # Catches any errors gracefully
        except Exception as e:
            
            # Informs user that an error has occured
            self.addDebug('Error adding overlay! Please see console output for more information...')
            # Prints an informative error message to the console
            return (f'Error adding overlay: {e}')
    
    
    def setOverlayColor(self, newColor = 'white'):
        """
        Method that changes the color of the overlays
        
         Parameters:
        - color (QColor): The desired overlay color (default = 'white')
        """
        
        # Attempts to convert the passed color string into a QColor
        convertedColor = QColor(newColor)
        
        # Ensures the passed color is of type QColor before proceeding
        if convertedColor.isValid():
            # Sets the overlay paint brush to the passed color
            self.overlayColor = convertedColor
        
        # Else if passed color is not of the correct type
        else:
            # Returns an error message
            return (f'Failed to set overlay color - Invalid QColor of \"{newColor}" was passed!')
    
    
    def tryClose(self):
        """
        Method that interrupts any application exit attempts to ensure all actions have been completed first
        """
        
        # Ensures debug message and all overlays have been cleared before exiting
        if self.debugCleared and self.overlaysCleared:
            
            # Writes close message to console
            print('Overlay Manager tasks complete! Exiting overlay manager...')
            # Resets overlay booleans to prevent them being true the next time this instance is used
            self.debugCleared = self.overlaysCleared = False
            # Exits the event loop, closing this widget
            QApplication.quit()