from datetime import datetime
import time
from threading import Thread
class dtm (Thread):
    def __init__(self,win):
        Thread.__init__(self)
        self.win = win #keeping a reference to the window object so we can pass info to it
    def run(self):
        while True: #Updating the time and date every second
            self.win.updateDateTime(datetime.now().strftime("%a, %e %b %G"),datetime.now().strftime("%H:%M"))
            time.sleep(1)
