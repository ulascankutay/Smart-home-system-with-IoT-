
from machine import Pin
from time import sleep

relay = Pin(12, Pin.OUT)
relay1 = Pin(14, Pin.OUT)
relay2 = Pin(27, Pin.OUT)
relay3 = Pin(26, Pin.OUT)

relay.value(1)
relay1.value(1)
relay2.value(1)
relay3.value(1)
  
while True:
 
  relay.value(0)
  sleep(2)
  relay1.value(0)
  sleep(2)
  relay2.value(0)
  sleep(2)
  relay3.value(0)
  sleep(2)
  # RELAY OFF
  
  print("kapanıyor")
  relay.value(1)
  sleep(2)
  relay1.value(1)
  sleep(2)
  relay2.value(1)
  sleep(2)
  relay3.value(1)
  sleep(2)
  

