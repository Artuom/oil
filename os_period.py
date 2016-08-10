# -*- coding: utf-8 -*-
import commands, os, string


program = ['ussd_life.py', 'ussd_mts.py', 'ussd_velcom.py']
prid_dict = {}
for pr in program:
    try:
        output = commands.getoutput("ps -f|grep " + pr)
        proginfo = string.split(output)
        process_id = proginfo[1]
        starttime = proginfo[4]
        prid_dict[pr] = process_id
    except:
        pass

print prid_dict