import requests

BASE = "http://127.0.0.1:5000/"

#response = requests.post(BASE + "/addactivity", {'name': 'Eaton Centre', 'location': '220 Yonge St, Toronto, ON M5B 2H1', 'description': 'Spend some time at one of the grandest shopping centres in Toronto. Go on a shopping spree and don\'t forget to take a picture!'})
response = requests.get(BASE + "/activity")

print(response.json())