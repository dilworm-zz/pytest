#-*-coding=utf8-*-
import configparser as cf
import redisinfocollector as ric
import redisreplyhandler as rrh
import time, logging

def initlogger():
    FORMAT = "%(asctime)s [%(levelname)-.7s] %(message)s"
    logFormatter = logging.Formatter(FORMAT)
    g_cflogger = logging.getLogger("cf")
    g_cflogger.setLevel(logging.DEBUG)
    fileHandle = logging.FileHandler("{0}.log".format("testlog"))
    fileHandle.setFormatter(logFormatter)
    fileHandle.setLevel(logging.WARN)
    g_cflogger.addHandler(fileHandle)
    consoleHandle = logging.StreamHandler()
    consoleHandle.setFormatter(logFormatter)
    consoleHandle.setLevel(logging.DEBUG)
    g_cflogger.addHandler(consoleHandle)

initlogger()

serverlist = cf.GetServerList('./config/serverlist.txt')
#serverlist = cf.GetServerList('./redisinfo/serverlist.txt')
print "{0}:Loading server list:".format(time.time())
for addr in serverlist:
    print addr[0], addr[1]
    
reply_service = rrh.RedisReplyService()
collector = ric.ReidsInfoCollector()
collector.set_server_list(serverlist)
collector.set_reply_service(reply_service)

reply_service.start()
collector.start()
