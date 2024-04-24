from machine import ADC
from machine import Pin
from time import sleep
import dht 



adc = ADC(0)            
sensor = dht.DHT11(Pin(0))

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
    
 

