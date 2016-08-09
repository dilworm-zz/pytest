#-*-coding=utf-8-*-
import logging
import Queue
import time
import threading

logger = logging.getLogger("cf")

class BaseCommandDispatcher:
    def __init__(self, map=None):
        if map is None:
            self._cmd_map = cmd_map
        else:
            self._cmd_map = map

        self.peer = None
        self.queue = Queue.Queue()
        self.running = False

    def run(self, peer):
        if self.running:
            return

        self.peer = peer
        self.running = True
        while self.running:
            try:
                item = self.queue.get()
                func = None
                try:
                    func = self._cmd_map[item[0]]
                except KeyError:
                    logger.error(u"command '{}'is not exists.".format(item[0]))
                func(self, item[0])
            except:
                logger.error("handle command error")

    def stop(self):
        self.running = False

    # Network thread will call this method.
    def OnReceiveData(self, data=None):
        logger.debug("OnReceiveCmd")
        try:
            self.queue.put_nowait((data, time.time()))
        except Queue.Full:
            logger.error(u"Queue is Full")
            pass

    def _do_ping(self, data=None):
        logger.debug("_do_ping")
        self.peer.send("pong")

    def _do_download(self, data=None):
        logger.debug("_do_download")
        pass

    def _do_update(self, data=None):
        logger.debug(u"receive update command.")

    def _do_print(self, data=None):
        if data is not None:
            print data


#命令处理映射，在这里添加新的命令映射
cmd_map = { "ping"      : BaseCommandDispatcher._do_ping,
            "download"  : BaseCommandDispatcher._do_download,
            "update"    : BaseCommandDispatcher._do_update,
            "print"     : BaseCommandDispatcher._do_print,
          }
