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
    
    if topic == b"home/led":
        if message_str == "1":
            # LED açık
            print("LED açık")
        elif message_str == "0":
            # LED kapalı
            print("LED kapalı")
    elif topic == b"home/temperature":
        if message_str == "1":
            # Geçerli sıcaklık verisi
            print("Geçerli sıcaklık verisi")
        elif message_str == "0":
            # Geçersiz sıcaklık verisi
            print("Geçersiz sıcaklık verisi")
    elif topic == b"home/humidity":
        if message_str == "1":
            # Geçerli nem verisi
            print("Geçerli nem verisi")
        elif message_str == "0":
            # Geçersiz nem verisi
            print("Geçersiz nem verisi")
    elif topic == b"home/fan":
        if message_str == "1":
            # Fan açık
            print("Fan açık")
        elif message_str == "0":
            # Fan kapalı
            print("Fan kapalı")
    elif topic == b"home/door":
        if message_str == "open":
            # Kapı açık
            print("Kapı açık")
        elif message_str == "close":
            # Kapı kapalı
            print("Kapı kapalı")
    elif topic == b"bahce/nem":
        if message_str == "1":
            # Geçerli bahçe nem verisi
            print("Geçerli bahçe nem verisi")
        elif message_str == "0":
            # Geçersiz bahçe nem verisi
            print("Geçersiz bahçe nem verisi")
    elif topic == b"bahce/supom":
        if message_str == "1":
            # Bahçe su pompası açık
            print("Bahçe su pompası açık")
        elif message_str == "0":
            # Bahçe su pompası kapalı
            print("Bahçe su pompası kapalı")
    elif topic == b"home/kapı":
        if message_str == "open":
            # Ev kapısı açık
            print("Ev kapısı açık")
        elif message_str == "close":
            # Ev kapısı kapalı
            print("Ev kapısı kapalı")
    elif topic == b"home/pencere":
        if message_str == "open":
            # Ev penceresi açık
            print("Ev penceresi açık")
        elif message_str == "close":
            # Ev penceresi kapalı
            print("Ev penceresi kapalı")
    else:
        # Bilinmeyen mesaj veya topik
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

    
    