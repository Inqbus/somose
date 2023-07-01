from machine import Pin, I2C, Timer

from somose import SoMoSe

i2c = I2C(0, sda=Pin(18), scl=Pin(19))

print("I2C Scan: should show '[85]'")

scan_res = i2c.scan()

print(f'scan result: {scan_res}')

somose_sensor = SoMoSe(i2c)


def get_moisture(_timer):
    
    mean, current = somose_sensor.measure()
    print(f'mean: {mean}, current: {current}')
    
    
timer0 = Timer(0)

timer0.init(period=10000, mode=Timer.PERIODIC, callback=get_moisture)



               