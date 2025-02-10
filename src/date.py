from datetime import datetime
import time
from threading import Thread
from src.threads import SharedData
class DateTimeManager (Thread):
    def __init__(self):
        Thread.__init__(self)
        self.date_time = SharedData()
        self.date_time.update([datetime.now().strftime("%a, %e %b %G"),datetime.now().strftime("%H:%M")])
    def run(self):
        while True: #Updating the time and date every second
            self.date_time.update([datetime.now().strftime("%a, %e %b %G"),datetime.now().strftime("%H:%M")])
            time.sleep(1)