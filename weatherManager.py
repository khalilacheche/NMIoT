
from threading import Thread
import requests
import time
import json
class wtm (Thread):

    def __init__(self,win): #Intializing the request for the Yahoo Weather API
        ############### ALL COMMENTEND WAITING FOR API KEY ###############
        #Basic info
        self.url = "https://weather-fetcher-nmiot.herokuapp.com/weather"
        Thread.__init__(self)
        self.win = win #keeping a reference to the window object so we can pass info to it
    def run(self):
        while True:
            try:
                r = requests.get(url=self.url)
                r.raise_for_status()
                self.win.updateWeatherData(json.loads(r.text)["forecasts"])
                time.sleep(3600) #Updating the weather every hour
            except Exception as err:
                print("couldn't get weather")
                time.sleep(10) #try again in 10 seconds   
            #with open('res.json','r') as file: #Reading from res.json as placeholder
            #    response=json.load(file)

