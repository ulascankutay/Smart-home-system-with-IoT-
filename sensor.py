from machine import ADC
from machine import Pin
from time import sleep
from hcsr04 import HCSR04
from time import sleep
import dht 

usensor = HCSR04(trigger_pin=12, echo_pin=14,echo_timeout_us=10000)
adc = ADC(32)            
sensor = dht.DHT11(Pin(15))

def mq_sensor():
    sleep(1)
    deger = adc.read()
    print("gaz değeri :",deger)
    sleep(1)
   
    
    
def dht_sensor():
    try:
        sleep(1)
        sensor.measure()
        t = sensor.temperature()
        h = sensor.humidity()
        print('Sıcaklık: %3.1f C' %t)
        print('Nem: %3.1f %%' %h)
    except OSError as e:
        print('sensör okunmadı')
    
def hcr_sensor():
    try :
        mesafe = usensor.distance_cm()
        print(mesafe,"\n")
        sleep(2)
    except KeyboardInterrupt:
        pass 
