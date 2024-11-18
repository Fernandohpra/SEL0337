from smbus import SMBus
from time import sleep

addr = 0x8
bus = SMBus(1)


while True:
    data = bus.read_i2c_block_data(addr,0,2)
    value = data[0]*256+data[1]
    print(str(value).zfill(4), end='\r')
    sleep(0.05)
 
