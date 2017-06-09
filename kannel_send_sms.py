# -*- coding: utf-8 -*-

import requests


def send_sms(msisdn, text, network):
    try:
        text = text.encode('utf-8')
        text = text.replace('%', "%25")
        if network == 'life':
            r = requests.get("http://localhost:13003/cgi-bin/sendsms?smsc=life&username=user_life&"
                            "password=usrlife&coding=2&from=9226&to={}&text={}&charset=UTF-8".format(msisdn, text))
            return 1
        elif network == 'velcom':
            r = requests.get("http://localhost:13003/cgi-bin/sendsms?smsc=velcom&username=user_velcom&"
                             "password=usrvelcom&coding=2&from=99973&to={}&text={}&charset=UTF-8".format(msisdn, text))
            return 1
        else:
            return 1

    except Exception as err:
        print err

