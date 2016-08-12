#-*-coding=utf-8-*-
import cmddispatch

class DeployServerCmdHandler(cmddispatch.BaseCommandHandler):
    def _do_pong(self, peer, data):
        logger.debug("recv pong")




