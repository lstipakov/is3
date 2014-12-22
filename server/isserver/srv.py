
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory

import datetime
from is_protocol import *
from is_srv_f import *

def startlog():
    if LOGGING == 1:
        log.startLogging(open('logs/log' + str(datetime.datetime.now().date().day) + '.log', 'w'))



class ChatProtocolFactory(ServerFactory):

    protocol = ChatProtocol

    def __init__(self):
        self.clientProtocols = []

    def sendMessageToAllClients(self, mesg):
        for client in self.clientProtocols:
            client.sendLine(mesg)




if __name__ == '__main__':


    log_msg(">>Starting Server");
    factory = ChatProtocolFactory()

    reactor.listenTCP(12345, factory)
    if LOGGING:
        reactor.callLater(0.2, startlog)

    reactor.run()
