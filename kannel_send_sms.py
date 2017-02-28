# -*- coding: utf-8 -*-

import requests


def send_sms(msisdn, text, network):
    try:
        text = text.encode('utf-8')
        print text
        r = requests.get("http://localhost:13003/cgi-bin/sendsms?smsc=life&username=user_life&"
                        "password=usrlife&coding=2&to={}&text={}&charset=UTF-8".format(msisdn, text))
        return r
    except Exception as err:
        print err

