from datetime import datetime

class timeManip:
    @staticmethod
    def getMinDiff(x):
        given_h = int(x[0:2])
        given_min = int(x[3:5])
        if given_h < 2 and datetime.now().hour==23:
            given_h =+24
        current_time =  (datetime.now().hour)*60 +datetime.now().minute
        given_time = given_h*60 + given_min
        return given_time-current_time
    @staticmethod
    def getETA(x):
        pass
        if x.find("~") != -1:
            x=x.strip("~")
            return timeManip.getMinDiff(x)
        if x.find(":") != -1:
            return timeManip.getMinDiff(x)
        if x.find('\'') != -1:
            x=x.strip("\'")
            return int(x)
class tlManager:
    @staticmethod
    def formatTl(tl):
        final =[]
        for t in tl:
            final.append(timeStamp(t,getTColor(t)))
        return final

    @staticmethod
    def getTColor(t):
        if(timeManip.getETA(t)>5):
            return"green"
        if timeManip.getETA(t)>3:
            return "orange"
        return "red"

class timeStamp:
    def __init__(self, value, color):
        self.value = timeStamp
        self.color = timeL
