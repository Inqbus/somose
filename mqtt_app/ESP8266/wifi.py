import network
from time import sleep

class WiFi():

    def __init__(self, log):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        if not self.wlan.isconnected():
            log('connecting to network...')
            self.wlan.connect('xxxx', 'xxxx')
            while not self.wlan.isconnected():
                log('.')
                sleep(1)
        log('network config:' + str(self.wlan.ifconfig()))
        
    def signal(self):
       return self.wlan.scan()
    
    def disconnect(self):
        self.wlan.active(False)