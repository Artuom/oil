# -*- coding: utf-8 -*-

import socket
import sys
import time
import datetime
import kannel_send_sms

conn = socket.socket()
conn.bind(("", 8989))
conn.listen(10)
conn.setblocking(0)
conn.settimeout(0)

time_delay = time.time()
print time_delay
while 1:
    try:
        client, addr = conn.accept()
    except socket.error:  # данных нет
        cur_time = time.time()
        if cur_time - time_delay >= 115:
            continue
        continue
    else:  # данные есть
        client.setblocking(0)  # снимаем блокировку и тут тоже
    try:
        data = client.recv(1024)
    except socket.error as err:  # данных нет
        print err
        continue
    else:  # данные есть
        msisdn, text, network = data.split(';')
        kannel_send_sms.send_sms(msisdn, text, network)
