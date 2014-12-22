from twisted.python import log


LOGGING = 0
DEBUGING = 1
STDIO_OFF = 0


def cutline(line):
        x = line.index(r'/')
        log_msg('Removing trash from input line: ' + line)

        return line[x:]

def log_msg(msg):
    if STDIO_OFF == 0:
        print '>>' + msg
    if LOGGING == 1:
        log.msg(msg)

