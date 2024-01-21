# Imports os library to 
import os
import pyautogui
import cv2
import numpy as np
import time
from PIL import ImageGrab

def get_pixel_color(x, y):
    screenshot = ImageGrab.grab(bbox=(x, y, x+1, y+1))
    pixel_color = screenshot.getpixel((0, 0))
    return pixel_color

# Move mouse to the center of the screen
pyautogui.moveTo(pyautogui.size()[0] // 2, pyautogui.size()[1] // 2)
time.sleep(1)

# Left click
pyautogui.click()
time.sleep(1)

# Type "Hi, Eli!"
pyautogui.typewrite("Hi, Eli!")

# Construct the relative path to the "screens" folder
imagePath = os.path.normpath(os.path.join(os.getcwd(), '..', 'screens'))

# Load the image
template_path = os.path.join(imagePath, 'test3.png')
template = cv2.imread(template_path)

# Get the screen image
screenshot = pyautogui.screenshot()
screenshot = np.array(screenshot)
screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

# Match the template
result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# Define a threshold for a match
threshold = 0.8

# Convert the target color to hex
target_color = (189, 191, 165)  # Replace with the actual RGB values

if max_val >= threshold:
    # Get the center of the found image
    center_x = max_loc[0] + template.shape[1] // 2
    center_y = max_loc[1] + template.shape[0] // 2

    # Move mouse to the center of the found image
    pyautogui.moveTo(center_x, center_y)
    time.sleep(1)

    # Left click
    pyautogui.click()
    time.sleep(1)

    # Get pixel color using Pillow at the current mouse location
    pixel_color = get_pixel_color(center_x, center_y)
    print("Pixel color at mouse location:", pixel_color)
    print("Target color:", target_color)

    # Check if the pixel color matches the specified values
    if pixel_color == target_color:
        print("Pixel color matches target color.")

        # Search for the target color on the entire screen
        screen_width, screen_height = pyautogui.size()
        for x in range(screen_width):
            for y in range(screen_height):
                pixel_color = get_pixel_color(x, y)
                if pixel_color == target_color:
                    print("Target color found at:", x, y)
                    # Move the mouse to the target color location
                    pyautogui.moveTo(x, y)
                    break
    else:
        print("Pixel color does not match target color.")
else:
    print("Error: Image not found on the screen.")
