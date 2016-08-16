#-*-coding=utf-8-*-

import threading
from cmddispatch import BaseCommandDispatcher
from TcpServer import TcpServer

def logic_thread_handler(dispatcher):
    dispatcher.run()

def network_thread_handler(server):
    server.run_forever()

class BaseAppServer:
    def __init__(self, host, port, CmdHandlerClass):
        self.host = host
        self.port = port
        self.dispatcher = BaseCommandDispatcher(CmdHandlerClass)
        self.tcpServer = TcpServer(('127.0.0.1', 9999), self.dispatcher)

    def run_forever(self):
        cmdDispatchThread = threading.Thread(target=logic_thread_handler, 
                name="CmdDispatch", args=[self.dispatcher])
        tcpServerThread = threading.Thread(target=network_thread_handler, 
                name="Network", args=[self.tcpServer])

        cmdDispatchThread.start()
        tcpServerThread.start()
        cmdDispatchThread.join()
        tcpServerThread.join()


