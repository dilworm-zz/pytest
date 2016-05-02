import redisproto as rp

''''
s = "$4\r\n1234\r\n"
ck = rp.check_bulk_strings(s)
print s, ck

s = "$3\r\n1234\r\n"
ck = rp.check_bulk_strings(s)
print s, ck

s = "$3\r\n1234\n"
ck = rp.check_bulk_strings(s)
print s, ck
''' 

s = "$4\r\n1234\r\n"
s = "$3\r\n1234\n"
print rp.remove_bulk_string_format(s)

