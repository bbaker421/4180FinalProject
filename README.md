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

```
TODO
```

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

2. Connect the Pushbutton to the Pi through GPIO
```
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
```
You can set the GPIO pin through the first parameter of the setup function. Additionally, GPIO.PUD_DOWN is used to indicate that the button will be registered as "high" when pressed.

3. Create a function to read in the button press
   - called in the main loop, will be called everytime
   - uses GPIO.input(PIN_NUMBER) to read in the value from the button
   - if the button is pressed, the camera takes an image and saves it to the desired path as a JPG
   ```
   camera.capture('/PATH/NAME.jpg')
   ```

*Send image to server*

```
Explain
```

*Receive authentication status from server*

```
Explain
```

*Send authentication status to mbed*

```
Explain
```

### Server


```
Give an example
```

### Mbed


```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds


## Authors

* **Daniel Greene**   - *Server/Mbed* - daniel.greene@gatech.edu
* **Apurva Deshmukh** - *Pi/Mbed*     - apurva.deshmukh@gatech.edu
* **Joe Zein**        - *Mbed*        - joezein@gatech.edu

See also the list of [contributors](https://github.com/dgr1/4180FinalProject/contributors) who participated in this project.


## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

