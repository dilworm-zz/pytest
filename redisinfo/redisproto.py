def check_bulk_strings(data):
        ib = data.find("$")
        irn = data.find("\r\n")
        if ((ib != 0) or
            (irn == -1) or
            (not data.endswith("\r\n"))):
                return False

        len_str = data[ib+1:irn]
        if not len_str.isdigit():
            return False

        expect_cnt = int(len_str)
        if len(data[irn+2:]) != expect_cnt + len("\r\n"):
            return False

        return True

def remove_bulk_string_format(data):
    if not check_bulk_strings(data):
        return False, "not bulk strings"

    begin = data.find("\r\n")
    end = data.rfind("\r\n")
    return data[begin:end]
