import re
import math


def judge_ip_by_re(ip_addr: str):
    """
    判断当前IP是否IP地址
    """
    # 第一个数字不为0
    # comp = re.compile(r'^((2(5[0-5]|[0-4]\d))|1\d{2}|[1-9]\d|[1-9])(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}$')
    # 第一个数字可以为0
    comp = re.compile(r'^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}$')
    return bool(comp.match(ip_addr))


def judge_ip_info(start_ip: str, end_ip: str):
    """
    判断结束IP大于等于开始IP
    """
    new_start_ip = ".".join([x.zfill(3) for x in start_ip.split(".")])
    new_end_ip = ".".join([x.zfill(3) for x in end_ip.split(".")])
    return new_end_ip >= new_start_ip


def get_ip_list_by_ip_range(ip_range: list):
    """
    通过给定的IP范围，将之转化成IP资源列表

    ip_range:
        [{"start_ip": "192.168.10.1", "end_ip": "192.168.10.9"},{"start_ip": "192.168.10.1", "end_ip": "192.168.10.9"}]
    """
    ip_dict = {}
    for ip_info in ip_range:
        start_ip = ip_info.get("start_ip", "")
        end_ip = ip_info.get("end_ip", "")
        if not judge_ip_info(start_ip, end_ip):
            continue
        sp1, sp2, sp3, sp4 = [int(x) for x in start_ip.split(".")]
        ep1, ep2, ep3, ep4 = [int(x) for x in end_ip.split(".")]
        for _1 in range(sp1, ep1 + 1):
            for _2 in range(sp2, ep2 + 1):
                for _3 in range(sp3, ep3 + 1):
                    for _4 in range(sp4, ep4 + 1):
                        ip_dict["{}.{}.{}.{}".format(_1, _2, _3, _4)] = 1
    return list(ip_dict.keys())


def mask_num_to_mask(mask_num):
    """
    掩码数字转掩码
    """
    bin_arr = ['0' for i in range(32)]
    for i in range(mask_num):
        bin_arr[i] = '1'
    tmpmask = [''.join(bin_arr[i * 8:i * 8 + 8]) for i in range(4)]
    tmpmask = [str(int(tmpstr, 2)) for tmpstr in tmpmask]
    return '.'.join(tmpmask)


def mask_to_mask_num(mask):
    """
    掩码转掩码数字
    """
    mask = mask.split(".")
    length = 0
    for x in range(4):
        mask[x] = int(mask[x])
        if (255 & mask[x]) == 255:
            length += 8
        else:
            length += (8-math.log(256-mask[x], 2))
    return int(length)


if __name__ == '__main__':
    # ip_list = get_ip_list_by_ip_range(
    #     ip_range=[{"start_ip": "192.168.10.1", "end_ip": "192.168.10.9"},{"start_ip": "192.168.10.1", "end_ip": "192.168.10.9"}]
    # )
    # print(ip_list)

    # print(judge_ip_by_re("0.1.1.1"))
    # print(judge_ip_by_re("127.0.0.1"))
    # print(judge_ip_by_re("192.168.0.1"))
    # print(judge_ip_by_re("255.255.255.0"))
    # print(judge_ip_by_re("256.255.255.0"))
    # print(judge_ip_by_re("255.255.255.256"))
    print(mask_num_to_mask(24))
    print(mask_num_to_mask(25))
    print(mask_num_to_mask(29))
    print(mask_to_mask_num("255.255.255.0"))
    print(mask_to_mask_num("255.255.255.128"))
    print(mask_to_mask_num("255.255.255.248"))
