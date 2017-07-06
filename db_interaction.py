# -*- coding: utf-8 -*-

# подключение к БД
# mssql
# import pymssql
# conn = pymssql.connect(host='', user='', password='', database='')
# conn = pymssql.connect(host='mnssis-sql-test.branches.beloil.by', user='IT\\voip_service', password='V0ip$er', database='RCP_720')
from time import sleep

# import cx_Oracle
from datetime import datetime
import os
from unidecode import unidecode
import requests
import json
import logging.handlers
import re
import sys

os.environ["NLS_LANG"] = "Russian.CL8MSWIN1251"
a = []
cur = None
unsuccessCount = 0


logname = re.findall(r'_(\w+)\.py', sys.argv[0])[0]  # ussd_[life, mts, velcom].py
# logging block
log = logging.getLogger('subscriber')
log.setLevel(logging.INFO)
# logfile = 'logs/{}_subscr.log'.format(logname)
logfile = '{}_subscr.log'.format(logname)
hand = logging.handlers.TimedRotatingFileHandler(logfile, when='midnight', interval=1)
hand.setFormatter(logging.Formatter('%(levelname)-8s [%(asctime)s] %(message)s'))
log.addHandler(hand)


def db_connect():
    global cur
    global unsuccessCount
    try:
        con = cx_Oracle.connect('RCD_USSD/ubeysebyobstenu@10.93.1.24:21523/orclrcd')
        cur = con.cursor()
    except:
        print 'problem while connecting to db'
        sleep(10)
        db_connect()


# db_connect()


def db_reconnect():
    db_connect()


def msisdn_cards(msisdn):
    # select all subscriber data
    # return dict of subscriber info
    # +375295730676
    global unsuccessCount
    if unsuccessCount >= 3:
        db_reconnect()
    msisdn = '+{}'.format(str(msisdn))

    """
    phone = json.loads(a)
    print phone['cardlist']
    print dict(enumerate(phone['cardlist'], 1))
    """
    # 2: {u'cardcode': u'2000002456650', u'score': u'400', u'id': u'1'}
    subscriber_cards_dict = {1: {u'cardcode': u'2000000045665', u'score': u'600', u'id': u'0'}, }
    # subscriber_cards_dict = None
    return subscriber_cards_dict


def card_information(card_id):
    json_card_info = {u'goods': u'57,25', u'discount': u'', u'chance': u'none', u'score': u'600', u'date': u'20.09.2016 10:29:58', u'cardcode': u'2000002456650'}
    return json_card_info


def buyprize(card_number, lot_id):
    # update subs point value
    json_buy_result = {u'date': u'05.10.2016 13:46:34', u'cardcode': u'2000002456650', u'buyresult': u'0', u'prizenum': u'1', u'resultmessage': u'\u2592\u2592\u2592\u2592\u2592\u2592\u2592\u2592\u2592\u2592 \u2592\u2592\u2592\u2592 \u2592\u2592\u2592\u2592\u2592\u2592, \u2592\u2592\u2592 \u2592\u2592\u2592\u2592\u2592\u2592\u2592 \u2592 \u2592\u2592\u2592\u2592\u2592\u2592\u2592 \u2592\u2592\u2592\u2592\u2592\u2592.'}
    return json_buy_result


def current_lots():
    global unsuccessCount
    prize_dict = {1: {u'prizenum': u'1', u'prizename': u'FORD EcoSport (Trend)', u'prizecost': u'500'}, 2: {u'prizenum': u'2', u'prizename': u'Kruiz po stranam Karibskogo morya', u'prizecost': u'500'}}
    return prize_dict


def prices():
    outurl2 = 'http://www.belorusneft.by/beloil-map/ussd/prices'
    try:
        r4 = requests.get(outurl2)
        print r4.json()['date']
        text = str(r4.json()['date'])+'\n'
        for i in r4.json()['prices']:
            text += '{} -> {} BYN\n'.format(unidecode(i['fuelname']), i['price'])
        return text
    except Exception as err:
        log.info('{}'.format(err.message))


def actions():
    outurl1 = 'http://www.belorusneft.by/beloil-map/ussd/actions'
    try:
        r3 = requests.get(outurl1)
        text = str(r3.json()['date']) + '\n'
        for i in r3.json()['actions']:
            text += '{}\n'.format(unidecode(i['description']))
    except Exception as err:
        log.info(err.message)
        text = 'Net akcii. Poprobyite pozhe.\n'
    return text