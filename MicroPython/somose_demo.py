"""
Setup class for the SoMoSe v1.1 moisture sensor
"""

import sys
from time import sleep
from somose import SoMoSe, FACTORY_ADDRESS, FACTORY_SDA, FACTORY_SCL, FACTORY_FREQ

from machine import I2C, Pin

SECOND_ADDR = 34

class Demo():
    def __init__(self, sda=FACTORY_SDA, scl=FACTORY_SCL, addr=FACTORY_ADDRESS, freq=FACTORY_FREQ):
        self.sda = sda
        self.scl = scl
        self.addr = addr
        self.freq= freq
        self.setup_i2c()
        self.measure()
        self.set_addr()
        self.set_limits()
    
    def addr_scan(self):
        scan = self.i2c.scan()
        print('I2C scan: Found addresse: {}'.format(scan))
        return scan

    def setup_i2c(self):
        # Set up an I2C instance utilizing the first I2C controller on sda=Pin18 and scl=Pin19
        # The I2C frequency is limited to 100Khz this allows for a cable length of approx 10m to the sensor
        print('Bringing up the I2C bus on sda={} scl={} addr={} freq={}'.format(self.sda, self.scl, self.addr, self.freq))
        print('If these are not your settings please call Demo with the correct settings')
        print('These are the default setting: Demo(sda={}, scl={}, addr={}, freq={}'.format(FACTORY_SDA, FACTORY_SCL, FACTORY_ADDRESS, FACTORY_FREQ))
        self.i2c = I2C(0, sda=Pin(self.sda), scl=Pin(self.scl), freq=self.freq)
        # Scan the I2C bus for the sensor. Should print [85] if not change FACTORY_ADDRESS to the value shown to run the demo. 
        scan = self.addr_scan()
        if len(scan) == 0:
            print('No I2C device found!')
            print('This maybe due to:')
            print('1) Not connected power and or GND cable, check and retry')           
            print('2) Reversed the SDC and SCL cable. Please reverse the SDA and SCL cable, and try again.')            
            sys.exit(1)
        if FACTORY_ADDRESS not in scan:
            print('Cannot find SoMoSe sensor at its factory default address "85"')
            print('This maybe due to:')
            print('1) Not connected power and or GND cable, check and retry')           
            print('2) Usually you have reversed the SDC and SCL cable. Please reverse the SDA and SCL cable, and try again.')
            print("""3) Your Sensor has an other I2C address already set.
If so Please run the demo with the I2C address of the sensor as parameter. Demo(addr={})'.format(scan[0]))""")
            sys.exit(1)
        print('SoMoSe Sensor is up as I2C device {} and ready'.format(self.addr))
        

    def measure(self):
        """
        Shows how to measure moisture
        """
        # get a sensor instance. THe default addr is 0x55 aka 85
        print('We are statting a measurement')
        print('First we connect to our sensor at addr={}'.format(self.addr))
        somose = SoMoSe(self.i2c, self.addr)
       
        print('Then we do three measurements, with a 10 second pause between')
        # Do 3 measurements
        for i in range(2):
            mean, curr = somose.measure()
            print('Mean moisture:{}, current moisture {}'.format(mean, curr))
            sleep(10)

        print('All measurements done')


    def set_addr(self):
        """
        Shows how to change the I2C addres of the sensor
        """
        print('Now we demonstrate changing the I2C address of the sensor')
        print('The sensor should be currently at address {}'.format(self.addr))
        scan = self.addr_scan()
        if self.addr not in scan:
            print('But we found only the following addresses {}. Stopping!'.format(scan))
            sys.exit(1)
            
        print('First we connect to our sensor at addr={}'.format(self.addr))            
        # get a sensor instance. THe default addr is 0x55 aka 85
        somose = SoMoSe(self.i2c, self.addr)
        print('Then change the address to {}'.format(SECOND_ADDR))
        # set the sensor addr permanently to 34
        somose.addr = SECOND_ADDR
        # Scan the I2C bus for the sensor. Should print [SECOND_ADDR]
        
        print('The new scan should show the addr {}'.format(SECOND_ADDR))
        self.addr_scan()

        print('Now we delete our SoMoSe instance and fetch a new one from the new address')
        # delete the sensor instance
        del somose
        
        # get a new sensor instance on the new address
        somose = SoMoSe(self.i2c, SECOND_ADDR)

        print('And we do measurements')
        # Do 3 measurements
        for i in range(2):
            mean, curr = somose.measure()
            print('Mean moisture:{}, current moisture {}'.format(mean, curr))
            sleep(10)
            
        print('We change the address back to the initial address {}'.format(self.addr))
            
        #restore the factory default I2C address
        somose.addr = self.addr
        # Scan the I2C bus for the sensor. Should print [85]
        self.addr_scan()
        print('Sensor should be on the fromer address again.')
        print('Address change demo finished.')
        
        
    def set_limits(self):
        """
        Shows how to set the limits in the sensor
        """
        
    def setup(self):
        """
        SoMoSo Setup for ESP32 
        """
            
        # Shows how to measure moisture
        measure()
        # Shows how to change the I2C address of the sensor
        set_addr()
        # shows how to set the limits in the sensor
        set_limits()
    
