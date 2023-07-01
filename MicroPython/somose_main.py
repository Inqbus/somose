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



               
               