
mac_chrs = [
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "a", "b", "c", "d", "e", "f",
    "A", "B", "C", "D", "E", "F",
]


def get_mac_addr(mac_address, concat_str="-", is_upper=True, part=6):
    """
    获取Mac地址（默认6段式大写）
    """
    mac_address = mac_address.replace("-", "").replace(".", "").replace(":", "").replace(" ", "").strip()
    if len(mac_address) != 12:
        return ""
    if not all([x in mac_chrs for x in mac_address]):
        return ""
    step = 12 // part
    new_mac = concat_str.join([mac_address[x: x + step] for x in range(0, len(mac_address), step)])
    if is_upper:
        return new_mac.upper()
    else:
        return new_mac.lower()


if __name__ == '__main__':
    print("6段式小写：", get_mac_addr("12-34-56-78-90-AB", concat_str=".", is_upper=False, part=6))
    print("6段式大写：", get_mac_addr("12-34-56-78-90-AB", concat_str=".", is_upper=True, part=6))
    print("3段式小写：", get_mac_addr("12-34-56-78-90-AB", concat_str=".", is_upper=False, part=3))
    print("3段式大写：", get_mac_addr("12-34-56-78-90-AB", concat_str=".", is_upper=True, part=3))

    print("6段式小写：", get_mac_addr("1234.5678.90AB", concat_str="-", is_upper=False, part=6))
    print("6段式大写：", get_mac_addr("1234.5678.90AB", concat_str="-", is_upper=True, part=6))
    print("3段式小写：", get_mac_addr("1234.5678.90AB", concat_str="-", is_upper=False, part=3))
    print("3段式大写：", get_mac_addr("1234.5678.90AB", concat_str="-", is_upper=True, part=3))
