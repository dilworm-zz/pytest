# -*- coding=utf8 -*-
import sys,urllib,urllib2,hashlib,base64,time,binascii

def gen_sign(params, secret):
    canstring = ''
    #先将参数以其参数名的字典序升序进行排序
    params = sorted(params.items(), key=lambda item:item[0])
    #遍历排序后的参数数组中的每一个key/value对
    for k,v in params:
        if( k != 'sign' and k != 'key' and v != '') :
         canstring +=  k + '=' + v + '&'
    canstring = canstring[:-1]
    canstring += secret
    md5 = hashlib.md5(canstring).digest()
    return base64.b64encode(md5)


path = "https://free-api.heweather.com/s6/weather/forecast?"

key = "4f6ef0eb7a0e4929a1576d8d8a009ebf"
params = {
    "location": "CN101010100",
    "username": "HE1805061213491924",
    "t": str(int(time.time())),
}
params["sign"] = gen_sign(params, key)
params = sorted(params.items(), key=lambda item:item[0])
uri = path + urllib.urlencode(params)
print uri

req = urllib2.Request(uri)
res = urllib2.urlopen(req)
print res.read()

