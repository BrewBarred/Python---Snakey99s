# Imports timer library
from PyQt5.QtCore import QTimer
# Imports application/widget for event loop
from PyQt5.QtWidgets import QApplication, QWidget
# Imports date time library to clearly see when timers are being activated
from datetime import datetime

# TimerClass 
class TimerClass(QWidget):
    '''
    Class that shows an example of how to two seperate singleShot timers that perform 
    two different tasks after two different amounts of time in milliseconds before exiting
    '''

    def __init__(self):
        '''
        Initialization method: Initializes the variables and objects we require for this timer test class
        '''
        # Must call the base initialization method for this class to execute properly
        super().__init__()
        
        # Creates two timer objects using the QTimer class
        self.timer1 = self.timer2 = QTimer(self)
        # Initializes booleans to test if both timers are finished before exiting app
        self.timer1_done = self.timer2_done = False
        # Calls the start timer method which starts both timers
        self.startTimers()
        

    def startTimers(self):
        '''
        Method to start both timers with messages printed to the console that show what time they have begun
        '''
        # Initializes singleShot timers, these will both only run once for the amount of time passed as the 1st parameter in milliseconds, 
        # and then they will execute the method passed as the second parameter, in this case, timer1 will call action1 and timer2 will call 
        # action2 on completion
        print(f'Starting Timer 1 @ {datetime.now()}')
        self.timer1.singleShot(3000, self.action1)
        print(f'Starting Timer 2 @ {datetime.now()}')
        self.timer2.singleShot(6000, self.action2)


    def action1(self):
        '''
        Method to execute once timer1 has finished executing
        '''
        # Prints the completion time of timer1 to the console
        print(f'Timer 1 completed @ {datetime.now()}')
        
        #
        # Do stuff here when timer 1 expires after 3 seconds
        #

        # Bool acts like a flag to acknowledge that timer 1 has completed its course
        self.timer1_done = True
        # Closes app if both timers are finished
        self.tryClose()


    def action2(self):
        '''
        Method to execute once timer2 has finished executing
        '''
        # Prints the completion time of timer2 the console
        print(f'Timer 2 completed @ {datetime.now()}')
        
        #
        # Do stuff here when timer 2 expires after 6 seconds
        #

        # Bool acts like a flag to acknowledge that timer 2 has completed its course
        self.timer2_done = True
        # Closes app if both timers are finished
        self.tryClose()
        

    def tryClose(self):
        '''
        Method to check if both timers have finished before closing this application
        '''
        # Ensures both timers have finished before exiting
        if self.timer1_done and self.timer2_done:
            # Exits application since both timers are complete
            print('Both timers completed! App will close now...')
            self.close()
        # Else if there is still an active timer, returns early
        else:
            # Breaks out of this event since one timer is still active
            print('Test failed! One or more timers are still active... App will not close yet...')
            return
        

def setup():
    '''
    Method to create a QApplication and instance of the TimerClass in order to execute an event loop
    '''
    # instantiates a QApplication with no command line arguments
    timer_test = QApplication([])
    # creates an instance of our timer test class (the class you can see above)
    timer_class = TimerClass()
    # begins event loop
    timer_test.exec_()
        
# Executes the main function if this class is directly executed as the main program (rather than being imported as a module)
if __name__ == '__main__':
    # Calls the setup method of this class
    setup()
