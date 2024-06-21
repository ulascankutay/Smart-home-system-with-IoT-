from machine import ADC
from machine import Pin
from time import sleep
from hcsr04 import HCSR04

usensor = HCSR04(trigger_pin=12, echo_pin=14,echo_timeout_us=10000)


 
def hcr_sensor():
    try :
        mesafe = usensor.distance_cm()
        print(mesafe,"\n")
        sleep(2)
    except KeyboardInterrupt:
        pass 
