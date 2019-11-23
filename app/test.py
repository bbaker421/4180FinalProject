import requests

url = 'http://0.0.0.0:5000/authenticate'
files = {'file': open('testImages/unknownapurva.jpeg', 'rb')}
requests.post(url, files=files)
