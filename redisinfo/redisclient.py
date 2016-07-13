#-*-coding=utf8-*-
import asyncore, socket, time
import redisproto as rp
import threading
import traceback
import Queue,logging

logger = logging.getLogger("cf")

CONN_TIMEOUT = 15

class RedisClient(asyncore.dispatcher):
    redis_reply = ''# redis reply, bulk strings
    recv_size = 0
    wflag = False
    rflag = False # prevent being pushed into poll readable list before invoke connect() 
    queue = Queue.Queue()
    buf = ""
    last_try_conn = 0

    def __init__(self, host, port, id, name):
        asyncore.dispatcher.__init__(self)
        self.host = host
        self.port = port
        self.id = id
        self.name = name
        #self.set_reuse_addr()

    def add_cmd(self):
        try:
            self.queue.put_nowait(time.time()) #simply put an item to notify redisclient 
            #print "add to queue {}".format(self.port)
        except Queue.Full:
            print u"Error: add_cmd failed, queue is FULL !!!"

    def set_callback(self, cb):
        self.cb = cb

    def asyn_info(self):
        self.cmd = "*2\r\n$4\r\ninfo\r\n$3\r\nall\r\n"
        
    def set_readable(self, flag = True):
        self.rflag = flag

    def set_writable(self, flag = True):
        self.wflag = flag

    def try_connect(self):
        if not(self.is_connecting() or self.is_connected()):
            if time.time() - self.last_try_conn > CONN_TIMEOUT:
                print "{0}: connecting {1}:{2}".format(time.time(), self.host, self.port)
                self.last_try_conn = time.time()
                self.connect()


    # inherted fucntions from asyncore.dispatcher
    def connect(self):
        assert(not(self.is_connecting() or self.is_connected()))
        asyncore.dispatcher.connect(self, (self.host, self.port))
        self.set_readable()
        self.set_writable()

    def handle_connect(self):
        print u"{0}: connected to {1}:{2}".format(time.time(), self.host, self.port)

    def handle_read(self):
        #print 'handle_read...{0}'.format(self.port)
        recv = self.recv(256) 
        self.recv_size += len(recv)
        self.redis_reply += recv
        last = rp.check_bulk_strings(self.redis_reply)
        if (last != -1):
            try:
                logger.debug("{0}: redis reply from {1}:{2} , data_size = {3}".format(time.time(), self.host, self.port, len(self.redis_reply)))
                self.cb.on_info(self.id, self.name, rp.remove_bulk_string_format(self.redis_reply[:last]))
                self.redis_reply = self.redis_reply[last:]
                if (len(self.redis_reply) > 0):
                    logger.warn("{0} remain {1}".format(self.port, len(self.redis_reply)))
            except Exception as e:
                print e
                logger.error(e)

        #else:
        #    print "{0} check bulk_strings failed! recv_size = {1}, data_size = {2}".format(self.port, len(recv), len(self.redis_reply))

    def handle_write(self):
        #print 'handle_write...'
        if len(self.buf) > 0:
            sent = self.send(self.buf)
            self.buf=self.buf[sent:]

    # readable, writeable can also treate as "local" poll timeout event handler 
    # of this redisclient.
    def readable(self):
        #print "{0}: readable".format(time.time())
        return self.rflag
    
    def empty_queue(self):
        print "{0}: RedisClient::empty_queue".format(time.time())
        while not self.queue.empty():
            self.queue.get_nowait()

    # This function also treat as poll timeout event.
    def writable(self):
        self.try_connect() 

        if self.is_connecting():
            print "{0}:rediclient is connecting to:{1}:{2}".format(time.time(), self.host, self.port)
            return True
        if self.is_connected():
            if len(self.buf) == 0:
                try:
                    t = self.queue.get_nowait()
                    self.buf = self.cmd
                    #print "self.buf = self.cmd {}".format(self.port)
                    return True
                except Queue.Empty:
                    return False
            elif len(self.buf) > 0:
                print "{0}:need to send remaining request data".format(time.time())
                return True
        else:
            return False

    def is_connected(self):
        return self.connected

    def is_connecting(self):
        return self.connecting


    def handle_close(self):
        print "{0}: handle close {1}:{2}".format(time.time(), self.host, self.port)
        #traceback.print_stack()
        self.set_readable(False)
        self.set_writable(False)
        self.close() # remove old socket from asyncore pollable channel
        # add new socket to poolable channel
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

'''
--------------- Test -----------------

r = RedisClient('127.0.0.1', 52021)
r.asyn_info()
collector = []
collector.append(r)

def timer_check_connection(collector):
    #print '{0}: check connection... '.format(time.time())
    for p in collector:
        if not (p.is_connected() or p.is_connecting()):
            print "{0}: connecting {1}:{2}".format(time.time(), p.host, p.port)
            p.connect()
    threading.Timer(5, timer_check_connection, args=[collector]).start()

def timer_add_cmd(collector):
    #print '{0}: add_cmd... '.format(time.time())
    for p in collector:
        if p.is_connected():
            print "{0}: add_cmd {1}:{2}".format(time.time(), p.host, p.port)
            p.add_cmd()
    threading.Timer(3, timer_add_cmd, args=[collector]).start()


threading.Timer(5, timer_check_connection, args=[collector]).start()
threading.Timer(5, timer_add_cmd, args=[collector]).start()

asyncore.loop(2)
''' 

