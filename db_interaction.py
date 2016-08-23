# -*- coding: utf-8 -*-

# подключение к БД
# mssql
# import pymssql
# conn = pymssql.connect(host='', user='', password='', database='')
# conn = pymssql.connect(host='mnssis-sql-test.branches.beloil.by', user='IT\\voip_service', password='V0ip$er', database='RCP_720')
from time import sleep

import cx_Oracle
from datetime import datetime
import os
from unidecode import unidecode
import json

os.environ["NLS_LANG"] = "Russian.CL8MSWIN1251"

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
        query_str = cur.callfunc('RCD.CHECKPHONE', result, [msisdn]) # return str format '||xxx||yyy||     '
        # {1: '2000000045665', 2: '2000002456650'}
        subscriber_cards_dict =  dict(enumerate([i for i in query_str.rstrip().split('||') if i != ''], 1))
        return subscriber_cards_dict
    except:
        unsuccessCount += 1
        print 'problem while checkphone for {}'.format(msisdn)


def card_information(card_id):
    global unsuccessCount
    # make db request with card id
    # return information about card
    try:
        my_str = cur.callfunc('RCD.GetCardInfo', cx_Oracle.FIXED_CHAR, [card_id]).rstrip()
        dict_obj = json.loads([i for i in my_str.split("'") if i != ''][0])
        # {u'status': u' ', u'sumgoods': u'0', u'score': u'', u'lots2': u'', u'lots1': u'', u'distype': u'3', u'disvalue':
        # u'0', u'cardcode': u'00010'}
        for i in dict_obj:
            if dict_obj[i] == '' or dict_obj[i] == ' ':
                dict_obj[i] = 0
        # {u'status': 0, u'sumgoods': u'0', u'score': 0, u'lots2': 0, u'lots1': 0, u'distype': u'3', u'disvalue': u'0',
        # u'cardcode': u'00010'}
        return dict_obj
    except:
        unsuccessCount += 1
        print 'problem while getcardinfo for {}'.format(card_id)


def change_info(card_number, lot_id):
    # update subs point value
    print msisdn, 'in change_info'
    return "OK"


def current_lots():
    global unsuccessCount
    try:
        result = cx_Oracle.FIXED_CHAR
        cur_date = '042016'
        # date = datetime.today().strftime('%m%Y')
        # cur.callfunc('RCD.LOTS', result, ['042016']).rstrip().decode('cp1251') # return in russian coding cp1251
        # '1:Krossover Pezho;2:Poezdka vo Frantsiiu na chempionat Evropy po futbolu na 3-kh;' - lots_str
        lots_str = unidecode(cur.callfunc('RCD.LOTS', result, [cur_date]).rstrip().decode('cp1251'))
        # {1: '1:Krossover Pezho', 2: '2:Poezdka vo Frantsiiu na chempionat Evropy po futbolu na 3-kh'} - lots_dict
        lots_dict = dict(enumerate([i for i in lots_str.split(';') if i != ''], 1))
        return lots_dict
    except:
        unsuccessCount += 1
        print 'problem while lots for {}'.format(cur_date)
