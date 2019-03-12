from datetime import datetime

class timeManip:
    @staticmethod
    def getMinDiff(x,y):
        given_h = int(x[0:2])
        given_min = int(x[3:5])
        current_h = int(y[0:2])
        current_min = int(y[3:5])
        if given_h < 2 and current_h==23:
            given_h =+24
        current_time =  current_h*60 +current_min
        given_time = given_h*60 + given_min
        return given_time-current_time
    @staticmethod
    def getETA(x):
        pass
        if timeManip.getTimeType(x)==1:
            x=x.strip("~")
            return timeManip.getMinDiff(x,datetime.now().strftime("%H:%M"))
        if timeManip.getTimeType(x)==2:
            return timeManip.getMinDiff(x,datetime.now().strftime("%H:%M"))
        if timeManip.getTimeType(x)==3:
            x=x.strip("\'")
            return int(x)
    @staticmethod
    def getTimeType(x):
        if x.find("~") != -1:
            return 1
        if x.find(":") != -1:
            return 2
        if x.find('\'') != -1:
            return 3
        return 0
class tlManager:
    @staticmethod
    def formatTl(tl):
        final =[]
        for t in tl:
            final.append(timeStamp(t,tlManager.getTColor(t)))
        return final

    @staticmethod
    def getTColor(t):
        if(timeManip.getETA(t)>5):
            return"#2ecc71"#GREEN
        if timeManip.getETA(t)>3:
            return "#e67e22"#ORANGE
        return "#e74c3c"#RED
    @staticmethod
    def updateTlOffline(tl,lastCheckTime):
        newTl =[]

        print(tl)
        for t in tl:#looping through tl copy
            if timeManip.getTimeType(t) == 3:
                timePassed= -timeManip.getETA(lastCheckTime)
                if(timeManip.getETA(t)>timePassed):
                    newTl.append(str(timeManip.getETA(t)-timePassed)+"\'")
            else:
                if timeManip.getMinDiff(t.strip("~"),datetime.now().strftime("%H:%M"))>0:
                    newTl.append(str(timeManip.getMinDiff(t.strip("~"),datetime.now().strftime("%H:%M")))+"\'")
        return newTl
class timeStamp:
    def __init__(self, value, color):
        self.value = value
        self.color = color
