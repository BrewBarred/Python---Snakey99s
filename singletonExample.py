import sys
from PyQt5.QtWidgets import QApplication, QWidget

class SomeClass(QWidget):
    
    # Stores any existing instances of this class to prevent multiple instances being executed simultaneously, a.k.a simple singleton implementation
    instance = None
    
    def __new__(self):
        """ Method that manages the different instances of this class being created, ensuring only one instance exists at any given time """
        # If not instances already exists, creates a new instance of this class and stores it in the 'instance' attribute
        if not self.instance:
            print('Successfully created a new instance of SomeClass...')
            # Creates a new instance of this class and stores it in the 'instance' attribute
            self.instance = super().__new__(self)
        else:
            print('An instance of SomeClass already exists! Fetching that instance...')
        # Returns either the newly created instance of this class or if one previously existed, returns that instance instead
        return self.instance
    
    def __init__(self):
        # Calls the parent super class to ensure default initialization is executed
        super().__init__()
        """ Method that creates/initializes any instance variables that this class may require """
        print('Initializing SomeClass\'s instance variables...')
        # Initializes two instance variables
        self.instanceVariable1 = None
        self.instanceVariable2 = None
        print(f'instanceVariable1 = {self.instanceVariable1}, instanceVariable2 = {self.instanceVariable2}')
        
    def doStuff(self):
        """ Method that changes instance variables then quits QApplication"""
        print('Doing stuff...')
        # Manipulates the instance variables created earlier
        self.instanceVariable1 = not None
        self.instanceVariable2 = not None
        # Closes this instance
        self.closeApp()       

    def doMoreStuff(self):
        """ Method that does more stuff even though this instance was closed earlier"""
        print('Successfully doing more stuff even though this instance was previously closed...')
        # Closes this instance
        self.closeApp()        

    def closeApp(self):
        print(f'instanceVariable1 = {self.instanceVariable1}, instanceVariable2 = {self.instanceVariable2}')
        print('Quitting out of SomeClass\'s instance...')
        # Exits event loop closing this QWidget application
        QApplication.quit()
    

class SomeOtherClass():
    
    def __init__(self):
        """ Method that creates an instance of SomeClass(), does stuff, then quits out of the QApplication """
        print('Attempting to create an instance of SomeClass...')
        # Creates an instance of SomeClass()
        self.instantiatedInstanceOfSomeClass = SomeClass()
        # Does stuff in instanced version of SomeClass then quits out of SomeClass's instance
        self.instantiatedInstanceOfSomeClass.doStuff()
        # Does more stuff with the instance that was closed in the last execution
        self.reuseClosedInstance()
        
        print('Finished using both classes... Happy Coding!')
        sys.exit()
        
    def reuseClosedInstance(self):
        """ Method that does something with the instance that has already been closed"""
        print('Attempting to do stuff with the instance that was previously closed')
        # Uses the inherited instance of SomeClass to doMoreStuff even though the doStuff() method quit out of the QApplication instance
        self.instantiatedInstanceOfSomeClass.doMoreStuff()
        

def main():
    # Creates a QApplication instance in order to execute the QWidget
    eventLoop = QApplication([])
    
    # Creates an instance of SomeOtherClass which will create an instance of SomeClass, do stuff, then quits the QApplication
    inheritingClass = SomeOtherClass()
    # Access the SomeClass instance created by SomeOtherClass
    inheritedInstanceOfSomeClass = inheritingClass.instantiatedInstanceOfSomeClass
    
    # Begins the SomeClass event loop
    eventLoop.exec_()

# Executes the main method when executed via the command line
if __name__ == "__main__":
    main()