
# SoMoSe Driver
Driver for the digital moisture sensor SoMoSe V1.1 for MicroPython.


# SoMoSe Sensor
<img src="https://github.com/Inqbus/somose/blob/main/images/sensor.jpg" alt="drawing" width="200"/>

You can order the sensor via e.g. Amazon. Look for "BeFlE kapazitiver Bodenfeuchtesensor SoMoSe v1.1" 

The sensor is quite cool. Almost any analog moisture sensor has problems with shifting ground.   
Placing the ADC in the sensor eliminates a lot of the effects owners of analogue moisture sensors have to deal with.

The capacity impact of cable length can be compensated easily by reducing the I2C frequency.  
Setting the I2C bus freq down to 100Khz you can reliably measure moisture over 10 meters distance using cheap telephone cable.


### Project maturity
This project is beta. Please evaluate the code before you use it in production.


### MicroPython Driver
The MicroPython driver lives in the MicroPython directory. It is tested against three ESP32 controllers. 

Left to right: LOLIN32 lite clone (from AZ-Delivery), TTGO T-Koala, Mini D1 ESP32

<img src="https://github.com/Inqbus/somose/blob/main/images/esp32_controller.jpg" alt="drawing" width="200"/>

The driver should run on any hardware supporting MicroPython and having a hardware I2C. It may also work on Hardware with Soft-I2C too, but maybe not as stable. 
Please report any issues I will have a look.


#### Installation

To use solely the driver, copy the file "somose.py" to your controller.
If you like to have additional setup-support you may copy "somose_demo.py" as well.

#### Fast pace usage

Here am minimal code example (Hardware I2C):

```python
from machine import I2C, Pin
from somose import SoMoSe

# get a Hardware I2C bus instance
i2c = I2C(0, sda=Pin(18), scl=Pin(19), freq=100000)

# Fire up the SoMoSe on the I2C bus 
somose = SoMoSe(i2c)

# Do a measurement
mean, curr = somose.measure()
print('Mean moisture:{}, current moisture {}'.format(mean, curr))
```

If you are having only software I2C 

```python
# get a Software I2C bus instance
i2c = I2C(sda=Pin(18), scl=Pin(19), freq=100000)
```

You may have to adjust the 'freq' parameter for longer cables. 


#### Using the demo for setup

The demo helps you with the usual obstacles any beginner stumbles over.

You have to start the demo from the command line of your controller. Here an image from a ![thonny](https://thonny.org) session.

<img src="https://github.com/Inqbus/somose/blob/main/images/setup_1.png" alt="drawing" width="400"/>

In the Thonny command line (or any other commandline you have to your controller type:

```python
from somose_demo import Demo
demo = Demo()
```

You should see something like this:

```
Bringing up the I2C bus on sda=18 scl=19 addr=85 freq=1000000
If these are not your settings please call Demo with the correct settings
These are the default setting: Demo(sda=18, scl=19, addr=85, freq=1000000
I2C scan: [85]
SoMoSe Sensor is up as I2C device 85 and ready
We are statting a measurement
First we connect to our sensor at addr=85
Then we do three measurements, with a 10 second pause between
Mean moisture:b'\x01', current moisture b'\x01'
Mean moisture:b'\x01', current moisture b'\x01'
All measurements done
Now we demonstrate changing the I2C address of the sensor
The sensor should be currently at address 85
I2C scan: [85]
First we connect to our sensor at addr=85
Then change the address to 34
The new scan should show the addr 34
I2C scan: [34]
Now we delete our SoMoSe instance and fetch a new one from the new address
And we do measurements
Mean moisture:b'\x01', current moisture b'\x01'
Mean moisture:b'\x01', current moisture b'\x01'
We change the address back to the initial address 85
I2C scan: [85]
Sensor should be on the old address. Address change demo finished.
```

Or some other messages helping you find the problem.


#### Minimal code with logging, timestamps and a timer

Please have a look at "somose_main.py"

```python
from machine import Pin, I2C, Timer, RTC

from somose import SoMoSe

rtc = RTC()
rtc.datetime((2023, 7, 1, 0, 0, 0, 0, 0))

def log(msg):
    now = rtc.datetime()
    now_str = f'{now[0]:.4d}-{now[1]:02d}-{now[2]:02d} {now[4]:02d}:{now[5]:02d}:{now[6]:02d}' 
    print(now_str, msg)


i2c = I2C(0, sda=Pin(18), scl=Pin(19))

log("I2C Scan: should show '[85]'")

scan_res = i2c.scan()

log(f'scan result: {scan_res}')

somose_sensor = SoMoSe(i2c)

log('Waiting 10 seconds for first timer call')



def get_moisture(_timer):
    
    log('Doing measurement')
    mean, current = somose_sensor.measure()
    log(f'mean: {mean}, current: {current}')
    
    
timer0 = Timer(0)

timer0.init(period=10000, mode=Timer.PERIODIC, callback=get_moisture)
```

### General advice on watering

#### Take the time of day into account

If you like to have your RTC reboot-safe you can use a

DollaTek DS1307 AT24C32

Battery powered realtime clock also via I2C. 

I am using this in my Greenhouse since I like to water my plants not only by moisture level but also by time. Watering 
during high solar input is useless since the water will evaporate quickly. A better strategy is to water in the 
nighttime, based on moisture levels.


#### Drain in intervals

If you have well drained plants e.g. Tomatoes watering in intervals is a good strategie: Watering for 30 secs. Two minutes Waiting. Repeat.
Too much water will only be drained away and you are loosing water. Water in Europe is becoming a crucial resource due to climate change.
The evaporation rate increases 8% per degree Celsius. And here in Germany we have 1.6 degrees warming already.
I hope that SoMoSe will help us all to cope with the water shortage.  

