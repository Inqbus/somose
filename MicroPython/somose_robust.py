"""
A more robust control code. If the measurement raises an error the SoMoSe is restarted by doing a power cycle.
To achieve this functionality the Vcc of the SoMoSe has to be a GPIO and NOT the Vcc of the Microcontroller.
"""

from machine import Pin, I2C, Timer, RTC

from somose import SoMoSe

# Power GPIO for SoMoSe Sensor
SOMOSE_POWER_PIN = 23
# GPIO for I2C SDA
I2C_SDA = 18
# GPIO for I2C SCL
I2C_SCL = 19


class RobustSomose:
    
    def __init__(self):
        self.rtc = RTC()
        self.rtc.datetime((2023, 7, 1, 0, 0, 0, 0, 0))
        self.setup_somose()
        
    def log(self, msg):
        now = self.rtc.datetime()
        now_str = f'{now[0]:.4d}-{now[1]:02d}-{now[2]:02d} {now[4]:02d}:{now[5]:02d}:{now[6]:02d}' 
        print(now_str, msg)

    def power_cycle_somose(self):
        self.power_i2c = Pin(SOMOSE_POWER_PIN, Pin.OUT)
        self.power_i2c.value(0)
        self.power_i2c.value(1)


    def setup_somose(self):

        self.power_cycle_somose()

        i2c = I2C(0, sda=Pin(I2C_SDA), scl=Pin(I2C_SCL))

        self.log("I2C Scan: should show '[85]'")

        scan_res = i2c.scan()

        self.log(f'scan result: {scan_res}')

        self.sensor = SoMoSe(i2c)



def get_moisture(_timer):
    
    somose.log('Doing measurement')
    try:
        mean, current = somose.sensor.measure()
        somose.log(f'mean: {mean}, current: {current}')
    except Exception as e:
        somose.log(f'An Error occured: {e}, restarting SoMoSe')
        somose.setup_somose()
        

# Get a Somose Control instance
somose = RobustSomose()

timer0 = Timer(0)

timer0.init(period=10000, mode=Timer.PERIODIC, callback=get_moisture)

somose.log('Waiting 10 seconds for first timer call')

               
               