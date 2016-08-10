# -*- coding: utf-8 -*-


import ussd_submit
import time
import subscriber
import ussd_submit
import read_json

level = read_json.read_menus()

list_of_objects = None
usr_obj = 0
service_key = "*877#"


def request(client, pdu):
    global usr_obj
    global list_of_objects
    if str(pdu.source_addr) in list_of_objects.keys() and pdu.short_message != service_key and pdu.ussd_service_op != '33':
        usr_obj = list_of_objects[str(pdu.source_addr)]
    elif pdu.ussd_service_op != '33':
        usr_obj = subscriber.Subscriber(pdu.source_addr)  # first request. object of subscriber class
        list_of_objects[str(pdu.source_addr)] = usr_obj

    if pdu.ussd_service_op is not None and pdu.ussd_service_op != 19 and pdu.ussd_service_op != 33 \
            and pdu.short_message == service_key:
        print "First request" + " " + str(pdu.ussd_service_op)
        response(client, pdu.source_addr, pdu.destination_addr, usr_obj, pdu.user_message_reference)

    elif (pdu.ussd_service_op is not None and int(pdu.ussd_service_op) != 19) and pdu.ussd_service_op != '33' \
            and pdu.short_message != service_key:
        print "Not first request" + "  " + str(pdu.ussd_service_op)
        response(client, pdu.source_addr, pdu.destination_addr, usr_obj, pdu.user_message_reference, pdu.short_message)

    elif pdu.ussd_service_op is not None and (int(pdu.ussd_service_op) == 19 or int(pdu.ussd_service_op) == 33):
        print "Third request while final confirmation" + " " + str(pdu.ussd_service_op)
        if int(pdu.ussd_service_op) == 33:
            response(client, pdu.source_addr, pdu.destination_addr, usr_obj, pdu.user_message_reference,
                     'final')
        usr_obj.__del__()
        try:
            del list_of_objects[str(pdu.source_addr)]
        except AttributeError:
            pass

    else:  # rejected from subscriber side, session ending
        print "Reject ", ' ', pdu.message_state
        try:
            usr_obj.__del__()
            del list_of_objects[str(pdu.source_addr)]
        except AttributeError:
            print "Can't delete"


def response(client, msisdn=0, src_addr=0, usr_obj=0, user_message_reference=None,  srctext=""):
    try:
        pass
    except IndexError:
        return 1
    ussd_service_op = 0x02
    if srctext == "":
        usr_obj.level_up(0)
    elif srctext != "":
        usr_obj.level_up(srctext)
    elif srctext == 'final':
        text = ''
        ussd_service_op = 0x32
        ussd_submit.submit(client, msisdn, src_addr, ussd_service_op, user_message_reference, text)
    else:
        text = "Vash vibor prinyat"
        ussd_service_op = 0x03

    print "Уровень ветки: %s" % usr_obj.level

    try:
        # text = level[usr_obj.level]
        text_request = usr_obj.answer_text()
        text = text_request[0]
        ussd_service_op = text_request[1]
    except Exception as err:
        text = "Unknown error. Try later!" + str(err)
        ussd_service_op = 0x03
    ussd_submit.submit(client, msisdn, src_addr, ussd_service_op, user_message_reference, text)
    # usr.obj = 0 - 1 level
