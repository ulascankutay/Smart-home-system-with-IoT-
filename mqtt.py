def subscribe_callback(topic,message):
    
    print(topic,message)
    
    message_str = message.decode('utf-8')
    
    if topic == b"home/led":
        if message_str == "10":
            LED.on()        
        elif message_str == "11":
            LED.off()    
        elif message_str == "20":
            LED1.on()
        elif message_str == "21":
            LED1.off()
        elif message_str == "30":
            LED2.on()
        elif message_str == "31":
            LED2.off()
        elif message_str == "40":
            LED3.on()
        elif message_str == "41":
            LED3.off()
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
    elif topic == b"bahce/supom":
        if message_str == "1":
            # Bahçe su pompası açık
            print("Bahçe su pompası açık")
        elif message_str == "0":
            # Bahçe su pompası kapalı
            print("Bahçe su pompası kapalı")
    elif topic == b"home/kapi":
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
