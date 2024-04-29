from simple import MQTTClient
import urequests as requests
import time
import network
import machine
import sensor

secrets = {
   'mqtt_username' : 'ulascan',
   'mqtt_key' : '135790.Uk',
   'broker' : '59861b68801a421591bfed24cac1febf.s1.eu.hivemq.cloud',
   'port' : 8883
}

topic_sub=b"Fan"

"""
branch 
"""


def subscribe_callback(topic,message):
    print((topic,message))
    if message == b'LED1 ON':
        LED.on()
        print('Led On yapıldı')
    if message == b'LED1 OFF':
        LED.off()
        print('Led Off yapıldı')

def ConnectAndSubscribe():
    sslparams = {'server_hostname': secrets["broker"]}
    client = MQTTClient(client_id="esp32-R1",
                    server=secrets["broker"],
                    port=secrets["port"],
                    user=secrets["mqtt_username"],
                    password=secrets["mqtt_key"],
                    keepalive=3600,
                    ssl=True,
                    ssl_params=sslparams) 
    client.set_callback(subscribe_callback)
    client.connect()
    client.subscribe(topic_sub)
    #print('connected to',mqtt_server, 'MQTT Broker', 'subscribed to',topic_sub,'topic')
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
    hum = 60 #sensor.humidity()
    cnt = cnt + 20
    dht_readings = {'field1':temp,'field2':hum,'field3':cnt}
    #request = requests.post('https://api.thingspeak.com/update?api_key=ZT0I1PTFIIIBB0GE',json=dht_readings, headers = {'Content-Type': 'application/json'})
    #request.close()
    
    time.sleep(1)