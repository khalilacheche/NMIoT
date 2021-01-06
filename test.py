import requests
url = "https://api.apixu.com/v1/forecast.json?key=0429e07e3c0246ffa1e185749191503 &q=Lausanne&days=1"
resp = requests.get(url=url)
data = resp.json()
print(data["current"]["temp_c"])
print(data["current"]["temp_c"])
