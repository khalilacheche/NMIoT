import requests

from src.threads import SharedData

from threading import Thread
from datetime import datetime
from time import sleep
import json

from datetime import timedelta





class TLManager (Thread):
    def __init__(self, metadata_path):
        Thread.__init__(self)
        with open(metadata_path, "r") as f:
            self.metadatas = json.load(f)
        self.upcoming_departures = SharedData()

        self.departure_times = {}
        # initialize departure times
        for line_name, line_metadata in self.metadatas.items():
            self.departure_times[line_name] = []    

    def get_query(self, line_metadata):
        line = line_metadata["line"]
        stop = line_metadata["stop"]

        count = line_metadata["count"] if "count" in line_metadata else 5

        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        date = date.replace("-","%2F")
        h = now.strftime("%H")
        m = now.strftime("%M")
        return f"https://tl-apps.t-l.ch/ni-web/api/departures?line={line}&stop={stop}&date={date}%20{h}:{m}:00&count={count}"

    def fetch_departure_time(self, line_metadata):
        res = []
        query = self.get_query(line_metadata)
        try:
            r = requests.get(query,timeout=5)
            r.raise_for_status()
            data = r.json()
        except Exception as err:
            print("Couldn't timetable for", line_metadata,":", err)
            return None
        for departure_time in data:
            try:
                planned_time = departure_time["plannedDepartureTime"]
                real_time = departure_time["realDepartureTime"]
                
                destination = departure_time["destination"]
                destination_str = destination["name"]+", "+destination["city"]
                
                departure_time = real_time if real_time is not None else planned_time
                
                departure_time = datetime.fromtimestamp(departure_time/1000.0)

                eta = TLManager.get_min_diff(departure_time,datetime.now())
                is_approx = real_time is None

                elem = {
                    "departure_time": departure_time,
                    "eta": eta,
                    "is_approx": is_approx,
                    "destination": destination_str,
                    "metadata": line_metadata
                }
                res.append(elem)
            except Exception as err:
                print("Couldn't parse metro timetable for", line_metadata,":", err)
                continue
        return res
    
    @staticmethod
    def get_min_diff(x,y):
        time_delta = (x - y)
        total_seconds = time_delta.total_seconds()
        minutes = total_seconds/60        
        return minutes



    def run(self):
        while True:
            for line_name, line_metadata in self.metadatas.items():
                line_departure_times = self.fetch_departure_time(line_metadata)
                if line_departure_times is not None:
                    self.departure_times[line_name] = line_departure_times
                else:
                    # update the eta for previously saved departures, mark them as approx
                    for departure_time in self.departure_times[line_name]:
                        departure_time["is_approx"] = True
                        departure_time["eta"] = TLManager.get_min_diff(departure_time["departure_time"],datetime.now())
            
            # flatten the departure times
            flat_departure_times = []
            for line_name, line_data in self.departure_times.items():
                flat_departure_times += line_data

            # sort the departure times
            flat_departure_times.sort(key=lambda x: x["eta"])
            
            # remove negative etas
            flat_departure_times = [x for x in flat_departure_times if x["eta"] >= x["metadata"]["eta_cutoff"]]

            
            # update the shared data
            self.upcoming_departures.update(flat_departure_times)
            sleep(1)




