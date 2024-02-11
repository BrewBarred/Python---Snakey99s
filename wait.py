
        
    
    async def wait(self, seconds = 0.25):
        """
        Uses the asyncio.sleep() function to create a non-blocking delay for the default or passed amount of seconds before proceeding. (Unfortunately this still pauses the EventLoop though)
        
         Parameters:
        - seconds (optional int or float): The amount of seconds to wait for  before proceeding (Default = 0.25 seconds)
        """
        
         # Check to ensure that seconds is a positive integer or float value
        if not isinstance(seconds, (int, float)):
            # Throws an informative error message to the console before exiting
            self.logError(f'Invalid wait time of {seconds} was passed, seconds must be positive integer or floating-point value!')
        
        # If debug mode is enabled, prints wait time to console
        self.drawDebug(f'Wait function called! Waiting {seconds} seconds before proceeding...', False)
        
        # Waits for the default or the passed amount of seconds
        await asyncio.sleep(seconds)