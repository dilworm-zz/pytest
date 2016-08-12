#-*-coding=utf-8-*-
import logging
import Queue
import time
import threading
import json

logger = logging.getLogger("cf")

# Generally, you should driverd from BaseCommandHandler and impletement 
# self-define cmd hanndler method
class BaseCommandHandler:
    def __init__(self, owner):
        self.owner = owner
        self.send = self.owner

    def _do_ping(self, conn, data=None):
        logger.debug("_do_ping")
        self.owner.send("pong")

    def _do_pong(self, conn, data=None):
        logger.debug("_do_pong")

    def _do_download(self, conn, data=None):
        logger.debug("_do_download")
        pass

    def _do_update(self, conn, data=None):
        logger.debug(u"receive update command.")

    def _do_print(self, conn, data=None):
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

    def run(self):
        if self.running:
            return

        self.running = True
        while self.running:
            try:
                item = self.queue.get()
                func = None
                peer, data = item[0],item[1]
                pair = pp.response(data)
                if (pair is not None):
                    cmd, param = pair
                    if self.handler.hasattr("_do_" + cmd):
                        getattr(self.handler, "_do_" + cmd)(peer, param)
                    else:
                        logger.error(u"找不到 '{}'的处理函数".format(cmd))
            except:
                logger.error("handle command error")

    def stop(self):
        self.running = False

    def send(self, peer, cmd, param={}):
        try:
            assert(isinstance(cmd, str))
            d = json.dumps({"cmd":cmd, "param":param})
            peer.send(d)
        except Exception as e:
            print e
        
    # Network thread will call this method.
    def OnReceiveData(self, peer, data=None):
        logger.debug("OnReceiveData")
        try:
            self.queue.put_nowait((peer, data, time.time()))
        except Queue.Full:
            logger.error(u"Queue is Full")

