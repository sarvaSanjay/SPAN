import requests

BASE = "http://127.0.0.1:5000/"

s = requests.Session()
response = s.post(BASE + "/login", {'name': 'shregory', 'password': 'hello'})
response = s.get(BASE + "/history")

print(response.json())