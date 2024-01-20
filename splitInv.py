import pygame

def divide_rectangle(rectangle):
    """
    Divide a rectangle into a fixed grid of smaller rectangles.

    Parameters:
    - rectangle: pygame.Rect object representing the initial rectangle.

    Returns:
    - List of pygame.Rect objects representing the smaller rectangles.
    """
    rows = 7
    columns = 4

    width = rectangle.width // columns
    height = rectangle.height // rows

    rectangles = []
    for row in range(rows):
        for col in range(columns):
            x = rectangle.left + col * width
            y = rectangle.top + row * height
            small_rect = pygame.Rect(x, y, width, height)
            rectangles.append(small_rect)

    return rectangles

# Example usage:
# Define the initial rectangle
initial_rectangle = pygame.Rect(50, 50, 700, 500)

# Divide the rectangle into a 4x7 grid
grid_rectangles = divide_rectangle(initial_rectangle)

# Print the coordinates and dimensions of each smaller rectangle
for i, small_rect in enumerate(grid_rectangles, 1):
    print(f"Rectangle {i}: x={small_rect.x}, y={small_rect.y}, width={small_rect.width}, height={small_rect.height}")