# -*- coding: utf-8 -*-

import socket
sock = socket.socket()
sock.connect(('localhost', 8989))
sock.send('111',)
sock.close()

#print data