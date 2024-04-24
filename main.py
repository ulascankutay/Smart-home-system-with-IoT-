from time import sleep
import sensor


while True :
     sensor.mq_sensor()
     sleep(1)
     sensor.dht_sensor()
     if(str(sensor.mq_sensor())>="200"):
         print("asdas")
    