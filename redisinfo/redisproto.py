#-*-coding=utf-8-*-
def check_bulk_strings(data):
    ib = data.find("$")
    irn = data.find("\r\n")
    if ((ib != 0) or
        (irn == -1) or
        (not data.endswith("\r\n"))):
            return -1

    len_str = data[ib+1:irn] # 后续长度
    if not len_str.isdigit():
        return -1

    expect_cnt = int(len_str) + len("\r\n") # 最后的两个字符 "\r\n"
    if len(data[irn+2:]) < expect_cnt:
        return -1

    return irn+2+expect_cnt

def remove_bulk_string_format(data):
    if not check_bulk_strings(data):
        return False, "not bulk strings"

    begin = data.find("\r\n")
    end = data.rfind("\r\n")
    return data[begin:end]
