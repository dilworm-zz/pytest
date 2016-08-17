#-*-coding=utf-8-*-
import cmddispatch
import logging
import packetparser as pp

logger = logging.getLogger("cf")


# 管理客户端连接
class ClientManager:
    def __init__(self):
        self.agents = {}
        self.controllers = {}
        pass

    def AddClient(self, type, name, conn):
        if type == "agent":
            assert(name not in self.agents)
            self.agents[name] = conn
        elif type == "controller":
            assert(name not in self.controllers)
            self.controllers[name] = conn

    def RemoveClient(self, type, name):
        if type == "agent":
            assert(name in self.agents)
            del self.agents[name]
        elif type == "controller":
            assert(name in self.controllers)
            del self.controllers[name]

    def GetAgents(self):
        return self.agents

    def GetControlers(self):
        return self.controlers

class DeployServerCmdHandler(cmddispatch.BaseCommandHandler):
    def __init__(self, owner):
        cmddispatch.BaseCommandHandler.__init__(self, owner)
        self.clientManager = ClientManager()

    def _do_pong(self, peer, data):
        logger.debug("recv pong")

    def _do_login(self, peer, data):
        type, name = date["type"], data["name"]
        self.clientManager.AddClient(type, name)

        loggger.debug(u"收到 {0} 注册: {1}".format(type, name))

    # 转发controler的命令到所有agent
    def _do_agent_cmd(self, peer, data):
        logger.debug(u"_do_agent_cmd")
        for n, p in self.clientManager.GetAgents():
            print "send agent cmd"
            p.send(data)

    # agent 执行命令后的返回
    def _do_agent_response(self, peer, data):
        logger.debug(u"_do_agent_response")
        for n, p in self.clientManager.controllers():
            p.send(data)
    
