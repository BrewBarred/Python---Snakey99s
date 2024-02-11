class Point():
    """
    Class that mimics a Point object from the likes of C#
    """


    def __init__(self, x, y):
        """
        Initializes the necessary instance attributes required for a Point object
        """
        
        # Creates two instance attributes x and y defining the coordinates of this point
        self.x = x
        self.y = y
        
    
    def __repr__(self):
        """
        Returns a detailed representation of this class for debugging purposes (intended for developers)
        """
        
        # Returns an informative description of the current instance of this class
        return (f'Point({self.x}, {self.y})')
    
    
    def __str__(self):
        """
        Returns the current coordinates assigned to this instance of the Point class
        """
        
        # Returns the current coordinates that this instance of the class is holding
        return (f'{self.x}, {self.y}')