# -*- coding: utf-8 -*-
import commands, os, string


program = 'ussd_'
try:
    #выполняем команду 'ps' и присваиваем результат списку
    output = commands.getoutput("ps -f|grep " + program)
    proginfo = string.split(output)
    #выводим результат
    print "\n\
    Путь:\t\t", proginfo[5], "\n\
    Владелец:\t\t\t", proginfo[0], "\n\
    ID процесса:\t\t", proginfo[1], "\n\
    ID родительского процесса:\t", proginfo[2], "\n\
    Время запуска:\t\t", proginfo[4]
except:
    print "При выполнении программы возникла проблема!"
