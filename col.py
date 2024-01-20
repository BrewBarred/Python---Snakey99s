import pyautogui
import numpy as np
from PIL import ImageGrab

def hex_to_rgb(hex_color):
    # Convert a hex color code to an RGB tuple
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def find_and_move_to_color(color, step=10, threshold=30):
    """
    Finds the first occurrence of the specified color on the entire screen.

    Parameters:
    - color (tuple or str): RGB tuple or Hex color code.
    - step (int): Step size for the search. Default is 10.
    - threshold (int): Threshold for color matching. Default is 30.

    Returns:
    None

    Example usage:
    find_and_move_to_color((0, 0, 0), step=10)
    find_and_move_to_color("#FF0000", step=10)
    """
    # Get the screen size
    screen_width, screen_height = pyautogui.size()

    # Capture the entire screen
    screenshot = ImageGrab.grab()

    # Convert the screenshot to a NumPy array
    screenshot_array = np.array(screenshot)

    # Convert the color to RGB if it's in hex format
    if isinstance(color, str):
        color = hex_to_rgb(color)

    # Search for the first occurrence of the specified color on the entire screen with a specified step
    for x in range(0, screen_width, step):
        for y in range(0, screen_height, step):
            # Extract the color information for the specified region
            region = screenshot_array[y:y+step, x:x+step, :]

            # Check if any pixel in the region is close enough to the specified color
            if np.any(np.all(np.abs(region - color) <= threshold, axis=2)):
                print(f"Color {color} found at:", x, y)
                # Move the mouse to the color location
                pyautogui.moveTo(x, y)
                return

    print(f"Color {color} not found on the screen.")

# Example usage:
# Pass RGB color
find_and_move_to_color((0, 0, 0), step=10)

# Pass Hex color
find_and_move_to_color("#000000", step=10)
