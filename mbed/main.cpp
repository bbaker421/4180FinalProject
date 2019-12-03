#include "mbed.h"
#include "Servo.h"
//Class to control an RGB LED using three PWM pins
class RGBLed
{
public:
    RGBLed(PinName redpin, PinName greenpin, PinName bluepin);
    void write(float red,float green, float blue);
private:
    PwmOut _redpin;
    PwmOut _greenpin;
    PwmOut _bluepin;
};
 
RGBLed::RGBLed (PinName redpin, PinName greenpin, PinName bluepin)
    : _redpin(redpin), _greenpin(greenpin), _bluepin(bluepin)
{
    //50Hz PWM clock default a bit too low, go to 2000Hz (less flicker)
    _redpin.period(0.0005);
}
 
void RGBLed::write(float red,float green, float blue)
{
    _redpin = red;
    _greenpin = green;
    _bluepin = blue;
}
//class could be moved to include file
 
 
//Setup RGB led using PWM pins and class
RGBLed myRGBled(p24,p25,p26); //RGB PWM pins
 
Servo s(p22);

RawSerial  pi(USBTX, USBRX);

void dev_recv()
{
    char temp = 0;
    while(pi.readable()) {
        temp = pi.getc();
        pi.putc(temp);
        if (temp=='1') {
            myRGBled.write(0.0,1.0,0.0);
            s = 0.9; // Open
            wait(3.0);
            s = 0.0; // Close
            }
        if (temp=='0')  myRGBled.write(1.0,0.0,0.0);
    }
}

int main()
{
     s.calibrate(0.001, 45.0);
     s = 0.0;
     pi.baud(9600);
    pi.attach(&dev_recv, Serial::RxIrq);
    while(1) {
        sleep();
    }
    
   /* while(1) {
        if (pc.getc() == '1'){
             myRGBled.write(0.0,1.0,0.0);
             while (1){}
        } else if (pc.getc() == '0') {
            myRGBled.write(1.0,0.0,0.0);
             while (1){}
        } else {
            myRGBled.write(0.0,0.0,1.0);
            }
    }*/
    
}