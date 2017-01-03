# -*- coding: utf-8 -*-

# подключение к БД
# mssql
# import pymssql
# conn = pymssql.connect(host='', user='', password='', database='')
# conn = pymssql.connect(host='mnssis-sql-test.branches.beloil.by', user='IT\\voip_service', password='V0ip$er', database='RCP_720')
# ok
from time import sleep
import logging
import logging.handlers
import cx_Oracle
from datetime import datetime
import os
from unidecode import unidecode
import json
import requests
import sys
import re

os.environ["NLS_LANG"] = "Russian.CL8MSWIN1251"

cur = None
unsuccessCount = 0

logname = re.findall(r'_(\w+)\.py', sys.argv[0])[0]  # ussd_[life, mts, velcom].py
# logging block
log = logging.getLogger('db')
log.setLevel(logging.INFO)
logfile = 'logs/{}_db.log'.format(logname)
hand = logging.handlers.TimedRotatingFileHandler(logfile, when='midnight', interval=1)
hand.setFormatter(logging.Formatter('%(levelname)-8s [%(asctime)s] %(message)s'))
log.addHandler(hand)
# logging block end


def db_connect():
    global cur
    global unsuccessCount
    try:
        con = cx_Oracle.connect('RCD_USSD/ubeysebyobstenu@10.93.1.24:21523/orclrcd')
        cur = con.cursor()
    except Exception as err:
        log.info('problem while connecting to db.\nerror\n {}'.format(err))
        sleep(10)
        db_connect()


db_connect()


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
    try:
        result = cx_Oracle.FIXED_CHAR
        # cur.callfunc('RCD.CHECKPHONE', result, ['+375295730676'])
        # {u'date': u'20.09.16', u'phone': u'+375295730676', u'cardlist': [{u'cardcode': u'2000000045665',
        # u'score': u'600', u'id': u'0'}, {u'cardcode': u'2000002456650', u'score': u'400', u'id': u'1'}]}
        json_cards = json.loads(cur.callfunc('RCD.CHECKPHONE', result, [msisdn]).rstrip())
        # {1: '2000000045665', 2: '2000002456650'}
        if json_cards['cardlist'] == 'none':
            subscriber_cards_dict = None
        else:
            subscriber_cards_dict = dict(enumerate(json_cards['cardlist'], 1))
        log.info('{} {}'.format(msisdn, subscriber_cards_dict))
        return subscriber_cards_dict
    except Exception as err:
        unsuccessCount += 1
        log.info('problem while checkphone for {}\n{}'.format(msisdn, err))


def card_information(card_id):
    global unsuccessCount
    # make db request with card id
    # return information about card
    try:
        json_card_info = json.loads(cur.callfunc('RCD.CARDINFO', cx_Oracle.FIXED_CHAR, [card_id]).rstrip())
        # {u'status': u' ', u'sumgoods': u'0', u'score': u'', u'lots2': u'', u'lots1': u'', u'distype': u'3', u'disvalue':
        # u'0', u'cardcode': u'00010'}
        # {u'status': 0, u'sumgoods': u'0', u'score': 0, u'lots2': 0, u'lots1': 0, u'distype': u'3', u'disvalue': u'0',
        # u'cardcode': u'00010'}
        log.info('{}'.format(json_card_info))
        return json_card_info
    except Exception as err:
        unsuccessCount += 1
        log.info('problem while getcardinfo for {}\n{}'.format(card_id, err))


def buyprize(card_number, lot_id):
    # update subs point value
    # '{"date":"05.10.2016 13:46:34","cardcode":"2000002456650","prizenum":"1","buyresult":"1",
    # "resultmessage":"▒▒▒▒▒▒▒▒▒▒ ▒▒▒▒ ▒▒▒▒▒▒, ▒▒▒ ▒▒▒▒▒▒▒ ▒ ▒▒▒▒▒▒▒ ▒▒▒▒▒▒."}'
    result = cx_Oracle.FIXED_CHAR
    json_buy_result = json.loads(cur.callfunc('RCD.SFLotsUSSDBuy', result, [card_number, 1]).rstrip().decode('cp1251'))
    log.info('{}'.format(json_buy_result))
    return json_buy_result


def current_lots():
    global unsuccessCount
    try:
        result = cx_Oracle.FIXED_CHAR
        date = datetime.today().strftime('%d%m%Y')
        # '{"date":"20.09.2016 10:29:58","prizelist":[{"prizenum":"1","prizename":"FORD EcoSport (Trend)",' \
        # '"prizecost":"500"},{"prizenum":"2","prizename":"Kruiz po stranam Karibskogo morya","prizecost":"500"},' \
        # '{"prizenum":"3","prizename":"Zapravka do polnogo baka","prizecost":"0"}]}'
        lots_json = json.loads(cur.callfunc('RCD.prizeinfo', result, [date]).rstrip())
        lots_list = lots_json['prizelist']
        if lots_list == 'none':
            prize_dict = None
        else:
            prize_dict = dict(enumerate(lots_list, 1))
        log.info('{}'.format(prize_dict))
        return prize_dict
    except Exception as err:
        unsuccessCount += 1
        log.info('problem while lots for {}\n{}'.format(date, err))


def prices():
    outurl2 = 'http://www.belorusneft.by/beloil-map/ussd/prices'
    try:
        r4 = requests.get(outurl2)
        print r4.json()['date']
        text = ''
        for i in r4.json()['prices']:
            text += '{} -> {} BYN\n'.format(unidecode(i['fuelname']), i['price'])

    except Exception as err:
        log.info('{}'.format(err.message))
        text = 'Net cen. Poprobyite pozhe.'
    return text


def actions():
    outurl1 = 'http://www.belorusneft.by/beloil-map/ussd/actions'
    try:
        r3 = requests.get(outurl1)
        text = ''
        for i in r3.json()['actions']:
            if unidecode(i['description']) not in text:
                text += '{}\n'.format(unidecode(i['description']))
        if len(text) > 160:
            text = text[:160]
    except Exception as err:
        log.info(err.message)
        text = 'Net akcii. Poprobyite pozhe.\n'
    return text
