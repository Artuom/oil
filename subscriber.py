# -*- coding: utf-8 -*-


import db_interaction
from datetime import datetime
import json
from unidecode import unidecode

list_of_objects = []
a = []
daterange = ('01', '02', '03', '04')

class Subscriber:
    def __init__(self, msisdn):
        self.level = ""
        self.prize_dict = db_interaction.current_lots()  # {1: {}, 2: {}, 3: {}}
        self.msisdn = msisdn
        self.subscriber_cards_dict = db_interaction.msisdn_cards(self.msisdn)  # выборка из БД
        # {1: {u'cardcode': u'2000000045665', u'score': u'600', u'id': u'0'}, 2: {u'cardcode': u'2000002456650',
        # u'score': u'400', u'id': u'1'}}


    def __str__(self):
        return self.msisdn

    def error_msg(self):
        text = 'Unknown error. Try later!'
        sop = 0x03
        return text, sop

    def level_up(self, level):
        if len(self.level) == 3 and int(level) != 1:
            self.level += str(1) + str(int(level) - 1)
        elif len(self.level) == 6:
            self.level = self.level[:-2] + str(level)
        else:
            self.level += str(level)

    def level_down(self, level=None):
        if len(self.subscriber_cards_dict) == 1 and len(self.level) != 2 and len(self.level) != 3:
            self.level = '01'
        elif len(self.level) == 2:
            self.level = '0'
        elif len(self.level) == 3:
            if len(self.subscriber_cards_dict) == 1:
                self.level = '0'
            else:
                self.level = self.level[:2]
        else:
            self.level = self.level[:3]

    def make_change(self, value):
        # update subs_info with value where msisdn=self.msisdn
        if value > self.card_points:
            return None
        else:
            new_value = self.card_points - value
            db_interaction.change_info(self.msisdn, new_value)
        return new_value

    def current_lots(self):
        # receives dict of lots
        # {1: '1:Krossover Pezho', 2: '2:Poezdka vo Frantsiiu na chempionat Evropy po futbolu na 3-kh'}
        self.prize_dict = db_interaction.current_lots()  # {1: {}, 2: {}, 3: {}}

    def card_info(self, id):
        card_info = db_interaction.card_information(id)

    def answer_text(self):
        text = None
        sop = 0x03
        # first request
        # *xxx#
        if len(self.level) == 1:
            # level = 0
            text = "1. Upravlenie kartoi\n2. Actyal'nye akcii\n3. Ceny na toplivo\n"
            sop = 0x02
        # end first request
        elif len(self.level) == 2:
            # level = 0x
            my_str_cards = ''
            # esli karta odna i uroven' zaprosa info po karte, podnyat' level
            if len(self.subscriber_cards_dict) == 1 and self.level == '01':
                self.level_up(1)

            elif len(self.subscriber_cards_dict) != 1 and self.level == '01':
                if self.subscriber_cards_dict is None:
                    my_str_cards = 'U vas net dostupnih kart.'
                    text = "{}".format(my_str_cards)
                    sop = 0x03
                else:
                    my_str_cards = ''
                    for num, card in self.subscriber_cards_dict.iteritems():
                        my_str_cards += '{}: {}\n'.format(num, card['cardcode'])
                    text = "Viberete vashu kartu:\n{}".format(my_str_cards)
                    sop = 0x02


            # lots menu *xxx*2#
            elif self.level == '02':
                current_date = datetime.today().strftime('%d%m%Y')
                my_str_lots = ''
                for num, prize in self.prize_dict.iteritems():
                    my_str_lots += '{}:{}\n'.format(num, prize['prizename'])
                text = '{}\n{}\n0 - Nazad'.format(current_date, my_str_lots)
                sop = 0x02
                return text, sop
            # lots ends
            #
            # actions and discounts for fuel
            elif self.level == '03':
                text = 'You will receive an sms. Currently unavailable.'
                sop = 0x03
                return text, sop

        # card selection
        if len(self.level) == 3:
            # 01x
            # x = [2] - card id
            request_card_id = int(self.level[2])
            # card = self.subscriber_cards_dict[request_card_id]
            try:
                card = self.subscriber_cards_dict[request_card_id]  # card number
                # card_info = db_interaction.card_information(card)
                # proverka daty
                if datetime.today().strftime('%d') in daterange:
                    text = '{}\n1. Podrobnaya info po karte\nS 1 po 3 chislo mesyaca priobretenie shansov ' \
                           'ogranicheno. Povtorite popitku posle 3-go chisla.\n0 - Nazad'.format(card['cardcode'])
                    sop = 0x02
                elif self.prize_dict is None:
                    text = '{}\n1. Podrobnaya info po karte\nNa danniy moment net akcii\n0 - Nazad'.format(
                        card['cardcode'])
                    sop = 0x02
                else:
                    str_prz = ''
                    """
                    for key, value in dict.iteritems():
                        print '{}:{}'.format(key, value['prizename'])
                    """
                    # for key, value in self.prize_dict.iteritems():
                    #     str_prz += '{}:{}\n'.format(key, value['prizename'])
                    # str_prz = ""
                    text = 'Na karte {} ballov\n1. Podrobnaya info po karte\n2. Priobresti shans na priz 1(x500)\n3. ' \
                           'Priobresti shans na priz 2(x500)\n0 - Nazad'.format(card['score'])
                    sop = 0x02
            except IndexError as err:
                print err
                text = 'Unknown error. Try later.' + ' in card selection'
                sop = 0x03

        # card menu selection
        elif len(self.level) == 4:
            # 01xy
            # x = [2] - card_id
            # y = [3] - answer(info ili priobretenie shansa)
            request_card_id = int(self.level[2])
            answer = self.level[3]
            card = self.subscriber_cards_dict[request_card_id]  # card number
            print 'card ', card['cardcode']
            if int(answer) == 1:
                json_card_info = db_interaction.card_information(card['cardcode'])

                if json_card_info['chance'] == 'none':
                    count1 = 0
                    count2 = 0
                else:
                    count1 = 0
                    count2 = 0
                    for i in json_card_info[u'chance']:
                        if i['num'] == '1':
                            count1 = i['count']
                        if i['num'] == '2':
                            count2 = i['count']

                if json_card_info['discount'] in ('', ' '):
                    discount = 0
                else:
                    discount = json_card_info['discount']

                if datetime.today().strftime('%d') in daterange:
                    text = 'Skidka {disc}%\nPriobreteno soput.tovarov: {goods}rub\nBalli: {score}\nShansi priz 1: {first_count}' \
                           '\nShansi priz 2: {second_count}\nS 1 po 3 chislo mesyaca priobretenie shansov ' \
                           'ogranicheno.'.format(
                        disc=discount, first_count=count1, second_count=count2, **json_card_info)
                elif self.prize_dict is None:
                    text = 'Skidka {disc}%\nPriobreteno soput.tovarov: {goods}rub\nBalli: {score}\nShansi priz 1: {first_count}' \
                           '\nShansi priz 2: {second_count}\nNet akcii'.format(
                        disc=discount, first_count=count1, second_count=count2, **json_card_info)
                else:
                    text = 'Skidka {disc}%\nPriobreteno soput.tovarov: {goods}rub\nBalli: {score}\nShansi priz 1: {first_count}' \
                          '\nShansi priz 2: {second_count}\n1.Priobresti shans na priz 1\n2.Priobresti shans na priz 2'.format(
                        disc=discount, first_count=count1, second_count=count2, **json_card_info)


                sop = 0x02

            else:
                self.level_up('1')
                self.lvel_up(answer - 1)

        elif len(self.level) == 5:
            # 01xyz
            # x = [2] - card id
            # y = [3] - otvet(priobretenie shansa is menu card info)
            # z = [4] - shansa po y-1(id shansa)
            request_card_id = int(self.level[2])
            chance_id = int(self.level[4])  # 1 - info po karte, 2,3,4 cifri vibora = 1,2,3 id shansa
            date = datetime.today().strftime('%d')
            try:
                if str(date) in daterange or self.prize_dict is None:
                    text, sop = self.error_msg()
                else:
                    text = 'Priobresti shans na priz {}\n1.Da\n0.Net'.format(
                        self.prize_dict[int(chance_id)]['prizename'])
                    sop = 0x02
            except KeyError:
                text = 'Unknown error. Try later.'
                sop = 0x03

        elif len(self.level) == 6:
            request_card_id = int(self.level[2])
            chance_id = int(self.level[4])  # 1 - info po karte, 2,3,4 cifri vibora = 1,2,3 id shansa
            change_result = 0
            if int(self.level[5]) == 1:
                try:
                    json_buy_result = db_interaction.buyprize(self.subscriber_cards_dict[request_card_id]['cardcode'], chance_id)
                    # json_buy_result = json.dumps(json_buy_result)
                    # json_buy_result = json.loads(json_buy_result)
                except Exception as err:
                    print err
                    change_result = 1  # error
                if change_result == 1:  # error
                    text = 'Unknown error. Try later.'
                    sop = 0x03
                elif change_result == 0 and json_buy_result['buyresult'] != '1':
                    self.subscriber_cards_dict = db_interaction.msisdn_cards(self.msisdn)
                    text = 'Vi priobreli shans na priz {} {}\nPriobresti esche shans?\n1.Da, na priz 1\n2.Da, na priz ' \
                           '2'.format(json_buy_result['prizenum'], self.prize_dict[int(
                        json_buy_result['prizenum'])]['prizename'])
                    sop = 0x02
                elif change_result == 0 and json_buy_result['buyresult'] == '1':
                    # json_buy_result = json_buy_result.decode('cp1251')
                    text = unidecode(json_buy_result['resultmessage'])
                    sop = 0x02
                else:
                    text = 'Unknown error. Please, try later!'
                    sop = 0x03
            else:
                text = "Otmeneno pol'zovatelem"
                sop = 0x03

        return text, sop

    def __del__(self):
        print self.msisdn + ' finished'
        del self