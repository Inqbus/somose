"""
Driver class for the SoMoSe v1.1 moisture sensor
"""
import sys

from machine import I2C, Pin
from time import sleep

FACTORY_ADDRESS = 85
FACTORY_SDA = 18
FACTORY_SCL = 19
FACTORY_FREQ = 400000



class SoMoSe():
    """
    SoMoSe Sensor 
    """
    def __init__(self, i2c, addr=FACTORY_ADDRESS):
        """
        i2c : I2C Bus instance.
        addr : i2c address of the sensor. Factory default is 85
        """
        self.i2c = i2c
        self._addr = addr
        
    @property
    def addr(self):
        """
        Returns the i2c address of the sensor
        """
        return self._addr
    
    @addr.setter
    def addr(self, addr):
        """
        Changes the i2c address of the sensor
        """
        self.i2c.writeto(self.addr, bytearray([ord('A'), addr<<1]))

        self._addr = addr
        
    def measure(self):
        """
        Return a measurement.
        mean : The 30 second average
        curr : The current sensor reading
        """
        self.i2c.writeto(self.addr, 'v')
        mean, curr = bytes(self.i2c.readfrom(self.addr, 2))
        
        return mean, curr
    
    def low_high_buf(self, data):
        """
        Split a data word into low and high bytes and transfer into a str buffer
        """
        low_byte = data & 0x00FF
        high_byte = (data & 0xFF00) >> 8
        return [low_byte, high_byte]
    
    def set_dry_limit(self, dry_limit=90):
        """
        Set the internal value for dry soil
        dry_value : The new dry value: Factory default value 90
        """
        self.i2c.writeto(self.addr, bytearray([ord('D')] + self.low_high_buf(dry_limit)))
        
    def set_moist_limit(self, moist_limit=4160):
        """
        Set the internal value for dry soil
        moist_limit : The new dry limit: Factory default value 4160
        """
        self.i2c.writeto(self.addr, bytearray([ord('U')] + self.low_high_buf(moist_limit)))
        
    def set_limits(self, dry_limit=None, moist_limit=None):
        """
        Set both limits. See above
        """
        if dry_limit is not None:
            self.set_dry_limit(dry_limit)
        if moist_limit is not None:
            self.set_moist_limit(moist_limit)
            
    def get_dry_limit(self):
        """
        Get the internal value for dry soil
        Returns dry_limit : The dry limit: Factory default value 90
        """
        self.i2c.writeto(self.addr, 'd')
        dry_limit_bytes = bytes(self.i2c.readfrom(self.addr, 2))
        dry_limit = dry_limit_bytes[0] << 8 + dry_limit_bytes[1]
        return dry_limit
        
    def get_moist_limit(self):
        """
        Get the internal value for dry soil
        returns : moist_limit : The moist limit: Factory default value 4160
        """
        self.i2c.writeto(self.addr, 'u')
        moist_limit_bytes = bytes(self.i2c.readfrom(self.addr, 2))
        moist_limit = moist_limit_bytes[0] << 8 + moist_limit_bytes[1]
        return moist_limit
        
    def get_limits(self):
        """
        Set both limits. See above
        """
        dry_limit = self.get_dry_limit()
        moist_limit = self.get_moist_limit()
        return dry_limit, moist_limit
    




        
