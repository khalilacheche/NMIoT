import subprocess
from threading import Thread
class RPiPlayM (Thread):
    def __init__(self,win):
        Thread.__init__(self)
        self.win = win #keeping a reference to the window object so we can pass info to it
    def run(self):
        tache = subprocess.Popen(["sudo","systemctl","start","rpiplay.service"])