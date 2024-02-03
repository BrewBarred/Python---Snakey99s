# Imports sys library for immediate exit after handling a runtime error
import sys


class Debugger():
    """
    Handles all debug messages drawn to the screen or console or log errors for all classes
    """

    @staticmethod
    def debug(debugMsg):
        """
        Paints debug info to the screen to inform the user of the action currently being undertaken by the bot
        
         Parameters:
        - debugMsg (str): The debug message to be displayed at the top of the game client to inform the user of the current process being performed
        """
        
        try:
            
            # Writes debug message to the console with a yellow font color
            print(f'\033[93m{debugMsg}\033[0m')
            
        # Catches any errors gracefully
        except Exception as e:
            
            # Prints an informative error message to the console
            Debugger.logError(f'Error printing debug message: {e}')
            

    @staticmethod
    def logError(errorMsg):
        """
        Method that writes an error to the console then quits the application to ensure it exits after an exception is handled
        
         Parameters:
        - errorMsg (str): The error message to print to the console before exiting
        """
        
        # Prints the passed error message to the console with a red font color
        print(f'\033[91m{errorMsg}\033[0m')
        # System exits with a non-zero exit code to show that an error or exception has occured
        sys.exit(1)