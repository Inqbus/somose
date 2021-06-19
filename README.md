# somose
Drivers for the digital moisture sensor SoMoSe V1.1 in Micropython(, RaspberryPi and C).

<img src="https://github.com/Inqbus/somose/blob/main/images/sensor.jpg" alt="drawing" width="200"/>

You can order the sensor via e.g. Amazon. Look for "BeFlE kapazitiver Bodenfeuchtesensor SoMoSe v1.1" 

### Project maturity
This project is beta. Please evaluate the code before you use it in production.

### MicroPython drivers
The MicroPython driver lives in the MicroPython directory. This driver is tested against ESP32 and LOLIN32 controllers, only. 
It should work on any controller with Hardware I2C, but it may not. Please report any errors I will have a look.

#### Installaton

To use solely the driver copy the file "somose.py" to your controller.
If you like to have setup-support you may copy "somose_demo.py" as well.

#### Fast pace usage

Here am minimal code example:

```python
from machine import I2C, Pin
from somose import SoMoSe

# get a I2C bus instance
i2c = I2C(0, sda=Pin(18), scl=Pin(19), freq=100000)

# Fire up the SoMoSe on the I2C bus 
somose = SoMoSe(i2c)

# Do a measurement
mean, curr = somose.measure()
print('Mean moisture:{}, current moisture {}'.format(mean, curr))
```

#### Using the demo for setup

The demo helps you with the usual obstacles any beginner stumbles over.

You have to start the demo from the command line of your controller. Here I show an image from a ![thonny](https://thonny.org) session.

<img src="https://github.com/Inqbus/somose/blob/main/images/setup_1.png" alt="drawing" width="400"/>

In the Thonny command line type:

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

Or some other messages helping you to find the problem.

### RaspberryPi drivers
Coming soon!




