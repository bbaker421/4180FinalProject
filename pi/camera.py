from picamera import PiCamera
from time import sleep
import os

"""
import RPI.GPIO as GPIO

GPIO.setWarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO_PUD_DOWN)

while (True):
   if GPIO.input(10) == GPIO.HIGH:
        print("1");

"""
camera = PiCamera()

camera.start_preview()
sleep(1)
camera.capture('/home/pi/Desktop/unknown_image.jpg')
camera.stop_preview()
camera.close()

import requests

url = 'http://10.0.0.236:5000/authenticate'
files = {'file': open('/home/pi/Desktop/unknown_image.jpg', 'rb')}
r = requests.post(url, files=files)

print(r.content)

cmd = './mbed_comm ' + r.content.decode("utf-8")
os.system(cmd)





