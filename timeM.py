from datetime import datetime
import math
class timeManip:
    @staticmethod
    def getMinDiff(x,y):
        time_delta = (x - y)
        total_seconds = time_delta.total_seconds()
        minutes = total_seconds/60        
        return int(math.floor(minutes))
    @staticmethod
    def getETA(x):
        return timeManip.getMinDiff(x,datetime.now())
class tlManager:
    @staticmethod
    def formatTl(tl,isApprox):
        final =[]
        for t in tl:
            if(timeManip.getETA(t[0])<15):
                final.append(timeStamp(("~" if isApprox else "" )+str(timeManip.getETA(t[0]))+"\'",timeManip.getETA(t[0]),tlManager.getTColor(t[0]),t[1]))
            else:
                final.append(timeStamp(("~" if isApprox else "" )+t[0].strftime("%H:%M"),timeManip.getETA(t[0]),tlManager.getTColor(t[0]),t[1]))
        return final

    @staticmethod
    def getTColor(t):
        if(timeManip.getETA(t)>5):
            return"#2ecc71"#GREEN
        if timeManip.getETA(t)>2:
            return "#e67e22"#ORANGE
        return "#e74c3c"#RED
    @staticmethod
    def updateTlOffline(tl,lastCheckTime):
        newTl =[]
        for t in tl:#filtering out of date metro times
            timePassed= -timeManip.getETA(lastCheckTime)
            if(timeManip.getETA(t[0])>=timePassed):
                newTl.append(t)
        return newTl
class timeStamp:
    def __init__(self, timeStr,eta, color,direction):
        self.timeStr = timeStr
        self.eta = eta
        self.color = color
        self.direction = direction
