#-*-coding=utf-8-*-

HEAD_SIZE = 5 # 前五个字节指名后面的数据包大小 
HEAD_PAD = '&'# 用于填充前5个字节中的“字位置”
MAX_SEND_SIZE = 4096 - HEAD_SIZE

def pack(data):
    dataSize = len(data)
    if (dataSize > MAX_SEND_SIZE):
        raise RuntimeError(u'发送数据超过最大值')

    head = string.ljust(str(dataSize), HEAD_SIZE, HEAD_PAD)
    packet = head + data
    return packet

# Unpack a complete packet from received buffer.
def unpack(buffer):
    if len(buffer) > HEAD_SIZE:
        bufSize = int(buffer[:HEAD_SIZE])
        if len(buffer[HEAD_SIZE:]) >= msgsize:
            data = buffer[HEAD_SIZE: HEAD_SIZE + msgsize]
            return data

    return None
