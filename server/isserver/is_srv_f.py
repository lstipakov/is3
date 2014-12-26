from twisted.python import log


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

