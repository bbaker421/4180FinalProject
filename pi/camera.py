from picamera import PiCamera
from time import sleep
import os
import RPi.GPIO as GPIO

camera = PiCamera()
def button_callback(channel):
    camera.capture('/home/pi/Desktop/unknown_image.jpg')
    camera.stop_preview()
    import requests

    url = 'http://143.215.98.174:5000/authenticate'
    files = {'file': open('/home/pi/Desktop/unknown_image.jpg', 'rb')}
    r = requests.post(url, files=files)

    print(r.content)

    cmd = './mbed_comm ' + r.content.decode("utf-8")
    os.system(cmd)
    camera.start_preview()


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

camera.start_preview()
GPIO.add_event_detect(10, GPIO.RISING, callback=button_callback)

message = input("Press enter to quit\n\n")
while(1):
    pass
GPIO.cleanup()








