# -*- coding: utf-8 -*-
# Name:         env_utils.py
# Description:
# Author:       wangge
# Date:         2019-04-04

import os


def getenv(name: str, default=None):
    """
    获取环境变量的值

    :param name: 环境变量名
    :param default: 如果没有这个环境变量默认拿的值
    :return: 环境变量的值
    """
    return os.getenv(name, default)


def setenv(name: str, value: str):
    """
    临时设置环境变量

    :param name: 环境变量名
    :param value: 环境变量的值
    :return: 返回环境变量的值
    """
    return os.environ.setdefault(name, value)
