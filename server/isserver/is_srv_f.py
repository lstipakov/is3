from twisted.python import log
import sys
from socket import *
serverHost = 'localhost'
serverPort = 12345


LOGGING = 0
DEBUGING = 1
STDIO_OFF = 0
PREFIX = '>>'




def cutline(line):
        i = line.find(r'/')
        if i != -1:
                log_msg('Removing trash from input line: ' + line)
                return line[i:]
        else:
            return '/SAY ' + line

def log_msg(msg):
    if STDIO_OFF == 0:
        print PREFIX + msg
    if LOGGING == 1:
        log.msg(msg)

def send_OK(msg):
    message = ['Estimate OK']
    sockobj = socket(AF_INET, SOCK_STREAM)
    sockobj.connect((serverHost, serverPort))
    sockobj.setblocking(0)
    for line in message:
        sockobj.send(line)

    sockobj.close()




