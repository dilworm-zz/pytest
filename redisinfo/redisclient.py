#-*-coding=utf8-*-
import asyncore, socket, time
import redisproto as rp
import threading
import traceback
import Queue

CONN_TIMEOUT = 15

class RedisClient(asyncore.dispatcher):
    redis_reply = ''# redis reply, bulk strings
    recv_size = 0
    wflag = False
    rflag = False # prevent pushed to poll readable before invoke connect() 
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
        except Queue.Full:
            print u"Error: add_cmd failed, queue is full."

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
        #print 'handle_read...'
        recv = self.recv(1024)
        self.recv_size += len(recv)
        self.redis_reply += recv
        if rp.check_bulk_strings(self.redis_reply):
            try:
                print "{0}: redis_reply from {1}:{2}".format(time.time(), self.host, self.port)
                self.cb.on_info(self.id, self.name, rp.remove_bulk_string_format(self.redis_reply))
            except Exception as e:
                print e
            finally:
                self.redis_reply = ""

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

    def writable(self):
        self.try_connect() #treat as poll timeout event.

        if self.is_connecting():
            print "1 true"
            return True
        if self.is_connected():
            if len(self.buf) == 0:
                try:
                    t = self.queue.get_nowait()
                    self.buf = self.cmd
                    #print "2 true"
                    return True
                except Queue.Empty:
                    return False
            elif len(self.buf) > 0:
                print "3 true"
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

