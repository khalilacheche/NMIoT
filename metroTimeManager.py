
import requests
import socket
import time
from metroTimeManager import *
from WindowManager import Window
from threading import Thread 
from datetime import datetime
import json
class timeManip: #A set of helper methods for color and time estimation
    @staticmethod
    def getMinDiff(x,y):
        time_delta = (x - y)
        total_seconds = time_delta.total_seconds()
        minutes = total_seconds/60        
        return int(minutes)
    @staticmethod
    def getETA(x):
        return timeManip.getMinDiff(x,datetime.now())
    @staticmethod
    def getTColor(t):
        if(timeManip.getETA(t)>5):
            return"#2ecc71"#GREEN
        if timeManip.getETA(t)>2:
            return "#e67e22"#ORANGE
        return "#e74c3c"#RED
class timeStamp: #represents a time stamp for a metro departure time
    def __init__(self, departureTime,destination,isApprox):
        self.isApprox = isApprox #Boolean, true if the time is not the real departure time but rather a planned or a previous real departure time
        self.destination = destination #String
        self.departureTime = departureTime # datetime
        self.eta = timeManip.getETA(departureTime) # int
        self.color = timeManip.getTColor(departureTime) #String of hex colors
        self.timeStr = self.updateTimeString() #the actual string to be displayed
    def updateTimeString(self):
        self.timeStr = ("~" if self.isApprox else "" )+(str(self.eta)+"\'" if self.eta < 15 else self.departureTime.strftime("%H:%M")) 
    def updateIsApprox(self,isApprox):
        self.isApprox = isApprox
        self.updateTimeString()
    def update(self):
        self.color = timeManip.getTColor(self.departureTime)
        self.updateTimeString() 
        self.eta = timeManip.getETA(self.departureTime)

class mtm (Thread):

    def __init__(self,win):
        Thread.__init__(self)
        self.dp_times = []
        self.dp_times_renens = []
        self.dp_times_flon = []
        self.win = win #keeping a reference to the window object so we can pass info to it
    def run(self):
        while True:
            (r_succeeded,dp_times_renens) = self.getTimeListJson(0) #try to get the newest mdt for one destination
            (f_succeeded,dp_times_flon) = self.getTimeListJson(1) #try to get the newest mdt for the other destination
            if(r_succeeded):
                self.dp_times_renens = dp_times_renens
            else: #Move to offline mode
                self.setAllAprox(self.dp_times_renens)
            if(f_succeeded):
                self.dp_times_flon = dp_times_flon
            else:#Move to offline mode
                self.setAllAprox(self.dp_times_flon)
            self.dp_times = self.dp_times_flon + self.dp_times_renens #updating the mdt list
            self.dp_times = sorted(self.dp_times,key=lambda t: t.eta) #sorting by increasing ETA
            self.removeOutdated() #updates the departure times (color, string, ETA) and only keeps the mdt that are still coming
            self.win.updateTimeList(self.dp_times) #show the mdt list
            time.sleep(1)
    def setAllAprox(self, times):
        for t in times :
            t.updateIsApprox(True)

    def getTimeListJson(self,wayback):
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        date = date.replace("-","%2F")
        h = now.strftime("%H")
        m = now.strftime("%M")
        url = "https://tl-apps.t-l.ch/ni-web/api/departures?line=11821953316814882&stop=1970329131941907&wayback="+str(wayback)+"&date="+date+"%20"+h+":"+m+":00&count=10"
        try:
            r = requests.get(url)
            r.raise_for_status()
            data = r.json()
        except Exception as err:
            print("Couldn't get metro timetable")
            for dp_time in self.dp_times:
                dp_time.updateIsApprox(True)
            return (False,[])
        updated_times = []
        for metro_time in data:
                dp_time = datetime.fromtimestamp(0)
                isApprox = True
                destination = "???"
                if(metro_time["destination"]["name"]!= None):
                    destination = metro_time["destination"]["name"]
                if((metro_time["realDepartureTime"]!= None)):
                    dp_time = datetime.fromtimestamp(metro_time["realDepartureTime"]/1000.0)
                    isApprox= False
                elif (metro_time["plannedDepartureTime"]!= None):
                    dp_time = datetime.fromtimestamp(metro_time["plannedDepartureTime"]/1000.0)
                    isApprox = True
                updated_times.append(timeStamp(dp_time,destination,isApprox))
        return (True,updated_times)
    def removeOutdated (self):
        final = []
        for t in self.dp_times:
            t.update()
            if (t.eta >= 0):
                final.append(t)
        self.dp_times = final