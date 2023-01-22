import requests

BASE = "http://127.0.0.1:5000/"

s = requests.Session()
response = s.post(BASE + "/login", {'name': 'shregory', 'password': 'hello'})
response = s.get(BASE + "/activity")

# response = requests.post(BASE + "/addactivity", {'name': 'CN Tower', 'location': '(43.6426,79.3871)', 'description': 'Pay a visit to the most iconic building in Toronto. Enjoy the panoramic views from the top of the tower and take a picture!'})
# response = requests.post(BASE + "/addactivity", {'name': 'Distillery District', 'location': '(43.6503,79.3596)', 'description': 'an internationally acclaimed village of brick-lined streets and dozens of vibrantly restored Victorian Industrial buildings. It’s one of Ontario’s hottest tourist attractions and home to live theatres, galleries, fashion, design and jewelry boutiques, unique cafes and award-winning restaurants. Don\'t forget to get some hot chocolate and take a picture!'})
# response = requests.post(BASE + "/addactivity", {'name': 'Nathan Phillips Square', 'location': '(43.6527,79.3834)', 'description': 'Enjoy skiing at this beautiful ice rink and upload a picture!'})
# response = requests.post(BASE + "/addactivity", {'name': 'Royal Ontario Museum', 'location': '(43.6677,79.3948)', 'description': 'The Royal Ontario Museum is the biggest museum of world cultures and natural history in Canada. Located right in downtown Toronto, the striking main entrance to the museum, known as The Crystal and designed by Michael Lee Chin, will draw you in right away'})
# response = requests.post(BASE + "/addactivity", {'name': 'The Art Gallery of Ontario', 'location': '(43.6536,79.3925)', 'description': 'A remarkable 90,000 works of art live inside the walls of the Art Gallery of Ontario, one of the biggest and best art museums in North America'})
# response = requests.post(BASE + "/addactivity", {'name': 'Casa Loma', 'location': '(43.6780,79.4094)', 'description': 'the only full-sized castle in North America is actually located in Toronto. Casa Loma literally has everything you could want from a castle'})
# response = requests.post(BASE + "/addactivity", {'name': 'Hockey Hall of Fame', 'location': '(43.6473,79.3777)', 'description': 'Ice hockey is often used to define Canada and it’s here on display, with 65,000 square feet filled to the brim with artifacts, mementos, and relics straight from the rink.'})
# response = requests.post(BASE + "/addactivity", {'name': 'Rouge National Urban Park', 'location': '(43.8287,79.1777)', 'description': 'Rouge National Park is Toronto’s own slice of paradise and Canada’s only urban National Park.'})
# response = requests.post(BASE + "/addactivity", {'name': 'St. Lawrence Market', 'location': '(43.6487,79.3715)', 'description': 'Right in the middle of Toronto’s historic Old Town district you’ll find one of the city’s best foodie destinations: the St. Lawrence Market. '})
# response = requests.post(BASE + "/addactivity", {'name': 'The Toronto Islands', 'location': '(43.6214,79.3788)', 'description': 'You only need to travel 10 minutes from the city of Toronto to enter a completely different world. Hop on a ferry and embark on a journey to the Toronto Islands, an attraction-filled destination where relaxation is the name of the game.'})



print(response.json())