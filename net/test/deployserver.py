#-*-coding=utf-8-*-
import logging
import sys
sys.path.append("..")


if __name__ == "__main__":
    import logger
    from logger import initlogger
    from BaseAppServer import *
    from DeployServerCmdHandler import DeployServerCmdHandler

    initlogger("./log/deployserver")
    logger = logging.getLogger("cf")
    logger.info("EasyDeploy started")

    deployServer = BaseAppServer('127.0.0.1', 9999, DeployServerCmdHandler)
    deployServer.run_forever()
    

    
