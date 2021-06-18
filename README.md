# somose
Python drivers for the digital moisture sensor SoMoSe V1.1 for Micropython and RaspberryPi

<img src="https://github.com/Inqbus/somose/blob/main/images/sensor.jpg" alt="drawing" width="200"/>

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





### RaspberryPi drivers
Coming soon!




