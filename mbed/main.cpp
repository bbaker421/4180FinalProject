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
 
Servo left(p21);
Servo right(p22);

RawSerial  pi(USBTX, USBRX);

void dev_recv()
{
    char temp = 0;
    while(pi.readable()) {
        temp = pi.getc();
        pi.putc(temp);
        if (temp=='1') myRGBled.write(0.0,1.0,0.0);
        if (temp=='0')  myRGBled.write(1.0,0.0,0.0);
    }
}

int main()
{
     pi.baud(9600);
    pi.attach(&dev_recv, Serial::RxIrq);
    while(1) {
        sleep();
    }
    /*
    myRGBled.write(0.0,1.0,0.0); //green
    while (1) {
    for(float p=0; p<0.5; p += 0.1) {
        left = p;
        right = p;
        wait(0.2);
    }
    for(float p=0.5; p<1.0; p += 0.1) {
        left = p;
        right = p;
        wait(0.1);
    }
    }*/
    
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