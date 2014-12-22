from is_srv_f import *
from twisted.protocols.basic import LineOnlyReceiver
from pdb import line_prefix

CMD = [{'cmd': 'NAME', 'val' : None, 'pos': {}},
       {'cmd': 'EXIT', 'val' : None, 'pos': {}},
       {'cmd': 'TEST', 'val' : None, 'pos': {}},
       ]


def parse_val(line_val):
    return line_val

def get_line_pos(line_val):
    #return parse_val(line_val)
    return  None

def get_line_val(line_val):
    return parse_val(line_val)



def div_line(line):
    i = line.index(r' ')
    cmd = line[:i]
    cmd = cmd[1:]
    val = line[i:]
    c = {'cmd': cmd, 'val': get_line_val(val), 'pos': get_line_pos(val)}
    return c


def test_cmd(cmd):
    for x in CMD:
        if cmd in x['cmd']:
            log_msg('command OK')
            return True
        else:
            log_msg('command FAIL')
            return False

def parse_line(line):
    log_msg('>>Parsing input line: ' + line)
    line = cutline(line) #clear trash
    msg = div_line(line)
    if test_cmd(msg['cmd']):
        log_msg("   Command " + msg['cmd'] + " is OK")
    else:
        log_msg("   Command " + msg['cmd'] + " is not supported")

    log_msg('  Value of command: ' + msg['val'])
    return line


class ChatProtocol(LineOnlyReceiver):

    name = ""



    def getName(self):
        if self.name!="":
            return self.name
        return self.transport.getPeer().host

    def connectionMade(self):
        log_msg("New connection from "+self.getName())
        self.sendLine("Welcome to my my chat server.")
        self.sendLine("Send '/NAME [new name]' to change your name.")
        self.sendLine("Send '/EXIT' to quit.")
        self.factory.sendMessageToAllClients(self.getName()+" has joined the party.")
        self.factory.clientProtocols.append(self)

    def connectionLost(self, reason):
        log_msg("Lost connection from "+self.getName())
        self.factory.clientProtocols.remove(self)
        self.factory.sendMessageToAllClients(self.getName()+" has disconnected.")


    def line_protocol1(self, line):

        if line[:5] == "/NAME":
            oldName = self.getName()
            self.name = line[5:].strip()
            self.factory.sendMessageToAllClients(oldName+" changed name to "+self.getName())


        elif line == "/EXIT":
            self.transport.loseConnection()


        elif line[:5] == "/TEST":
            log_msg('Testing')
            self.factory.sendMessageToAllClients('Test OK')


        else:
            self.factory.sendMessageToAllClients(self.getName()+" says "+line)
    def lineReceived(self, line):
        print self.getName()+" said "+line

        line = parse_line(line)
        self.line_protocol1(line)


    def sendLine(self, line):
        self.transport.write(line+"\r\n")


if __name__ == '__main__':
    print '---------'

    parse_line('zzzzz/NAME oleg')

