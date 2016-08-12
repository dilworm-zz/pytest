#-*-coding=utf-8-*-
import threading
import asyncore
import logging
from logger import initlogger
from TcpClient import TcpClient
from cmddispatch import *

from AgentCmdHandler import AgentCmdHandler 

def network_thread_handler(tcpClient): 
    tcpClient.start()

def logic_thread_handler(dispatcher):
    dispatcher.run()

class Agent:
    def __init__(self, host, port, CmdDispatcherClass):
        self.dispatcher = CmdDispatcherClass(AgentCmdHandler)
        self.tcpClient = TcpClient((host, port), self.dispatcher)

    def start(self):
        tcpclientThread = threading.Thread(target=network_thread_handler, 
                name="Network", args=[self.tcpClient])

        cmdDispatchThread = threading.Thread(target=logic_thread_handler, 
                name="CmdDispatch", args=[self.dispatcher])

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

