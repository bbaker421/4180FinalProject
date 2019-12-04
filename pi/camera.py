from picamera import PiCamera
from time import sleep
import os
import RPi.GPIO as GPIO

camera = PiCamera()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
prev_inp = 1

def BtnCheck(PinNr):
    global prev_inp
    global count
    
    inp = GPIO.input(PinNr)
    if((not prev_inp) and inp):
        camera.capture('/home/pi/Desktop/unknown_image.jpg')
        #camera.stop_preview()
        import requests
        
        url = 'http://143.215.98.174:5000/authenticate'
        files = {'file': open('/home/pi/Desktop/unknown_image.jpg', 'rb')}
        r = requests.post(url, files=files)

        print(r.content)

        cmd = './mbed_comm ' + r.content.decode("utf-8")
        print("\nSending result to mbed")
        os.system(cmd)
        
    prev_inp = inp

try:
    while(True):
        camera.start_preview()
        while (1):
            BtnCheck(10)
except KeyboardInterrupt:
    GPIO.cleanup()









