from is_srv_f import *
from twisted.protocols.basic import LineOnlyReceiver
#from pdb import line_prefix
from twisted.enterprise import adbapi
from send_task import send_msg

CMD = [{'cmd': 'NAME', 'val' : None, 'pos': {}},
       {'cmd': 'EXIT', 'val' : None, 'pos': {}},
       {'cmd': 'TEST', 'val' : None, 'pos': {}},
       {'cmd': 'TASK', 'val' : None, 'pos': {}},
       {'cmd': 'CALC_EST', 'val' : None, 'pos': {}},
       {'cmd': 'CALC_TRAFF', 'val' : None, 'pos': {}},
       {'cmd': 'SAY', 'val' : None, 'pos': {}},
       {'cmd': 'CLI_LIST', 'val' : None, 'pos': {}},
       {'cmd': 'NUMCON', 'val' : None, 'pos': {}}
       ]
log_msg('Connecting to log database....')
try:
    dbpool = adbapi.ConnectionPool("sqlite3", 'logbase.db',check_same_thread=False)

except:
    dbpool = None


#==========================================db routinies
def db_ins_log(msg):
    if dbpool != None:
        try:
            dbpool.runQuery('insert into t_logs values(CURRENT_TIMESTAMP, ?)', (msg,))
        except:
            log_msg('Error query')

#=================================================parsing
def parse_val(line_val):
    return line_val

def get_line_pos(line_val):
    #return parse_val(line_val)
    return  None

def get_line_val(line_val):
    return parse_val(line_val)

def div_line(line):
    i = line.find(r' ')
    if i == -1:
        i = len(line)

    cmd = line[:i]
    cmd = cmd[1:]
    val = line[i:]
    c = {'cmd': cmd, 'val': get_line_val(val), 'pos': get_line_pos(val)}
    return c


def test_cmd(cmd):
    res = False
    for x in CMD:

        if cmd in x['cmd']:
            res = True
        else:
            if res == False:
                res = False

    return res

def parse_line(line):
    log_msg('>>Parsing input line: ' + line)
    line = cutline(line) #clear trash
    if line != '':

        msg = div_line(line)
        if test_cmd(msg['cmd']):
            log_msg("   Command " + msg['cmd'] + " is OK")
        else:
            log_msg("   Command " + msg['cmd'] + " is not supported")

        log_msg('  Value of command: ' + msg['val'])
    return msg

#=================================== end of parsing


#=================================================twisted
class ISProtocol(LineOnlyReceiver):
    def getName(self):
        return self.name
    
    def connectionMade(self):
        self.name = str(self.transport.getPeer())
        log_msg("New connection from "+self.getName())
        self.sendLine("Welcome to ISserver.")
        self.sendLine("Send '/NAME [new name]' to change your name.")
        self.sendLine("Send '/TEST ' to get test message.")
        self.sendLine("Send '/CLI_LIST ' to get list of clients.")
        self.sendLine("Send '/NUMCON ' to get count of connections.")
        self.sendLine("Send '/TASK [command] ' to send command into queue.")
        self.sendLine("Send '/CALC_EST [id] ' to send command into queue on calculate estimate.")
        self.sendLine("Send '/CALC_TRAFF [id] ' to send command into queue on calculate traffic.")
        self.sendLine("Send '/KICK [name]' to kick client.")
        self.sendLine("Send '/EXIT' to quit.")

        self.factory.sendMessageToAllClients(self.getName()+" has joined the party.")
        self.factory.clientProtocols.append(self)

        c = [{'id_con': 0, 'con_name': self.getName()}]
        #self.factory.is_clients.append(c)
        self.factory.NumCon += 1

    def connectionLost(self, reason):
        log_msg("Lost connection from "+self.getName())
        self.factory.clientProtocols.remove(self)
        self.factory.sendMessageToAllClients(self.getName()+" has disconnected.")
        self.factory.NumCon -= 1


    def line_protocol1(self, line):
        cmd = line['cmd']
        val = line['val']
        db_ins_log(str(cmd))
        if cmd == "NAME":
            oldName = self.getName()

            self.name = val.strip()
            self.factory.sendMessageToAllClients(oldName+" changed name to "+self.getName())


        elif cmd == "EXIT":
            self.transport.loseConnection()


        elif cmd == "TEST":
            log_msg('Testing')
            self.factory.sendMessageToAllClients('Test OK')
        elif cmd == "TASK":
                send_msg(val)

        elif cmd == "CALC_EST":
                send_msg(val, is_queue='est')

        elif cmd == "CLI_LIST":
            log_msg('Request list of connections')
            clients = self.factory.getClientsList()
            for c in clients:
                self.sendLine(c)    

        elif cmd == "NUMCON":
            log_msg('Request count of connections')
            self.sendLine(str(self.factory.NumCon))
            #self.factory.getNumCon()

        elif cmd == 'SAY':
            self.factory.sendMessageToAllClients(self.getName()+" says "+val)

        elif cmd == "KICK":
            self.factory.kickByName(val.strip())

        else:
            self.factory.sendMessageToAllClients(self.getName()+" says "+val)

    def lineReceived(self, line):
        print self.getName()+" said "+line

        line = parse_line(line)
        self.line_protocol1(line)


    def sendLine(self, line):
        self.transport.write(line+"\r\n")
#==================================================================end of twisted

if __name__ == '__main__':
    print '---------'
    parse_line('zzzzz/EXIT')
    dbpool1 = adbapi.ConnectionPool("sqlite3", "logbase.db",check_same_thread=False)
    #dbpool1.
    dbpool1.openQuery('insert into t_logs values(CURRENT_TIMESTAMP, ?)', '11111')
    #db_ins_log('!!!!!!!!!!!!')

