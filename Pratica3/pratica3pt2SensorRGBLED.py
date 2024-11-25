from gpiozero import DistanceSensor
from gpiozero import RGBLED


led = RGBLED(17, 27, 22)
sensor = DistanceSensor(23, 24)

while True:
    print('Distance to nearest object is', sensor.distance, 'm', end='\r')
    if sensor.distance <= 0.2:
        led.color = (1, 0, 0)
    elif sensor.distance > 0.2 and sensor.distance <= 0.5:
        led.color = (1, 1, 0)
    else:
        led.color = (0, 1, 0)
            
         

        
