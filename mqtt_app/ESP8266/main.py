"""
A more robust control code. If the measurement raises an error the SoMoSe is restarted by doing a power cycle.
To achieve this functionality the Vcc of the SoMoSe has to be a GPIO and NOT the Vcc of the Microcontroller.
"""

from machine import Pin, I2C, Timer, RTC, deepsleep, UART
from time import sleep
import sys

from somose import SoMoSe
from wifi import WiFi
from mqtt import MQTT

# Power GPIO for SoMoSe Sensor
SOMOSE_POWER_PIN = 15
# GPIO for I2C SDA
I2C_SDA = 4
# GPIO for I2C SCL
I2C_SCL = 5


LOG_FILE_NAME = 'log.log'


class Logger:
    def __init__(self):
        self.rtc = RTC()
        self.log_file = open(LOG_FILE_NAME, 'w')
#        self.uart = UART(0, baudrate=9600, rx=16, tx=17 )
        
    def get_now(self):
        now = self.rtc.datetime()
        now_str = f'{now[0]:.4d}-{now[1]:02d}-{now[2]:02d} {now[4]:02d}:{now[5]:02d}:{now[6]:02d}' 
        return now_str       
        
    def log(self, msg):
#        self.uart.write(self.get_now() + ' ' + msg + '\n')
        print(self.get_now(), msg)
        self.log_file.write(msg+'\n')
    
    def disconnect(self):
        self.uart.deinit()
    

class RobustSomose:
    
    def __init__(self, log):
        self.log = log
        self.setup_somose()
        
    def power_cycle_somose(self):
        self.power_i2c = Pin(SOMOSE_POWER_PIN, Pin.OUT)
        self.power_i2c.value(0)
        self.power_i2c.value(1)

    def setup_somose(self):

        self.power_cycle_somose()

        self.i2c = I2C(sda=Pin(I2C_SDA), scl=Pin(I2C_SCL))

        self.log("I2C Scan: should show '[85]'")

        scan_res = self.i2c.scan()

        self.log(f'scan result: {scan_res}') 

        self.sensor = SoMoSe(self.i2c)
        
    def disconnect(self):
        self.log('Somose disconnecting')
        self.power_i2c.value(0)
        self.log('Somose disconnected')
        
        
    def get_moisture(self):
        
        self.log('Doing measurement')
        try:
            mean, current = robust_somose.sensor.measure()
            self.log(f'mean: {mean}, current: {current}')
        except Exception as e:
            robust_somose.log(f'An Error occured: {e}, restarting SoMoSe')
            robust_somose.setup_somose()
        return mean, current
        

logger = Logger()

# Get a Somose Control instance

logger.log('Starting mesurement')
robust_somose = RobustSomose(logger.log)

count = 3
while count > 0:
    mean, current = robust_somose.get_moisture()
    robust_somose.log('Waiting 1 sec')
    sleep(1)
    count -= 1


robust_somose.disconnect()


logger.log('Ended mesurement')


wifi = WiFi(logger.log)

mqtt = MQTT(logger.log)

logger.log('Publishing data')
try:
    now = logger.get_now()
    mqtt.publish({'mean':mean, 'current':current, 'time':now}, topic="moist/somose1")
except Exception as e:
    sys.print_exception(e)

logger.log('Data published')


mqtt.disconnect()
wifi.disconnect()

robust_somose.log('Waiting 1 sec')
sleep(1)

robust_somose.log('going deep sleep')

deepsleep(20000)