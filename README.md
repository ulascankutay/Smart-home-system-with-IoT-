
# Smart Home System With IoT


"Smart Home System With IoT" projesi, ESP32 kartı ve MicroPython programlama dili kullanılarak geliştirilmektedir. Bu projenin amacı, ev sahiplerine evlerini uzaktan kontrol etme ve izleme imkanı sunmaktır. ESP32 kartı, ev içindeki cihazlarla iletişim kurarak kullanıcıların ışıkları, elektronik cihazları, fanları ve diğer ev sistemlerini uzaktan yönetmelerini sağlar. Ayrıca projede, bahçe için toprak nem sensörü ve sulama pompası gibi unsurlar da bulunmaktadır. Bu sensörler, bahçe toprağının nem seviyesini ölçer ve gerektiğinde sulama pompasını çalıştırarak bitkilerin sulanmasını sağlar. Projede ayrıca yanıcı gaz algılama sensörleri, sıcaklık sensörleri ve kapı kontrol sistemleri gibi güvenlik ve konfor unsurları da yer almaktadır. Bu şekilde, kullanıcılar evlerinin iç ve dış mekanlarını güvenli bir şekilde kontrol edebilir ve enerji tasarrufu sağlayabilirler. Proje, iki kişi tarafından geliştirilmekte olup, her biri belirli görevleri üstlenerek projenin başarılı bir şekilde tamamlanmasını hedeflemektedir.
## Yazarlar ve Teşekkür

- [@keremtozann](https://github.com/keremtozann) tasarım ve geliştirme için.

## Bilgisayarınızda Çalıştırın

Projeyi klonlayın

```bash
  git clone https://github.com/ulascankutay/Smart-home-system-with-IoT-.git
```

Proje dizinine gidin

```bash
  cd my-project
```

Gerekli paketleri yükleyin

```bash
  npm install
```

Sunucuyu çalıştırın

```bash
  npm run start
```

  
## Sensör/Örnekler

```python
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
   
```

```python
def hcr_sensor():
    try :
        mesafe = usensor.distance_cm()
        print(mesafe,"\n")
        sleep(2)
    except KeyboardInterrupt:
        pass 

```
```python
def mq_sensor():
    sleep(1)
    deger = adc.read()
    print("gaz değeri :",deger)
    sleep(1)
   
```
## Yol haritası

- Ek Sensör desteği

- Daha fazla entegrasyon ekleme

  
## Kullanılan Teknolojiler

- MQTT 
- Thingspeek
- ESP32
- MicroPython

  
## İlişkili Projeler

İşte bazı ilgili projeler

[IoT Greenhouse](https://github.com/ulascankutay/ulascankutay-IoT-smart-greenhouse)

  
## Ekran Görüntüleri

![ER Diagram](https://github.com/ulascankutay/Smart-home-system-with-IoT-/blob/main/Belge/proje.png)


## Tamamlanmıs Maket  

![ER Diagram](https://github.com/ulascankutay/Smart-home-system-with-IoT-/blob/main/Belge/son.jpeg)


## Lisans

[MIT](https://github.com/ulascankutay/Smart-home-system-with-IoT-/blob/main/MIT.txt)

  