import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import datetime

i2c = busio.I2C(board.SCL, board.SDA)
adss = [ADS.ADS1115(i2c, address=address) for address in [0x48, 0x49, 0x4A, 0x4B]]
chs = []
for ads in adss:
    ads.gain = 1
    chs.append(AnalogIn(ads, ADS.P0))
    chs.append(AnalogIn(ads, ADS.P1))
    chs.append(AnalogIn(ads, ADS.P2))
    chs.append(AnalogIn(ads, ADS.P3))


#print("{:>5}\t{:>5}".format('raw', 'v'))

while True:
    print('Event')
    for ch in chs:
        print("{:>5}\t{:>5.3f}".format(ch.value, ch.voltage))
    time.sleep(2)
