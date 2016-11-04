# -*- coding: utf-8 -*-


import ussd_submit
import time
import subscriber
import ussd_submit
# import read_json
import logging

log = logging.getLogger('request_v')
log.setLevel(logging.INFO)
hand = logging.FileHandler('request_v.log', 'a')
hand.setFormatter(logging.Formatter('%(levelname)-8s [%(asctime)s] %(message)s'))
log.addHandler(hand)

list_of_objects = None
usr_obj = 0
service_key = "*877#"


def request(client, pdu):
    global usr_obj
    global list_of_objects
    log.info(pdu)
    if str(pdu.source_addr) in list_of_objects.keys() and pdu.short_message != service_key and pdu.ussd_service_op != '33':
        usr_obj = list_of_objects[str(pdu.source_addr)]
    elif pdu.ussd_service_op != '33':
        usr_obj = subscriber.Subscriber(pdu.source_addr)  # first request. object of subscriber class
        list_of_objects[str(pdu.source_addr)] = usr_obj

    if pdu.ussd_service_op is not None and pdu.ussd_service_op != 19 and pdu.ussd_service_op != 33 \
            and pdu.short_message == service_key:
        log.info('{}|{}|{}|{}'.format(str(pdu.source_addr), str(pdu.short_message), str(pdu.ussd_service_op),str(usr_obj.level)))
        response(client, pdu.source_addr, pdu.destination_addr, usr_obj, pdu.user_message_reference)

    elif (pdu.ussd_service_op is not None and int(pdu.ussd_service_op) != 19) and pdu.ussd_service_op != '33' \
            and pdu.short_message != service_key:
        log.info('{}|{}|{}|{}'.format(str(pdu.source_addr), str(pdu.short_message), str(pdu.ussd_service_op), str(usr_obj.level)))
        response(client, pdu.source_addr, pdu.destination_addr, usr_obj, pdu.user_message_reference, pdu.short_message)

    elif pdu.ussd_service_op is not None and (int(pdu.ussd_service_op) == 19 or int(pdu.ussd_service_op) == 33):
        log.info('{}|{}|{}|{}'.format(str(pdu.source_addr), str(pdu.short_message), str(pdu.ussd_service_op), str(usr_obj.level)))
        if int(pdu.ussd_service_op) == 19 and pdu.velc_notif:
            # '0x1120': 'Belorusneft'
            log.info('Rejected by {}'.format(pdu.source_addr))
            response(client, pdu.source_addr, pdu.destination_addr, usr_obj, pdu.user_message_reference,
                     'final')
        usr_obj.__del__()
        try:
            del list_of_objects[str(pdu.source_addr)]
        except AttributeError:
            pass

    else:  # rejected from subscriber side, session ending
        print "Rejected by " + pdu.source_addr
        try:
            usr_obj.__del__()
            del list_of_objects[str(pdu.source_addr)]
        except Exception as err:
            log.info("Can't delete {}: {}".format(pdu.source_addr, err.message))


def response(client, msisdn=0, src_addr=0, usr_obj=0, user_message_reference=None,  srctext=""):
    try:
        pass
    except IndexError:
        return 1
    ussd_service_op = 0x02
    if srctext == "":
        usr_obj.level_up(0)
    elif srctext != "" and srctext != 'final':
        if int(srctext) == 0:
            usr_obj.level_down()
        else:
            usr_obj.level_up(srctext)
    elif srctext == 'final':
        text = ''
        ussd_service_op = 0x20
        ussd_submit.submit(client, msisdn, src_addr, ussd_service_op, user_message_reference, text)
        return 1
    else:
        text = "Vash vibor prinyat"
        ussd_service_op = 0x03



    try:
        # text = level[usr_obj.level]
        text_request = usr_obj.answer_text()
        text = text_request[0]
        ussd_service_op = text_request[1]
    except Exception as err:
        text = "Unknown error. Try later!" + str(err)
        ussd_service_op = 0x03
    log.info('to submit: {}|{}|{}|{}|{}'.format(msisdn, src_addr, ussd_service_op, user_message_reference, text))
    ussd_submit.submit(client, msisdn, src_addr, ussd_service_op, user_message_reference, text)
    # usr.obj = 0 - 1 level
