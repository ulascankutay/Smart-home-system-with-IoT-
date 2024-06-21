from simple import MQTTClient
import urequests as requests
from time import sleep
from machine import ADC,Pin
from servo import Servo
import machine
import sensor

buzzer = Pin(32, Pin.OUT)
LED1 = Pin(2, Pin.OUT)
LED2 = Pin(18, Pin.OUT)
relay1 = Pin(12, Pin.OUT)
relay2 = Pin(14, Pin.OUT)
relay3 = Pin(27, Pin.OUT)
relay4 = Pin(26, Pin.OUT)
motor=Servo(pin=25) 

relay1.value(1)
relay2.value(1)
relay3.value(1)
relay4.value(1)
        

secrets = {
   'mqtt_username' : 'ulascan',
   'mqtt_key' : '135790.Uk',
   'broker' : '59861b68801a421591bfed24cac1febf.s1.eu.hivemq.cloud',
   'port' : 8883
}

def subscribe_callback(topic,message):
    
    print(topic,message)
    
    message_str = message.decode('utf-8')
    
    if topic == b"home/led":
        if message_str == "11":
            LED1.on()        
        elif message_str == "10":
            LED1.off()    
        elif message_str == "21":
            LED2.on()
        elif message_str == "20":
            LED2.off()
    elif topic == b"home/role":
        if message_str == "10":
            relay1.value(1)        
        elif message_str == "11":
            relay1.value(0)   
        elif message_str == "20":
            relay2.value(1)
        elif message_str == "21":
            relay2.value(0)
        elif message_str == "30":
            relay3.value(1)
        elif message_str == "31":
            relay3.value(0)
        elif message_str == "40":
            relay4.value(1)
        elif message_str == "41":
            relay4.value(0)
    elif topic == b"home/alarm":
        if message_str == "1":
            buzzer.on()
        elif message_str == "0":
            buzzer.off()
    elif topic == b"home/kapi":
        if message_str == "1":
           motor.move(180)
        elif message_str == "0":
           motor.move(0)
    else:
        print("Bilinmeyen mesaj veya topik")
        
def ConnectAndSubscribe():
    sslparams = {'server_hostname': secrets["broker"]}
    client = MQTTClient(client_id="esp32",
                    server=secrets["broker"],
                    port=secrets["port"],
                    user=secrets["mqtt_username"],
                    password=secrets["mqtt_key"],
                    keepalive=3600,
                    ssl=True,
                    ssl_params=sslparams) 
    client.set_callback(subscribe_callback)
    client.connect()
    client.subscribe(b"home/led")
    client.subscribe(b"home/role")
    client.subscribe(b"home/alarm")
    client.subscribe(b"home/sicaklik")
    client.subscribe(b"home/mq2")
    client.subscribe(b"home/fan")
    client.subscribe(b"home/kapi")
    return client

def publish(topic,value):
    print("-----------")
    client.publish(topic,str(value))
    print(" {} topigine {}'degeri gonderildi!".format(topic,value))
    print("-----------")
     
def RestartAndConnect():
    sleep(2)
    machine.reset()


try:
    client = ConnectAndSubscribe()
except OSError as e:
    RestartAndConnect()
   
publish("ESP-1", 1)
while True :
    temp,hum = sensor.dht_sensor()
    sleep(0.5)
    if temp >= 35 or hum >= 40:
        publish("home/fan",11)
        sleep(0.2)
        publish("home/fan",21)
    cnt = sensor.mq_sensor()
    client.check_msg()
    sleep(0.5)
    
    dht_readings = {'field1':temp,'field2':hum,'field3':cnt}
    request = requests.post('https://api.thingspeak.com/update?api_key=ZT0I1PTFIIIBB0GE',json=dht_readings, headers = {'Content-Type': 'application/json'})
    request.close()
    sleep(0.2)

    
    
