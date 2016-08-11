# -*- coding: utf-8 -*-
import commands, os, string, sys


program = ['ussd_life.py', 'ussd_mts.py', 'ussd_velcom.py']
prid_dict = {}
for pr in program:
    try:
        output = commands.getoutput("ps -ef | grep " + pr)
        my_list = [my_str for my_str in output.split('\n') if 'python' in my_str]
        proginfo = string.split(my_list[0])
        process_id = proginfo[1]
        starttime = proginfo[4]
        prid_dict[pr] = process_id
    except:
        pass


def stop_services():
    for prid in prid_dict.values():
        commands.getoutput("sudo kill -9 " + prid)


def start_services():
    for ussdinstance in program:
        try:
            if prid_dict[ussdinstance]:
                print '{} is already up.'.format(ussdinstance[:-3])
        except KeyError:
            str_to_start = 'nohup python {} > /dev/null &'.format(ussdinstance)
            print str_to_start
            # to_start = commands.getoutput(str_to_start)
            # print 'Starting {}. With pid {}.'.format(ussdinstance[:-3], to_start)


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'stop':
            stop_services()
        if sys.argv[1] == 'start':
            start_services()
    except IndexError:
        start_services()