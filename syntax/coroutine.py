#-*-coding=utf8-*-

def consumer():
    r = None
    while True:
        n = yield r 
        print("consume ", n)
        r = n*n

def productor(c):
    r = c.send(None)
    print(r)
    i = 0 
    while i < 5:
        r = c.send(i)
        i = i + 1
        print("pro", r)


c =  consumer()
productor(c)


