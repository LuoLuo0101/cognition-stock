import binascii


def str_to_hex(string):
    str_bin = string.encode("utf-8")
    return binascii.hexlify(str_bin).decode("utf-8")


def hex_to_str(hex_str):
    if hex_str.startswith("0x") or hex_str.startswith("0X"):
        hex_str = hex_str[2:]
        _hex = hex_str.encode("utf-8")
        str_bin = binascii.unhexlify(_hex)
        return str_bin.decode("utf-8")
    else:
        return hex_str


# def has_undefined_str(string):
#     chinese_pat = re.compile(r'^[a-zA-Z0-9\u4e00-\u9fa5]+$')
#     return all()


if __name__ == '__main__':
    s = "0xe4b8ade69687616263313233"
    # s2 = b"0E\x02\x01\x01\x04\tleoxiong1\xa75\x02\x01\x00\x02\x01\x00\x02\x01\x000*0\x10\x06\x08+\x06\x01\x02\x01\x01\x03\x00C\x04\x01\xa0m\xd80\x16\x06\n+\x06\x01\x06\x03\x01\x01\x04\x01\x00\x06\x08+\x06\x01\x02\x01\x11\x00\x02"
    d =hex_to_str(s).strip()
    print(d)

    # s2_str = s2.decode("utf-8", errors="ignore")
    # print(s2_str)
