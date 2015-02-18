
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory

import datetime
from is_protocol import *
from is_srv_f import *

def startlog():
    if LOGGING == 1:
        log.startLogging(open('logs/log' + str(datetime.datetime.now().date().day) + '.log', 'w'))



class ISProtocolFactory(ServerFactory):

    protocol = ISProtocol
    NumCon = 0
    is_client = []


    def __init__(self):
        self.clientProtocols = []
        self.NumCon = 0
        self.is_client = []

    def sendMessageToAllClients(self, mesg):
        for client in self.clientProtocols:
            client.sendLine(mesg)





    def getClientsList(self):
        return [c.getName() for c in self.clientProtocols]

    def getNumCon(self):
        for client in self.clientProtocols:

            #print ISProtocol(client).name
            client.sendLine('Num conn ' + str(self.NumCon))

    def kickByName(self, name):
        for p in self.clientProtocols:
            if p.getName() == name:
                p.transport.loseConnection()

    def doStuff(self, param):
        log_msg("doing stuff for %s" % param)
        import time
        time.sleep(5)
        return "<job result for> %s" % param

if __name__ == '__main__':


    log_msg(">>Starting Server");
    factory = ISProtocolFactory()

    reactor.listenTCP(12345, factory)
    if LOGGING:
        reactor.callLater(0.2, startlog)

    reactor.run()
