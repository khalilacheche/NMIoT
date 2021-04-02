import requests
from bs4 import BeautifulSoup
import socket
import time
from metroTimeManager import *
from WindowManager import Window
from weatherManager import *
from datetimeManager import *
from timeM import *
from RPiPlayM import *

########### MAIN THREAD #############
win = Window()
metrotm=mtm(win) #Creating the Metro Time Manager
datetm=dtm(win) #Creating the Date and time Manager
weatherm=wtm(win) #Creating the Weather Manager
rpim = RPiPlayM(win)
rpim.start()
metrotm.start() #Starting the threads
datetm.start()
weatherm.start()
win.start()

