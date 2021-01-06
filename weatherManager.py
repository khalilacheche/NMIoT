
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
            response = requests.get(url=self.url)
            #with open('res.json','r') as file: #Reading from res.json as placeholder
            #    response=json.load(file)

            self.win.updateWeatherData(json.loads(response.text)["forecasts"])
            time.sleep(10) #Updating the weather every 10 seconds(for testing)
