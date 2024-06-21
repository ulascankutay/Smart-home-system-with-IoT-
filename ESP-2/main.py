from simple import MQTTClient
from machine import Pin
from time import sleep
import network
import machine

LED1 = Pin(2, Pin.OUT)
LED2 = Pin(15, Pin.OUT)
fan1A = Pin(21, Pin.OUT)  # A-IA
fan1B = Pin(22, Pin.OUT)  # A-IB
fan2A = Pin(18, Pin.OUT)  # B-IA
fan2B = Pin(5, Pin.OUT)  # B-IB
buzzer= Pin(19, Pin.OUT)

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
            fan_start(fan1A,fan1B)        
        elif message_str == "10":
            fan_stop(fan1A,fan1B)    
        elif message_str == "21":
            fan_start(fan2A,fan2B)
        elif message_str == "20":
            fan_stop(fan2A,fan2B) 
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
    client.subscribe(b"home/alarm")
    client.subscribe(b"home/evbos")
    client.subscribe(b"home/ESP-2")
    return client

def publish(topic, value):
    print("-----------")
    client.publish(topic, str(value))
    print(" {} topigine {}'degeri gonderildi!".format(topic, value))
    print("-----------")
    
def RestartAndConnect():
    sleep(2)
    machine.reset()
   
def fan_start(in1,in2):
    in1.value(1)
    in2.value(0)

def fan_stop(in1,in2):
    in1.value(0)
    in2.value(0)

alarm_flag = False

try:
    client = ConnectAndSubscribe()
except OSError as e:
    RestartAndConnect()
    
publish("ESP-2", 1)
while True:
    client.check_msg()
    if alarm_flag:
        if ses_sensor.value() == 1: 
            publish("home/alarm", 1)
            sleep(1)
        elif ates_sensor.value() == 0:
            publish("home/alarm", 1)
            sleep(1)                                                                                                                                                                                                                                


