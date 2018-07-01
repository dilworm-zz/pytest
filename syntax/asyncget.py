#-*-coding=utf8-*-
import threading
import asyncio

@asyncio.coroutine
def hello():
    print("1", threading.currentThread())
    yield from asyncio.sleep(1)
    print("2", threading.currentThread())

loop = asyncio.get_event_loop()

loop.run_until_complete(asyncio.wait([hello(), hello()]))


