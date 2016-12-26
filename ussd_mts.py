# -*- coding: utf-8 -*-

import logging
import sys
import smpplib.client
import smpplib.gsm
import smpplib.consts
from threading import Thread
import time
import ussd_submit
import subscriber
import request_analyze
import datetime


# logging.basicConfig(level='DEBUG')

def settings():
    f = open('settings', 'r')
    ip = f.readline().rstrip()
    port = f.readline().rstrip()
    sysId = f.readline().rstrip()
    passwd = f.readline().rstrip()
    f.close()
    return (ip, port, sysId, passwd)


def connect():
    # (ip, port, sysId, passwd) = settings()
    (ip, port, sysId, passwd) = ("87.252.242.70", "900", "bElNeFT", "b4eLOIl")
    try:
        client = smpplib.client.Client(ip, port)
        client.connect()   # TCP connection
        client.bind_transceiver(system_id=sysId, password=passwd)   # SMPP connection
    except smpplib.exceptions.PDUError as pduer:
        print pduer
        return 0
    except smpplib.exceptions.ConnectionError as coner:
        print coner
        return 0
    except smpplib.exceptions.UnknownCommandError as unkn:
        print unkn
        return 0
    return client


def send_info(pdu):
    if pdu.command == "deliver_sm":
        request_analyze.request(client, pdu)


while 1:
    try:
        client = connect()
        request_analyze.list_of_objects = {}
        if client:
            client.set_message_received_handler(
                lambda pdu: send_info(pdu))
            # thr = Thread(target=client.listen)
            # thr.start()
	    try:
                client.listen()
	        print "\n", "after listen", "\n"
            except Exception as err:
	        print err
 		continue
            # except AttributeError:
                # time.sleep(20)
                # continue
        else:
            time.sleep(20)
            continue
    except smpplib.exceptions.ConnectionError:
        time.sleep(20)
        continue


