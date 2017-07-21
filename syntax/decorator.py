# -*-coding=utf8-*-
# decorator 是语法糖， 是一个函数，以原函数为参数，返回一个被wrap 后的函数，并替换原函数
#  
#  语法：
#
#   1. 装饰器不带参数 
#   @dec2
#   @dec1
#   def func(arg1, arg2, ...):
#       pass
#   This is equivalent to:
#   def func(arg1, arg2, ...):
#       pass
#   func = dec2(dec1(func))
#   
#   2. 装饰器带参数 
#   @decomaker(argA, argB, ...)
#   def func(arg1, arg2, ...):
#       pass
#   This is equivalent to:
#   func = decomaker(argA, argB, ...)(func)
#

def origin():
    print ("origin") 


def origin1(a):
    print ("origin1") 

# 1. 装饰无参数函数
def deco(func):
    def wrapped():
        print("deco before wrap");
        func()
        print("deco after wrap")

    return wrapped


@deco
def origin():
    print ("origin") 
    
#origin()


# 2. 装饰任意参数函数
def deco_nargs(func):
    def wrapped(*args, **kwargs):
        print("deco_nargs before wrap");
        func(*args, **kwargs)
        print("deco_nargs  after wrap")

    return wrapped
        

@deco_nargs
def origin():
    print ("origin") 

@deco_nargs
def origin1(a):
    print ("origin1") 


origin()
origin1(1)

# 3. 装饰器自身带参数 
def deco_with_args(name):
    def _deco_with_args(func):
        print("_deco_with_args -- %s"%(name))
        def wrap(*args, **kwargs):
            print("deco_nargs before wrap %s"%(name));
            func(*args, **kwargs)
            print("deco_nargs  after wrap %s"%(name))

        return wrap
    return _deco_with_args

@deco_with_args("xiaomin")
def origin():
    print ("origin") 


@deco_with_args("xiaomin1")
def origin1(a):
    print ("origin1") 

origin()
origin1(1)

