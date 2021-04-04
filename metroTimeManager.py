
import requests
from bs4 import BeautifulSoup
import socket
import time
from metroTimeManager import *
from WindowManager import Window
import json
from datetimeManager import *
from timeM import *
from threading import Thread
def is_connected(): #Checking for internet connection state
    try:
        socket.create_connection(("www.google.com",80))
        return True
    except OSError:
        pass
    return False

def getTimeListJson(times):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    date = date.replace("-","%2F")
    h = now.strftime("%H")
    m = now.strftime("%M")
    url_flon = "https://tl-apps.t-l.ch/ni-web/api/departures?line=11821953316814882&stop=1970329131941907&wayback=0&date="+date+"%20"+h+":"+m+":00&count=10"
    url_renens = "https://tl-apps.t-l.ch/ni-web/api/departures?line=11821953316814882&stop=1970329131941907&wayback=1&date="+date+"%20"+h+":"+m+":00&count=10"
    updated_times = []
    is_connected = False
    try:
        r = requests.get(url_flon)
        r.raise_for_status()
        data = r.json()
        for metro_time in data:
            dp_time = datetime.fromtimestamp(metro_time["realDepartureTime"]/1000.0)
            updated_times.append((dp_time,metro_time["destination"]["name"]))
        r = requests.get(url_renens)
        r.raise_for_status()
        data = r.json()
        for metro_time in data:
            dp_time = datetime.fromtimestamp(metro_time["realDepartureTime"]/1000.0)
            updated_times.append((dp_time,metro_time["destination"]["name"]))
        updated_times= sorted(updated_times, key=lambda t: t[0])
        is_connected = True
    except Exception as err:
        print("Couldn't get metro timetable")
        updated_times = times
    return (updated_times,is_connected)      

class mtm (Thread):
    def __init__(self,win):
        Thread.__init__(self)
        self.win = win #keeping a reference to the window object so we can pass info to it
    def run(self):
        times=[]
        lastCheckTime = datetime.now()
        while True:
            (times,is_connected) = getTimeListJson(times)
            if is_connected:
                lastCheckTime = datetime.now()
                self.win.updateTimeList(tlManager.formatTl(times,False))
            else :
                times=tlManager.updateTlOffline(times,lastCheckTime)
                self.win.updateTimeList(tlManager.formatTl(times,True))
            time.sleep(1)