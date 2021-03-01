import hashlib
import pickle
from collections import defaultdict
from copy import deepcopy
from datetime import datetime, timedelta
from typing import Dict, List

import jwt
from sanic import Sanic
from sanic.request import Request
import asyncio
from asyncio import Task
import re


def md5(content: str) -> str:
    return hashlib.md5(content.encode()).hexdigest()


def sha1(content: str) -> str:
    return hashlib.sha1(content.encode()).hexdigest()


def sha256(context: str) -> str:
    return hashlib.sha256(context.encode()).hexdigest()


def get_client_ip(request: Request) -> str:
    if request.remote_addr:
        return request.remote_addr
    return request.ip


def get_current_task() -> Task:
    current_task: Task = asyncio.current_task()
    return current_task


class classproperty(object):
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, obj, cls):
        return self.fget(cls)


def generate_token(payload: Dict, secret: str, ttl: int) -> str:
    """
    生成Token
    """
    # 必须用UTC的，会生成时间戳，后面我们需要用时间戳对其相减
    iat: datetime = datetime.utcnow()
    exp: datetime = iat + timedelta(seconds=ttl)  # 到期时间
    payload.update({"iat": iat, "exp": exp})
    return jwt.encode(payload, secret, algorithm="HS256").decode()


def decode_token(token: str, secret: str) -> Dict:
    """
    解码Token
    """
    return jwt.decode(token, secret)


def regex_match(origin: str, white_list: List):
    """
    正则匹配
    """
    for pattern in white_list:
        if re.match(pattern, origin):
            return True
    return False


def get_cache_key(key_list):
    return ":".join([str(x) for x in key_list])


async def get_cache_exist(cache, key: str):
    """
    获取键对应的缓存是否存在

    -2 or None: 键不存在
    -1 or False: 过期时间不存在

    :param cache: 缓存client
    :param key: 键
    :return: 返回这个键对应的缓存是否存在
    """
    ret = await cache.ttl(key)
    return ret not in [-2, None]


async def get_data_from_cache(cache, key: str):
    """
    从缓存中拿数据

    :param cache: 缓存client
    :param key: 键
    :return: 返回从缓存中拿到的数据
    """
    return await cache.get(key)


async def set_data_to_cache(cache, key: str, value, expire=25 * 60 * 60):
    """
    设置数据到内存中

    :param cache: 缓存client
    :param key: Key
    :param value: 数据
    :param expire: 过期时间
    :return:
    """
    return await cache.set(key, value, expire=expire)


async def get_data_from_db_or_cache(app: Sanic, key: str, get_data_callback, force: bool = False,
                                    expire: int = 25 * 60 * 60):
    """
    从数据库或者缓存中获取数据
    """
    # 如果强制刷新或者缓存不存在，那么重新获取一份数据吧
    if force or (not await get_cache_exist(cache=app.redis, key=key)):
        # 从数据库中查询数据
        data = get_data_callback()

        bys: bytes = pickle.dumps(data)
        # 存一份字节数据到缓存中
        await set_data_to_cache(cache=app.redis, key=key, value=bys, expire=expire)
    else:
        # 从缓存中拿数据
        bys: bytes = await get_data_from_cache(cache=app.redis_bytes, key=key)
        data: List = pickle.loads(bys)
    return data


def get_data_with_key(data_list: List, key_name="parent_id"):
    """
    将数据源变成 parent_id->[data, data] 格式
    """
    data = defaultdict(list)
    for x in data_list:
        data[x.get(key_name)].append(x)
    return data


def concat_data_with_data_relate(root_list, data_relate: Dict):
    """
    递归拼接数据
    """
    ret_data = []
    for root in root_list:
        root_id = root.get("id")
        new_root_list = data_relate.get(root_id, [])
        new_data = []
        if new_root_list:
            new_data = concat_data_with_data_relate(root_list=new_root_list, data_relate=data_relate)
        new_root = deepcopy(root)
        new_root["children"] = new_data
        ret_data.append(new_root)
    return ret_data
