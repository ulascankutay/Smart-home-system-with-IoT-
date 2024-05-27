from simple import MQTTClient
import urequests as requests
import time
import network
import machine
import sensor
from machine import Pin


p0 = Pin(2, Pin.OUT)
         
secrets = {
   'mqtt_username' : 'ulascan',
   'mqtt_key' : '135790.Uk',
   'broker' : '59861b68801a421591bfed24cac1febf.s1.eu.hivemq.cloud',
   'port' : 8883
}


def subscribe_callback(topic,message):
    
    print(topic,message)
    
    message_str = message.decode('utf-8')
    
    if topic==b"home/led" and message_str=="1":
        p0.on()
    elif topic==b"home/led" and message_str=="0":
        p0.off()

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
    client.subscribe(b"home/siren")
    client.subscribe(b"home/led")
    client.subscribe(b"home/sıcaklık")
    client.subscribe(b"home/mq2")
    client.subscribe(b"home/role")
    client.subscribe(b"home/ldr")
    client.subscribe(b"home/fan")
    client.subscribe(b"home/kapı")
    client.subscribe(b"home/pencere")
    client.subscribe(b"home/hareket")
    client.subscribe(b"bahce/yagmur")
    client.subscribe(b"bahce/supom")
    return client


def publish(topic,value):
    print("-----------")
    client.publish(topic,str(value))
    print(" {} topigine {}'degeri gonderildi!".format(topic,value))
    print("-----------")
    
    
def RestartAndConnect():
    time.sleep(2)
    machine.reset()



try:
    client = ConnectAndSubscribe()
except OSError as e:
    RestartAndConnect()
cnt = 0
while True :
        temp = 25 #sensor.temperature()
        hum = 70 #sensor.humidity()
        cnt = cnt + 30
        client.wait_msg()
        time.sleep(0.2)
       
        dht_readings = {'field1':temp,'field2':hum,'field3':cnt}
        request = requests.post('https://api.thingspeak.com/update?api_key=ZT0I1PTFIIIBB0GE',json=dht_readings, headers = {'Content-Type': 'application/json'})
        request.close()
        time.sleep(0.2)

    
    