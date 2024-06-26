from simple import MQTTClient
import urequests as requests
from machine import Pin
from time import sleep
import network
import machine
import umail
import gc
import sys

LED1 = Pin(2, Pin.OUT)
LED2 = Pin(3, Pin.OUT)
fan1 = Pin(32, Pin.OUT)  # A-IA
fan2 = Pin(15, Pin.OUT)  # A-IB
buzzer= Pin(27, Pin.OUT)

ates_sensor = Pin(23, Pin.IN, Pin.PULL_UP)
ses_sensor = Pin(4, Pin.IN, Pin.PULL_DOWN)

secrets = {
    'mqtt_username': 'ulascann',
    'mqtt_key': '135790.Uk',
    'broker': '59861b68801a421591bfed24cac1febf.s1.eu.hivemq.cloud',
    'port': 8883
}


def subscribe_callback(topic, message):
    global alarm_flag
    print(topic, message)
    
    message_str = message.decode('utf-8')
    
    if topic == b"home/led":
        if message_str == "31":
            LED1.on()        
        elif message_str == "30":
            LED1.off()    
        elif message_str == "41":
            LED2.on()
        elif message_str == "40":
            LED2.off()        
    elif topic == b"home/fan":
        if message_str == "11":
            fan_start()        
        elif message_str == "10":
            fan_stop()    
        elif message_str == "21":
            fan_start()
        elif message_str == "20":
            fan_stop() 
    elif topic == b"home/evbos":
        if message_str == "1":
            alarm_flag = True  
        elif message_str == "0":
            alarm_flag = False
    elif topic == b"home/alarm":
        if message_str == "1":
            buzzer.on()      
        elif message_str == "0":
            buzzer.off()
    else:
        print("Bilinmeyen mesaj veya topik")

def ConnectAndSubscribe():
    sslparams = {'server_hostname': secrets["broker"]}
    client = MQTTClient(client_id="esp32-2",
                    server=secrets["broker"],
                    port=secrets["port"],
                    user=secrets["mqtt_username"],
                    password=secrets["mqtt_key"],
                    keepalive=3600,
                    ssl=True,
                    ssl_params=sslparams) 
    client.set_callback(subscribe_callback)
    client.connect()
    client.subscribe(b"home/buzzer")
    client.subscribe(b"home/led")
    client.subscribe(b"home/fan")
    client.subscribe(b"home/ldr")
    client.subscribe(b"home/kapi")
    client.subscribe(b"home/pencere")
    client.subscribe(b"home/hareket")
    client.subscribe(b"home/evbos")
    client.subscribe(b"bahce/supom")
    return client

def publish(topic, value):
    print("-----------")
    client.publish(topic, str(value))
    print(" {} topigine {}'degeri gonderildi!".format(topic, value))
    print("-----------")
    
def RestartAndConnect():
    sleep(2)
    machine.reset()
   
def fan_start():
    fan1.value(1)
    fan2.value(0)

def fan_stop():
    fan1.value(0)
    fan2.value(0)

alarm_flag = False

try:
    client = ConnectAndSubscribe()
except OSError as e:
    RestartAndConnect()

while True:
    print("while girdi")
    client.check_msg()
    sleep(1)
    if alarm_flag:
        if ses_sensor.value() == 1: 
            publish("home/alarm", 1)
            print("ses")
        elif ates_sensor.value() == 0:
            publish("home/alarm", 1)
            print("ates")
    print("while son")
    sleep(1)

