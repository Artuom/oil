# -*- coding: utf-8 -*-

import logging
import smpplib.client
import smpplib.gsm
import smpplib.consts
import sys
from threading import Thread
import subscriber
# import read_json


# logging.basicConfig(level='DEBUG')


def submit(client, msisdn, src_addr, ussd_service_op, user_message_reference=None,  text=""):
    try:
        parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(text)
    except:
        print parts, encoding_flag, msg_type_flag
        text = 'Unknown error. Try later!'
        parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(text)
    msisdn = str(msisdn)

    def hex_val(number):
        x = format(number, '04x')
        y = x[-2:] + x[:2]
        return int(y, base=16)

    if user_message_reference:
        user_message_reference = hex_val(user_message_reference)

    for part in parts:
        pdu = client.send_message(
            service_type='USSD',
            source_addr_ton=smpplib.consts.SMPP_TON_INTL,
            source_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
            source_addr=src_addr,
            dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
            dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
            esm_class=smpplib.consts.SMPP_MSGMODE_FORWARD,
            destination_addr=msisdn,
            short_message=part,
            data_coding=encoding_flag,
            registered_delivery=False,
            priority_flag=1,
            ussd_service_op=ussd_service_op,
            user_message_reference=user_message_reference,
        )
    wait = client.read_pdu()
    """if wait.message_id == None:
        submit(client, 1, "709")
    else:
        pass"""
    with open('data.log', 'a') as fh:
        # fh.write(time.strftime("%Y-%m-%d %H:%M:%S") + " Sent " + str(msisdn) + '\n')
        pass
    return wait.message_id
