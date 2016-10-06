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
import json

os.environ["NLS_LANG"] = "Russian.CL8MSWIN1251"
a = []
cur = None
unsuccessCount = 0


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
    prize_dict = {1: {u'prizenum': u'1', u'prizename': u'FORD EcoSport (Trend)', u'prizecost': u'500'}, 2: {u'prizenum': u'2', u'prizename': u'Kruiz po stranam Karibskogo morya', u'prizecost': u'500'}, 3: {u'prizenum': u'3', u'prizename': u'Zapravka do polnogo baka', u'prizecost': u'0'}}
    return prize_dict
