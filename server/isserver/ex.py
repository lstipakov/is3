from twisted.internet import reactor
from twisted.enterprise import adbapi
dbpool = adbapi.ConnectionPool("sqlite3", "logbase.db",check_same_thread=False)
def getName(email):
    dbpool.runQuery('insert into t_logs values(CURRENT_TIMESTAMP, ?)', ('testing',))
    return dbpool.runQuery("SELECT s_log FROM t_logs ")
def printResults(results):
    for elt in results:
        print elt[0]


def finish():
    dbpool.close()
    reactor.stop()

d = getName("jane@foo.com")
d.addCallback(printResults)
reactor.callLater(1, finish)
reactor.run()