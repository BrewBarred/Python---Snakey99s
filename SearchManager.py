# Imports os library to 
import os
import pyautogui
import cv2
import numpy as np
import time
import Point
from PIL import ImageGrab

class SearchManager():
    
    # Defines the path in which the valid object images are located
    imageFolder = os.path.join('screens')
    # The list of pixel colors to accept when found on screen
    colorList = []
    # The list of object images 
    imageList = []
    
    def setDirectory(self, directory):
        """
        Fetches any images from the passed directory and loads them into the local imageList
        """
    
        # Iterates through the files in the passed directory
        for filename in os.path.join(self.imageFolder, directory):
            # Checks if the file is an image
            if filename.lower().endswith('.png', '.jpg', '.jpeg', '.gif'):
                # If the file is an image, add its full path to the image_list
                self.imageList.append(os.path.join(directory, filename))
    

    def findImage(self, imageName, threshold = 0.8):
        """
        Checks if the passed image is found on the screen returns the co-ordinates of its centre point if found, else returns an error msg
        
         Parameters:
        imageName (str): The filename of the image to find on the screen
        threshold (float): The tolerance amount between 0 and 1 representing the similarity threshold. The higher the threshold, the stricter the match.
        """

        # Checks if the image exists in the loaded image list
        if imageName in self.imageList:
            
            # Loads the image to find on the screen
            template = os.path.join(self.imageFolder, imageName)
            imageToFind = cv2.imread(template)
            
            # Takes a screen shot of the screen to compare against the imageToFind
            screenshot = np.array(pyautogui.screenshot())
            # Converts the screenshot to BGR color format
            convertedScreenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
            
            # Match the template
            result = cv2.matchTemplate(convertedScreenshot, imageToFind, cv2.TM_CCOEFF_NORMED)
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
            
            if maxVal >= threshold:
                # Get the center of the found image
                centreX = maxLoc[0] + imageToFind.shape[1] // 2
                centreY = maxLoc[1] + imageToFind.shape[0] // 2
                # Returns the pixel location of the found 
                return Point(centreX, centreY)
        
        else:
            # Else if passed image file name is not found in the image directory, writes error to console and returns None
            print('Failed to find the passed image filename in the image directory!')
            
    
    def findPixelByColor(self, targetColor, searchX = None, searchY = None, searchWidth = None, searchHeight = None):
        """
        Returns the location of the first found pixel matching the passed color, either on the whole screen or within a passed search area
        """

        # If no positional parameters were passed
        if searchX is None or searchY is None:
            # Sets the left corner of the search area to the top left corner of the screen
            searchX, searchY = 0,0
         
        # If no size parameters were passed
        if searchWidth is None or searchHeight is None:
            # Sets the search area to match the screen size
            searchWidth, searchHeight = pyautogui.size()
        
        # Foreach pixel in the search area
        for x in range(searchWidth):
            for y in range(searchHeight):
                
                # Get the current pixels color
                pixelColor = pyautogui.pixel(x, y)
                
                # If the current pixel matches the passed target color
                if pixelColor == targetColor:
                    
                    # Moves the mouse to the target color location
                    pyautogui.moveTo(x, y)
                    # Prints a successful debug message with information of the pixel location
                    print("Target color found at:", x, y)
                    # Returns the found pixels location as a Point object
                    return Point(x, y)
        
        # Else if pixel color is not found on screen or within passed search area, returns a failed debug message 
        return (f'Failed to find pixel color: {targetColor} in the search area: {searchX, searchY, searchWidth, searchHeight}')
            

    def getColorAt(x = None, y = None):
        """
        Returns the color of the pixel at the passed x and y coordinates or at the current mouse position if no x and y coordinates are passed
        """

        # If no coordinates were passed
        if x is None and y is None:
           # Sets coordinates to match the current mouse position
           x, y = pyautogui.position()
           
        # Ensures the coordinates are within the screen dimensions before proceeding
        if not pyautogui.onScreen(x, y):
            
            print(f'Cannot retrieve pixel color at {x}, {y}. Passed coordinates are out of bounds!')
            return
        
        else:
            
            # Takes a screenshot of the screen to create a bounding box the size of one pixel at the mouse position
            screenshot = ImageGrab.grab(bbox=(x, y, x+1, y+1))
            # Returns the pixel color of the bounding box
            return screenshot.getpixel(0, 0)


   
