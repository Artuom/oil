# -*- coding: utf-8 -*-


import db_interaction
from datetime import datetime

list_of_objects = []


class Subscriber:
    def __init__(self, msisdn):
        self.level = ""
        # self.dict_of_lots = None
        self.dict_of_lots = db_interaction.current_lots()
        self.msisdn = msisdn
        self.subscriber_cards_dict = db_interaction.msisdn_cards(self.msisdn)  # выборка из БД
        # self.card_number = card_info["number"]  # card number
        # self.card_points = card_info["points"]  # value of points on the card

    def __str__(self):
        return self.msisdn

    def level_up(self, level):
        self.level += str(level)

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
        self.dict_of_lots = db_interaction.current_lots()

    def card_info(self, id):
        card_info = db_interaction.card_information(id)
    
    def answer_text(self):
        text = None
        text_skeleton = {
            "0": "1. Upravlenie kartoi\n2. Actyal'nye akcii\n3. Ceny na toplivo\n",
            "01": "Viberete vashu kartu:\n1: 1111\n2:2222",
            "011": "Na karte 5000 ballov\n1.Podrobnaya info po karte\n2.Priobretenie shansa na priz 1(x500 ballov)\n3.Priobretenie shansa na priz 2(x500 ballov)",
            "0111": "Status: 1(skidka 5%)\nBally: 1120\nShansy priz 1: 0\nShansy priz 2: 2'",
            "0112": "Priobresti shans na priz 1: avtomobil' Nissan Kashkai(500 ballov)\n1.Da\n",
            "01121": "",
            "0113": "Priobresti shans na priz 2: puteshestvie v Yaponiy na 2x(500 ballov)?\n1.Da"
            }
        if len(self.level) == 1:
            # level = 0
            text = "1. Upravlenie kartoi\n2. Actyal'nye akcii\n3. Ceny na toplivo\n"
            sop = 0x02
        elif len(self.level) == 2:
            # level = 0x
            my_str_cards = ''
            if len(self.subscriber_cards_dict) == 1 and self.level == '01':
                self.level_up(1)
                # level = 011 - 1st card id
                request_card_id = int(self.level[2])
                # card = self.subscriber_cards_dict[request_card_id]
                try:
                    card = self.subscriber_cards_dict[request_card_id]  # card number
                    # card_info = db_interaction.card_information(card)
                    text = '{}\n1. Podrobnaya info po karte\n2. Priobresti shans na priz 1\n3. Priobresti shans na ' \
                           'priz 2'.format(card)
                    sop = 0x02
                except IndexError:
                    text = 'Unknown error. Try later.'
                    sop = 0x03
                return text, sop

            elif self.level == '02':
                current_date = datetime.today().strftime('%m%Y')
                my_str_lots = ''
                for lot in self.dict_of_lots.values():
                    my_str_lots += '{}\n'.format(lot)

                text = '{}\n{}'.format(current_date, my_str_lots)
                sop = 0x03
                return text, sop

            elif self.level == '03':
                text = 'You will receive an sms. Currently unavailable.'
                sop = 0x03
                return text, sop

            for card in self.subscriber_cards_dict:
                my_str_cards += '{}:{}\n'.format(card, self.subscriber_cards_dict[card])
            if my_str_cards == '':
                my_str_cards = 'U vas net dostupnih kart.'
            dict_choice = {
                '01': "Viberete vashu kartu:\n{}".format(my_str_cards),
                # '02': '{}\n{}'.format(current_date, my_str_lots),
                # '03': 'You will receive an sms. Currently unavailable.'
            }
            # text = dict_choice[self.level]
            text = "Viberete vashu kartu:\n{}".format(my_str_cards)
            sop = 0x02

        elif len(self.level) == 3:  # card selection
            # 01x
            # x = [2] - card id
            request_card_id = int(self.level[2])
            # card = self.subscriber_cards_dict[request_card_id]
            try:
                card = self.subscriber_cards_dict[request_card_id]  # card number
                # card_info = db_interaction.card_information(card)
                text = '{}\n1. Podrobnaya info po karte\n2. Priobresti shans na priz 1\n3. Priobresti shans na priz 2'. \
                    format(card)
                sop = 0x02
            except IndexError:
                text = 'Unknown error. Try later.'
                sop = 0x03

        elif len(self.level) == 4:  # card menu selection
            # 01xy
            # x = [2] - card_id
            # y = [3] - otvet(info ili priobretenie shansa)
            request_card_id = int(self.level[2])
            answer = self.level[3]
            card = self.subscriber_cards_dict[request_card_id]  # card number
            card_info = db_interaction.card_information(card)
            if int(answer) == 1:
                text = "Status karti {card_info[status]}. Na karte {card_info[score]} ballov\nKuplenih shansov:\n"\
                       "priz 1 - {card_info[lots1]}\npriz 2 - {card_info[lots2]}".format(card_info=card_info)
                sop = 0x03
            elif int(answer) != 1:
                try:
                    text = 'Priobresti shans na priz {}\n1.Da\n2.Net'.format(self.dict_of_lots[int(answer) - 1])
                    sop = 0x02
                except IndexError:
                    text = 'Unknown error. Try later.'
                    sop = 0x03
            else:
                text = 'Unknown error. Try later.'
                sop = 0x03

        elif len(self.level) == 5:
            # 01xyz
            # x = [2] - card id
            # y = [3] - otvet(priobretenie shansa, !=1) - id lota
            # z = [3] - podtvergdenie na pokupku shansa po y-1(id shansa)
            request_card_id = int(self.level[2])
            chance_id = int(self.level[3]) - 1  # 1 - info po karte, 2,3 cifri vibora = 1,2 id shansa
            if int(self.level[4]) == 1:  # Otvet - Da
                try:
                    change_result = db_interaction.change_info(self.subscriber_cards_dict[request_card_id], chance_id)
                except Exception:
                    change_result = 1  # error
                if change_result == 1:  # error
                    text = 'Unknown error. Try later.'
                elif change_result == 0:
                    text = 'Vi priobreli shans na priz {}: {}'.format(chance_id, self.dict_of_lots[chance_id])
            else:
                text = "Otmeneno pol'zovatelem"
                sop = 0x03

        return text, sop

    def __del__(self):
        del self
        print "object deleted"
