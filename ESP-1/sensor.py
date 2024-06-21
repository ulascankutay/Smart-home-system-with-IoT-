from machine import ADC
from machine import Pin
from time import sleep
import dht

adc = ADC(33)            
sensor = dht.DHT11(Pin(13))

def mq_sensor():
    sleep(1)
    deger = adc.read()
    print("gaz değeri :",deger)
    sleep(1)
    return deger
    
def dht_sensor():
    t=0.0
    h=0.0
    try:
        sleep(2)
        sensor.measure()
        t = sensor.temperature()
        h = sensor.humidity()
        print('Sıcaklık: %3.1f C' %t)
        print('Nem: %3.1f %%' %h)
    except OSError as e:
        print('sensör okunmadı')
        
    return [t,h]


