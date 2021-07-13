# Import Required Libraries and Functions
from Speech2Text import speech2Text
from code import type_code
import threading
import time

# +++++++++++++++++++++++++ Code Thread ++++++++++++++++++++++++++++++++++++++++++++++
class CodeThread(threading.Thread):
    def __init__(self,toolinfo,flag,text_box,trigger_function):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        #flag to pause thread
        self.paused = False
        self.pause_cond = threading.Condition(threading.Lock())
        self.toolinfo = toolinfo
        self.flag = flag
        self.text_box = text_box
        self.trigger_function = trigger_function

    # [ Function to start the thread ]
    def run(self):
        while True:
            with self.pause_cond:
                while self.paused:
                    self.pause_cond.wait()
                if self.flag == 1:
                    self.toolinfo.configure(text='State: Listening')
                    text = speech2Text()
                    if text == -1:
                        if self.flag == 1:
                            self.toolinfo.configure(text="Error: Didn't understand, Please try again")
                            time.sleep(2)
                    else:
                        type_code(self.text_box,self.trigger_function,text)

    # [ Function to pause the Thread ]
    def pause(self):
        if self.flag == 1:
            self.toolinfo.configure(text="State: - - -")
        self.flag = 0
        self.paused = True
        self.pause_cond.acquire()

    # [ Function to resume the Thread ]
    def resume(self):
        self.paused = False
        # Notify so thread will wake after lock released
        self.pause_cond.notify()
        # Now release the lock
        self.pause_cond.release()
        self.flag = 1

# This is Just a Thread and doesn't work on itself
if __name__=='__main__':
    print("This Process doesn't run on its own.")