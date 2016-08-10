# -*- coding: utf-8 -*-
import commands, os, string


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
