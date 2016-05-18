# -*- coding=utf8 -*-
import Queue,threading,asyncore,time,socket
import redisclient as rc
import configparser as cf
from redisreplycallback import RedisReplyCallback
import redisreplyhandler as rrh

exec_interval = 60 # send command "info" to redis

def timer_check_connection(collector):
    for p in collector.peers:
        if not (p.is_connected() or p.is_connecting()):
            #print "{0}: connecting {1}:{2}".format(time.time(), p.host, p.port)
            p.connect()
    threading.Timer(conn_timeout, timer_check_connection, args=[collector]).start()

def timer_add_cmd(collector):
    for p in collector.peers:
        if p.is_connected():
            print "{0}: add_cmd {1}:{2}".format(time.time(), p.host, p.port)
            p.add_cmd()
    threading.Timer(exec_interval, timer_add_cmd, args=[collector]).start()


#
class ReidsInfoCollector(RedisReplyCallback):
    svraddrlist = []
    peers = []
    queue = Queue.Queue()
    is_start = False

    def __init__(self):
        self.worker = threading.Thread(target=self._run, name = "collector service")

    def set_server_list(self, sl):
        self.svraddrlist = sl

    def set_reply_service(self, rs):
        self.reply_service = rs

    def _run(self):
        print "ReidsInfoCollector::_run"
        #threading.Timer(conn_timeout, timer_check_connection, args = [self]).start()
        threading.Timer(exec_interval, timer_add_cmd, args = [self]).start()

        # If you want to handle "global" poll timeout event of asyncore.loop, create a empty 
        # asyncore.dispatcher object with readable() return False ,then call 
        # create_socket, which will add the object to poll list, causing unproper disconnect event, now we can
        # handle the "global" poll timeout event inside the object's writeable() function.

        for item in self.svraddrlist:
            c = rc.RedisClient(item[0], item[1], item[2], item[3])
            c.set_callback(self)
            c.asyn_info() 
            c.create_socket(socket.AF_INET, socket.SOCK_STREAM) 
            self.peers.append(c)

        asyncore.loop(0.1)

    def start(self):
        if self.is_start:
            return True
        
        self.is_start = True
        self.worker.start()

    # RedisReplyCallback implement 
    def on_info(self, redisid, redisname, data):
        #print "{0}: on_info".format(time.time())
        item = rrh.ReplyItem(redisid, redisname, "info", data, time.time())
        self.reply_service.add_reply(item)



