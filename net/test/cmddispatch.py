#-*-coding=utf-8-*-
import logging 
import Queue
import time
import threading
import json
import packetparser as pp 
logger = logging.getLogger("cf")

# Generally, you should driverd from BaseCommandHandler and impletement 
# self-define cmd hanndler method
class BaseCommandHandler:
    def __init__(self, owner):
        self.owner = owner

    def _do_ping(self, conn, data={}):
        logger.debug("_do_ping")
        req = pp.request("pong", {})
        conn.send(req)

    def _do_pong(self, conn, data={}):
        logger.debug("_do_pong")

    def _do_download(self, conn, data={}):
        logger.debug("_do_download")
        pass

    def _do_update(self, conn, data={}):
        logger.debug(u"receive update command.")

    def _do_print(self, conn, data={}):
        if data is not None:
            print data

class BaseCommandDispatcher:
    def __init__(self, HandlerClass):
        if HandlerClass is not None:
            self.handler = HandlerClass(self)
        else:
            self.handler = BaseCommandHandler(self)

        self.peer = None
        self.queue = Queue.Queue()
        self.running = False

    def SetConnectCallback(self, cb):
        self.connectCallback = cb

    def run(self):
        if self.running:
            return

        self.running = True
        while self.running:
            try:
                item = self.queue.get()
                peer, data = item[0],item[1]
                pair = pp.response(data)
                #print pair
                if (pair is not None):
                    cmd, param = pair
                    if hasattr(self.handler, "_do_" + cmd):
                        getattr(self.handler, "_do_" + cmd)(peer, param)
                    else:
                        logger.error(u"找不到 '{}'的处理函数".format(cmd))
            except Exception as e:
                import traceback as tb
                tb.print_stack()
                print e
                logger.error("handle command error:{}".format(e))

    def stop(self):
        self.running = False

    def send(self, conn, cmd, param={}):
        try:
            assert(isinstance(cmd, str))
            d = json.dumps({"cmd":cmd, "param":param})
            conn.send(d)
        except Exception as e:
            print e
        
    # Network thread will call these methodes.
    def OnReceiveData(self, conn, data=None):
        #logger.debug("OnReceiveData")
        try:
            self.queue.put_nowait((conn, data, time.time()))
        except Queue.Full:
            logger.error(u"Queue is Full")

    def OnConnectEstablished(self, conn):
        logger.debug("OnConnectEstablished")
        if self.connectCallback is not None:
            self.connectCallback(conn)

    def OnConnectClose(self, conn):
        logger.debug(u"dispatcher OnConnectClose")
        self.handler.OnConnectClose(conn)

