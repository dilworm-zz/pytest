#-*-coding=utf-8-*-
from ftplib import FTP

ftp = FTP("127.0.0.1", user="ftpuser", passwd="123")
ftp.retrlines("LIST -al")
f = open("lua.tar.gz", "wb")
ftp.h



