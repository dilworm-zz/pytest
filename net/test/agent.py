#-*-coding=utf-8-*-
import threading
import asyncore
import logging
from logger import initlogger
from TcpClient import TcpClient
from cmddispatch import *

def network_thread_handler(svrSocket):
    svrSocket.start()

def cmd_thread_handler(dispatcher, svrSocket):
    dispatcher.run(svrSocket)

class Agent:
    def __init__(self, host, port, CmdDispatcherClass):
        self.dispatcher = CmdDispatcherClass()
        self.peer = TcpClient((host, port), self.dispatcher)

    def start(self):
        tcpclientThread = threading.Thread(target=network_thread_handler, 
                name="Network", args=[self.peer])

        cmdDispatchThread = threading.Thread(target=cmd_thread_handler, 
                name="CmdDispatch", args=[self.dispatcher, self.peer])

        tcpclientThread.start()
        cmdDispatchThread.start()
        tcpclientThread.join()
        cmdDispatchThread.join()

# TODO: Run agent as a deamon service.
if __name__ == "__main__":
    import sys
    sys.path.append("..")

    initlogger("./log/client")
    logger = logging.getLogger("cf")

    agent = Agent("127.0.0.1", 9999, BaseCommandDispatcher)
    agent.start()

    logger.info("agent exit.")

