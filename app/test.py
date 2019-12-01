import requests

url = 'http://0.0.0.0:5000/authenticate'
files = {'file': open('testImages/unknown_image.jpg', 'rb')}
requests.post(url, files=files)
