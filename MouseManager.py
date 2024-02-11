import pyautogui as mouse

class MouseManager():
    """
    Class that contains all the functions to manipulate any mouse movements that may be required for writing botting scripts
    """


    def __init__(self, lunaClient):
        """
        Initializes the MouseManager() class
        
         Parameters:
        - lunaClient (Win32Window): The client that the script manager is applying the botting scripts to
        """
        
        # Initializes boundary variables to check if coordinates are out of bounds or not
        self.client = lunaClient
    
    
    def isNotOutOfBounds(self, x, y):
        """
        Validates whether or not the passed coordinates are within the client area or not

         Parameters:
        - x, y (ints or Point()): The coordinates to be be validated
        
         Returns:
        - True if the passed coordinates are within the client area, else returns false
        """
        
        # Extracts the boundary limits from the client used on the initialize of this instance
        xMin, xMax = self.client.left, self.client.left + self.client.width
        yMin, yMax = self.client.top, self.client.top + self.client.height
        
        # Returns true if the passed coordinates fall within the client area, else returns false
        return xMin <= x <= xMax and yMin <= y <= yMax


    def getX():
        """
        Returns the cursors current X position
        """
               
        return mouse.position().x


    def getY():
        """
        Returns the cursors current Y position
        """
        
        return mouse.position().y
        

    def getPos():
        """
        Returns the cursors current position
        """
        
        return mouse.position()
    
    
    def moveTo(x, y):
        """
        Moves the mouse cursor to the passed location
        
         Parameters:
        - x, y (ints or Point()): The x and y position that the cursor should be moved to
        """

        mouse.moveTo(x, y, 1.5, mouse.easeInQuad)
    
    
    def moveToRelative(offsetX, offsetY):
        """
        Moves the mouse cursor to the relative position offset from its current location
        
         Parameters:
        - x, y (ints or Point()): The offset x and y position that the cursor should be moved to relative to the current mouse position
        """

        mouse.moveRelTo(offsetX, offsetY, 1.5, mouse.easeInQuad)
        

    def click(self, x = None, y = None, numClicks = 1, delay = 0.25, button = 'left'):
        """
        Clicks the passed mouse button a specified amount of times with the passed amount of time inbetween each click at the passed or current mouse location
        
         Parameters:
        - x, y (optional ints or Point()): The coordinates at which the click action should occur at. (Defaults to current mouse position if no coordinates are passed)
        - numClicks (optional int): The number times to perform the defined click action
        - delay (optional int or float): The time in seconds between each mouse click. (Default is 0.25s)
        - button (optional str): A string representing which mouse button should be pressed on method call. (This is 'left' by default but 'middle' and 'right' are also valid keyword arguments)
        """
        
        try:
            # Validates passed coordinates
            x, y = self.validateCoords(x, y)

            # Defines the accepted button parameters for error checking
            validButtons = ['left', 'middle', 'right']

            # Ensures a valid button keyword argument is passed
            if button in validButtons:
                # Performs click action using the passed parameters
                mouse.click(x, y, numClicks, delay, button)
            
            # Else if an invalid button keyword argument is passed 
            else:
                # Raises a value error exception
                raise ValueError(f'Invalid button parameter passed: {button}, valid buttons are {validButtons}')
                
        # If an exception is raised
        except Exception as e:
            # Returns the error message
            return(e)


    def leftClick(self, x = None, y = None):
        """
        Left clicks at the passed mouse position or the current mouse position if none was passed
        
         Parameters:
        - x, y (optional ints or Point()): The coordinates at which the click action should occur at. (Defaults to current mouse position if no coordinates are passed)
        """
        
        self.click(x, y, button = 'left')


    def rightClick(self, x = None, y = None):
        """
        Right clicks at the passed mouse position or the current mouse position if none was passed
        
         Parameters:
        - x, y (optional ints or Point()): The coordinates at which the click action should occur at. (Defaults to current mouse position if no coordinates are passed)
        """
        
        # Right clicks at the passed x and y position or current mouse position if none was passed
        self.click(x, y, button = 'right')
        

    def doubleClick(self, x = None, y = None):
        """
        Double clicks at the current or passed x, y coordinates with a 0.25 second delay inbetween clicks
        """
        
        # Validates the passed coordinates
        x, y = self.validateCoords(x, y)
        
        # If x and y coordinates were successfully validated
        if x and y:
            # Double clicks at the passed x and y position or current mouse position if none was passed
            mouse.doubleClick(x, y)


    def dragTo(self, endX, endY, startX = None, startY = None):
        """
        Clicks and drags mouse from the current cursor position or passed startX and startY coordinates to the passed endX and endY coordinates
        
         Parameters:
        - endX, endY (ints or Point()): The position at which the dragging will cease
        - startX, startY (optional ints or Point()): The position at which the dragging will start, if no start coordinates are passed, this will default to the current mouse position
        """
        
        # Validates the starting coordinates
        startX, startY = self.validateCoords(startX, startY)

        # Ensures that the passed coordinates are valid
        if startX and startY:
            # Moves the mouse to the start position before commencing the drag
            self.MoveTo(startX, startY)
            
        # Calls the pyautogui dragTo function to handle the drag action
        mouse.dragTo(endX, endY)
        

    def scrollUp(scrollAmount, x = None, y = None):
        """
        Scrolls up by the passed amount of clicks. Optionally, if x and y values are passed, moves the mouse to that location prior to scrolling
        
         Parameters:
        - scrollAmount (int): The number of clicks to scroll up by
        - x, y (optional ints or Point()): The position to move the mouse cursor to before scrolling
        """
            
        mouse.scroll(scrollAmount, x, y)
        

    def scrollDown(scrollAmount, x = None, y = None):
        """
        Scrolls down by the passed amount of clicks. Optionally, if x and y values are passed, moves the mouse to that location prior to scrolling
        
         Parameters:
        - scrollAmount (int): The number of clicks to scroll down by
        - x, y (optional ints or Point()): The position to move the mouse cursor to before scrolling
        """
            
        mouse.scroll((scrollAmount * -1), x, y)
     
    def validateCoords(self, x, y):
        """
        Validates the passed coordinates to ensure they are not None and not out of bounds
        
         Parameters:
        - x, y (ints or Point()): The coordinates to be validated
        
         Returns:
        - The current mouse position if either of the passed coordinates = None
        - else returns the passed coordinates if they are not out of bounds
        - else returns 0,0 if passed coordinates are invalid or the current mouse position is out of bounds
        """
        
        try:
            # Checks if passed coordinates are both valid
            if x is None or y is None:
                # Sets x and y to the current mouse position
                x, y = self.getPos()
            
            # Ensures passed or new coordinates are not out of bounds
            if self.isNotOutOfBounds(x, y):
                # Returns the validated coordinates
                return x, y
        
            # Else if passed coordinates or current mouse position are out of bounds
            else:
                # Raises a value error exception
                raise ValueError(f'Mouse coordinates \"{x, y}\" are out of bounds!')
            
        # If an exception is thrown during validation
        except Exception as e:
            # Prints exception error to the console
            print(e)
            return 0,0
        