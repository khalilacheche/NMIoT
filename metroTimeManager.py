
import requests
from bs4 import BeautifulSoup
import socket
import time
from metroTimeManager import *
from WindowManager import Window

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

def getTimeList():
    #Sending the request and storing the response in resp object
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    date = date.replace("-","%2F")
    h = now.strftime("%H")
    m = now.strftime("%M")
    resp = requests.get("https://www.t-l.ch/tl-live-mobile/line_detail.php?jour="+date+"&heure="+h+"&minute="+m+"&id=3377704015495524&line=11821953316814882&id_stop=2533279085549588&id_direction=11821953316814882&lineName=m1", verify=False)
    soup = BeautifulSoup(resp.text, 'html.parser')
    tags = soup.find_all('div'); #Getting all the div tags
    times =[]
    for tag in tags:
        attrs = tag.get('class')
        if str(type(attrs))!= '<class \'NoneType\'>': #Proceeding only with the tags that have the "class" attribute
            for attr in attrs:
                if(attr =='time'): #Proceeding only with the tags that have the "time" value in the "class" attribute
                    contents = tag.contents
                    isApprox=False;
                    for content in contents: #Looping through all the
                        if(content.name == 'img'): #Checking if the provided time is a certain time or just approximative
                            isApprox = content['src']=="images/vague.png"
                        if (content.name != 'img' and content != ' '):
                            times.append((isApprox and "~" or "")+content)
    return times


class mtm (Thread):
    def __init__(self,win):
        Thread.__init__(self)
        self.win = win #keeping a reference to the window object so we can pass info to it
    def run(self):
        times=[]
        lastCheckTime = "";
        while True:
            if is_connected():
                times=getTimeList()
                lastCheckTime = datetime.now().strftime("%H:%M")
                self.win.updateTimeList(tlManager.formatTl(times))
                time.sleep(5)
            else :
                print("offline")
                if times != []:
                    times=tlManager.updateTlOffline(times,lastCheckTime)
                    lastCheckTime=datetime.now().strftime("%H:%M")
                    self.win.updateTimeList(tlManager.formatTl(times))
                time.sleep(5)
