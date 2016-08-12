#-*-coding=utf-8-*-
import string
import json

HEAD_SIZE = 5 # 前五个字节指名后面的数据包大小 
HEAD_PAD = '0'# 用于填充前5个字节中的“空位置”
MAX_SEND_SIZE = 4096 - HEAD_SIZE

def pack(data):
    dataSize = len(data)
    if (dataSize > MAX_SEND_SIZE):
        raise RuntimeError(u'发送数据超过最大值')

    head = string.rjust(str(dataSize), HEAD_SIZE, HEAD_PAD)
    packet = head + data
    return packet

# Unpack a complete packet from received buffer.
def unpack(buffer):
    if len(buffer) > HEAD_SIZE:
        bufSize = int(buffer[:HEAD_SIZE])
        if len(buffer[HEAD_SIZE:]) >= bufSize:
            data = buffer[HEAD_SIZE: HEAD_SIZE + bufSize]
            return data

    return None


def request(cmd, param):
    try:
        d = json.dumps({"cmd":cmd, "param":param})
        return d
    except Exception as e:
        print e
        logger.error(u"编码数据失败 cmd = {}".format(cmd))
        return None

def response(data):
    try:
        l = json.loads(data)
        if not isinstance(l, "dict"):
            raise RuntimeError("json.loads return type is not dict")
        if not hasattr(l, "cmd"):
            logger.error(u"解码数据失败，找不到cmd属性")
            return None
        if not isinstance(l["cmd"], str):
            logger.error(u"解码数据失败，cmd属性值类型不为str")
            return None

        if not hasattr(l, "param"):
            logger.error(u"解码数据失败，找不到param属性")
            return None
        if not isinstance(l["param"], dict):
            logger.error(u"解码数据失败，param属性不为dict")
            return None

        return l["cmd"], l["param"]

    except Exception as e:
        print e
        logger.error(u"解码数据出现异常", )
        return None
        

