# -*- coding: utf-8 -*-

# подключение к БД
# mssql
# import pymssql
# conn = pymssql.connect(host='', user='', password='', database='')
# conn = pymssql.connect(host='mnssis-sql-test.branches.beloil.by', user='IT\\voip_service', password='V0ip$er', database='RCP_720')

# import cx_Oracle
from datetime import datetime
import unidecode
import json

# con = cx_Oracle.connect('RCD_USSD/ubeysebyobstenu@10.93.1.24:21523/orclrcd')
# cur = con.cursor()


def msisdn_cards(msisdn):
    # select all subscriber data
    # return dict of subscriber info
    # +375295730676
    #msisdn = '+{}'.format(str(msisdn))
    #result = cx_Oracle.FIXED_CHAR
    #query_str = cur.callfunc('RCD.CHECKPHONE', result, [msisdn])  # return str format '||xxx||yyy||     '
    # {1: '2000000045665', 2: '2000002456650'}
    # subscriber_cards_dict = dict(enumerate([i for i in query_str.rstrip().split('||') if i != ''], 1))
    subscriber_cards_dict = {1: '2000000045665', 2: '2000002456650'}
    return subscriber_cards_dict


def card_information(card_id):
    # make db request with card id
    # return information about card
    # my_str = cur.callfunc('RCD.GetCardInfo', cx_Oracle.FIXED_CHAR, [card_id]).rstrip()
    # dict_obj = json.loads([i for i in my_str.split("'") if i != ''][0])
    # {u'status': u' ', u'sumgoods': u'0', u'score': u'', u'lots2': u'', u'lots1': u'', u'distype': u'3', u'disvalue':
    # u'0', u'cardcode': u'70833700950016667600010'}
    #for i in dict_obj:
    #    if dict_obj[i] == '' or dict_obj[i] == ' ':
    #        dict_obj[i] = 0
    dict_obj = {u'status': 0, u'sumgoods': u'0', u'score': 0, u'lots2': 0, u'lots1': 0, u'distype': u'3', u'disvalue':
        u'0', u'cardcode': u'70833700950016667600010'}

    return dict_obj



def change_info(card_number, lot_id):
    # update subs point value
    # print msisdn, 'in change_info'
    return "OK"

def current_lots():
    # result = cx_Oracle.FIXED_CHAR
    cur_date = '042016'
    # date = datetime.today().strftime('%m%Y')
    # cur.callfunc('RCD.LOTS', result, ['042016']).rstrip().decode('cp1251') # return in russian coding cp1251
    # '1:Krossover Pezho;2:Poezdka vo Frantsiiu na chempionat Evropy po futbolu na 3-kh;' - lots_str
    # lots_str = unidecode(cur.callfunc('RCD.LOTS', result, [cur_date]).rstrip().decode('cp1251'))
    # {1: '1:Krossover Pezho', 2: '2:Poezdka vo Frantsiiu na chempionat Evropy po futbolu na 3-kh'} - lots_dict
    # lots_dict = dict(enumerate([i for i in lots_str.split(';') if i != ''], 1))
    lots_dict = {1: '1:Krossover Pezho', 2: '2:Poezdka vo Frantsiiu na chempionat Evropy po futbolu na 3-kh'}
    return lots_dict