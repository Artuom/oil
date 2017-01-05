# -*- coding: utf-8 -*-

import logging
import smpplib.client
import smpplib.gsm
import smpplib.consts
import sys
import re
from threading import Thread
import subscriber
# import read_json

logname = re.findall(r'_(\w+)\.py', sys.argv[0])[0]  # ussd_[life, mts, velcom].py
# logging block
log = logging.getLogger('sbm')
log.setLevel(logging.INFO)
logfile = 'logs/{}_submit.log'.format(logname)
hand = logging.handlers.TimedRotatingFileHandler(logfile, when='d', interval=1)
hand.setFormatter(logging.Formatter('%(levelname)-8s [%(asctime)s] %(message)s'))
log.addHandler(hand)
# logging block end


def submit(client, msisdn, src_addr, ussd_service_op, user_message_reference=None,  text=""):
    try:
        if text is not None:
            log.info('text length {} to submit: {}'.format(len(text), text))
            if len(text) > 160:
                text = text[:160]
        else:
            log.info('text length {} to submit: {}'.format('text is None', text))
        parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(text)
    except Exception as err:
        log.info('text to submit in exception: {}'.format(err.message))
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
            source_addr_ton=smpplib.consts.SMPP_TON_UNK,
            source_addr_npi=smpplib.consts.SMPP_NPI_UNK,
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
    log.info('text was sent: {}: {}'.format(pdu.destination_addr, pdu.short_message))
    return 1
