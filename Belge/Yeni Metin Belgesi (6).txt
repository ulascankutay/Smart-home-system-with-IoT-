from machine import ADC,Pin
from time import sleep
from robust import MQTTClient
import dht
import network
import umail
import ntptime



adc = ADC(0)
sensor = dht.DHT11(Pin(16))
buzzer= Pin(13, Pin.OUT)
relay1 = Pin(5, Pin.OUT)
relay2 = Pin(4, Pin.OUT)
yagmurSen = Pin(10, Pin.IN,)

relay1.value(1)
relay2.value(1)


config =      {'host'       : 'smtp.gmail.com',
               'port'       : 587,
               'username'   : 'nameulas@gmail.com',
               'password'   : 'jliz lhzw fijq yvgn',
               'from_name'  : 'ESP8266',
               'to_name'    : 'Ulas Can',
               'to'         : 'ulascankutay@gmail.com',
               'subject'    : '',
               'text'       : ''}

#=======================================================
THINGSPEAK_MQTT_CLIENT_ID = b"PSwCHCQEFSUhNBs6LB4OIBo"
THINGSPEAK_MQTT_USERNAME = b"PSwCHCQEFSUhNBs6LB4OIBo"
THINGSPEAK_MQTT_PASSWORD = b"4l9qnjbn3We2fzaYmvi6T3Ej"
THINGSPEAK_CHANNEL_ID = b'2511429'
#=======================================================

THINGSPEAK_MQTT_USERNAME = THINGSPEAK_MQTT_CLIENT_ID

client = MQTTClient(server=b"mqtt3.thingspeak.com",
                    client_id=THINGSPEAK_MQTT_CLIENT_ID, 
                    user=THINGSPEAK_MQTT_USERNAME, 
                    password=THINGSPEAK_MQTT_PASSWORD, 
                    ssl=False)
                    
try:            
    client.connect()
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()


def  send_mail(congif):
    print("mail gönderiliyor..")
    smtp = umail.SMTP(config['host'], config['port'], username=config['username'], password=config['password'])
    smtp.to(config['to'])
    smtp.write("From: {0} <{0}>\n".format(config['from_name'], config['username']))
    smtp.write("To: {0} <{0}>\n".format(config['to_name'], config['to']))
    smtp.write("Subject: {0}\n".format(config['subject']))
    smtp.send(config['text'])
    smtp.quit()
    print("mail gönderildi")


def dht_sensor():
    try:
        sleep(2)
        sensor.measure()
        t = sensor.temperature()
        h = sensor.humidity()
        """
        print('Sıcaklık: %3.1f C' %t)
        print('Nem: %3.1f %%' %h)
        
        """
    except OSError as e:
        print('sensör okunmadı')
        
    return [t,h]


def toprak_sensor():
    sleep(0.1)
    deger= adc.read()
    yüzde =100 -((100 * deger) / 1024)
    return [deger,yüzde]


def water_pump():
    
    deger, yüzde = toprak_sensor()
    sıcaklık, nem = dht_sensor()
    if yüzde<10 or sıcaklık >50:
        buzzer.on()
        relay1.value(0)
        sleep(0.5)
    else :
        buzzer.off()
        relay1.value(1)
        sleep(1)
    return relay1.value()

PUBLISH_PERIOD_IN_SEC = 5
while True:
    sıcaklık, nem = dht_sensor()
    sleep(0.1)
    deger, yüzde = toprak_sensor()
    sleep(0.1)
    yagmurDurum=yagmurSen.value()
    if yagmurDurum == 0:
        config['text'] ="Yağmur başladı  "
        config['subject']="Yağış Uyarısı "
        send_mail(config)      
    if yüzde<10:
        config['text'] ="Nem oranı düşük %10"
        config['subject']="Nem Oranı "
        send_mail(config)    
    sleep(0.1)
    try:
        freeHeapInBytes = gc.mem_free()
        credentials = bytes("channels/{:s}/publish".format(THINGSPEAK_CHANNEL_ID), 'utf-8')  
        payload = bytes("field1={:.1f}&field2={:.1f}&field3={:.1f}&field4={:.1f}\n".format(sıcaklık, nem, yüzde,yagmurDurum), 'utf-8')
        client.publish(credentials, payload)
        sleep(PUBLISH_PERIOD_IN_SEC)
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        client.disconnect()
        break



