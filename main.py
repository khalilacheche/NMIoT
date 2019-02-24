import requests
from bs4 import BeautifulSoup
import socket
import time
from Window import Window
from threading import Thread
from timeM import *

########### FUNCTIONS DEF #############

def is_connected(): #Checking for internet connection state
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

def getTimeList():
    #Sending the request and storing the response in resp object
    resp = requests.get("https://www.t-l.ch/tl-live-mobile/line_detail.php?from=horaire&id=3377704015495524&line=11821953316814882&id_stop=2533279085549588&id_direction=11821953316814882&lineName=m1", verify=False)
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

class mainloop (Thread):
    def __init__(self,win):
        Thread.__init__(self)
        self.win = win #keeping a reference to the window object so we can pass info to it
    def run(self):
        times=[]
        while True:
            if is_connected():
                times=getTimeList()
                self.win.updateTimeList(tlManager.formatTl(times))
                time.sleep(5)
            else :
                print("Cannot execute, no internet connection")
                time.sleep(5)

########### MAIN THREAD #############
win = Window()
ml=mainloop(win) #Creating the "main loop" thread
ml.start()
win.start()
