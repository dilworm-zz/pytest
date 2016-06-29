#-*-coding=utf8-*-
import time
import configparser as cf
import redisinfocollector as ric
import redisreplyhandler as rrh

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
