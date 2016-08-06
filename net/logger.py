#-*-coding=utf-8 -*-
import logging

def initlogger(logfile = "testlog"):
    FORMAT = "%(asctime)s [%(levelname)-.7s] %(message)s"
    logFormatter = logging.Formatter(FORMAT)
    g_cflogger = logging.getLogger("cf")
    g_cflogger.setLevel(logging.DEBUG)

    fileHandle = logging.FileHandler("{0}.log".format(logfile))
    fileHandle.setFormatter(logFormatter)
    fileHandle.setLevel(logging.INFO)
    g_cflogger.addHandler(fileHandle)

    consoleHandle = logging.StreamHandler()
    consoleHandle.setFormatter(logFormatter)
    consoleHandle.setLevel(logging.DEBUG)
    g_cflogger.addHandler(consoleHandle)

    g_cflogger.debug(u"初始化日志成功")

