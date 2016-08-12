#-*-coding=utf-8-*-
import cmddispatch

# AgentCmdHandle 的命令处理函数的命名格式为
# _do_XXX(self, param)

class AgentCmdHandler(cmddispatch.BaseCommandHandler)
    def _do_ping(self):
        self.owner.send("pong", {"var":"pong from agent"})
