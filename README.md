# ECE 4180 Final Project - FACE LOCK

This project uses facial recognition to authenticate a user in order to open a door lock. If a user is authorized, the door lock opens, a green LED is lit, and a noise is played from a speaker. If a user is not authorized, the door lock will not open, a red LED is lit, and police siren noises are played from the speaker.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What you need before you begin

#### Hardware (Links Included)

* [Raspberry Pi 4](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/specifications/)
* [Pi NoIR Camera V2](https://www.raspberrypi.org/products/pi-noir-camera-v2/)
* [Pushbutton](https://os.mbed.com/users/4180_1/notebook/pushbuttons/)
* [mbed LPC1768](https://os.mbed.com/platforms/mbed-LPC1768/)
* [RGB LED](https://os.mbed.com/users/4180_1/notebook/rgb-leds/)
* [Speaker - PCB Mount](https://www.sparkfun.com/products/11089)
* [2N3904 General Purpose Amplifier](https://os.mbed.com/users/4180_1/notebook/using-a-speaker-for-audio-output/)
* [Servo](https://os.mbed.com/cookbook/Servo)

#### Software
* [C++](www.cplusplus.com)
* [Python](https://www.python.org/)
* [flask](https://flask.palletsprojects.com/en/1.1.x/)
* [face_recognition](https://github.com/ageitgey/face_recognition)
* [requests](https://pypi.org/project/requests/2.7.0/)


## How It Works

### Raspberry Pi 4


*Import libraries*

```
from picamera import PiCamera
from time import sleep
import os
import RPi.GPIO as GPIO
```


*Capture image*

1. Connect the NoIR Camera V2 to the Pi as seen [here](https://thepihut.com/blogs/raspberry-pi-tutorials/16021420-how-to-install-use-the-raspberry-pi-camera)

2. Connect the Pushbutton to the Pi through GPIO (this project uses pin 10)
```
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
```
You can set the GPIO pin through the first parameter of the setup function. Additionally, GPIO.PUD_DOWN is used to indicate that the button will be registered as "high" when pressed. Be sure to use an external pullup resistor when connecting to ground while setting up the pushbutton.

3. Create a function to read in the button press
   - called in the main loop, will be called everytime
   - uses GPIO.input(PIN_NUMBER) to read in the value from the button
   - if the button is pressed, the camera takes an image and saves it to the desired path as a JPG
   ```
   camera.capture('/PATH/NAME.jpg')
   ```


*Send image to server*

Create a post request to send the image to the server
```
import requests
url = 'http://URL_ADDRESS'
files = {'file': open('/PATH/NAME.jpg', 'rb')}
r = requests.post(url, files=files)
```
The URL address is obtained from the server, explanation seen below in Server section. The request is sent using the Python standard library over HTTP.


*Receive authentication status from server*

```
r = requests.post(url, files=files)
```
After the request is sent, the server returns a '1' if the user is authorized or a '0' if the user is not authorized or if no faces are detected.


*Send authentication status to mbed*

1. Create a C++ file to send the status received from the server to the mbed
   - Communication is done through a serial port (USB)
   - Code can be seen [here](https://github.com/dgr1/4180FinalProject/blob/master/pi/mbed_comm.cpp)

2. Build the C++ file, which creates an executable
3. Call the executable using the response from the server as a command line argument in the original python script
NOTE: This step requires that the Mbed is powered by the Pi. Connect the Mbed to the Pi with the USB.
   ```
   cmd = './mbed_comm ' + r.content.decode("utf-8")
   os.system(cmd)
   ```
The full code for the Pi camera, sending/receiving information from the server, and sending the authentication status to the mbed can be seen [here](https://github.com/dgr1/4180FinalProject/blob/master/pi/camera.py)

### Server

Users are authenticated based on the first image in a folder called known_faces in the top level directory. Access is granted to a given individual or set of individuals.

*Load known face data*


```
daniel_image = face_recognition.load_image_file("known_people/daniel.jpg")
apurva_image = face_recognition.load_image_file("known_people/apurva.jpg")

daniel_face_encoding = face_recognition.face_encodings(daniel_image)[0]
apurva_face_encoding = face_recognition.face_encodings(apurva_image)[0]

known_faces = [
    daniel_face_encoding,
    apurva_face_encoding
]
```

*Revieve image in POST request*


```
@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
```

*Authenticate based on facial recognition*


```
try:
     if 'file' not in request.files:
         return redirect(request.url)
     file = request.files['file']
     if file:
         filename = secure_filename(file.filename)
         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

     unknown_image = face_recognition.load_image_file("./unknown_people/unknown_image.jpg")
     try:
         unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
     except Exception as err:
         print('No faces')
         return "0"
     results = face_recognition.compare_faces(known_faces, unknown_face_encoding)
 ```
*Respond with outcome*

```
if results[1]:
         print("authorized")

         if os.path.exists("unknown_people/unknown_image.jpg"):
             os.remove("unknown_people/unknown_image.jpg")
         else:
             print("The file does not exist")

         return "1"
     else:
         print("not authorized")

         if os.path.exists("unknown_people/unknown_image.jpg"):
             os.remove("unknown_people/unknown_image.jpg")
         else:
             print("The file does not exist")

         return "0"
```

### Mbed

*Wiring*

|mbed|RGB LED |
|----|--------|
| p24| 1-RED  |
| p25| 3-GREEN|
| p26| 4-BLUE |
| gnd| 2      |

NOTE: Use 180-ohm resistor when wiring red LED and 100-ohm resistors when wiring green and blue LEDs.

|mbed|Servo.          |External DC Supply|
|----|----------      |------------------|
|gnd |gnd(black)      |gnd               |
| -  |power(red}      |+4.8V to 6V       |
|p22 |PWM Signal Input| -                |


## Authors

* **Daniel Greene**   - *Server/Mbed* - daniel.greene@gatech.edu
* **Apurva Deshmukh** - *Pi/Mbed*     - apurva.deshmukh@gatech.edu
* **Joe Zein**        - *Mbed*        - joezein@gatech.edu

See also the list of [contributors](https://github.com/dgr1/4180FinalProject/contributors) who participated in this project.
