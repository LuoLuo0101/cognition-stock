# -*- coding: utf-8 -*-
# Name:         base_enum.py
# Description:
# Author:       wangge
# Date:         2019-04-04

from enum import Enum


class BaseConstEnum(Enum):

    @classmethod
    def choice_dict(cls):
        # to get value:key dict
        return {v.value: k for k, v in cls.__dict__.get("_member_map_", {}).items()}

    @classmethod
    def values(cls):
        return list(cls.choice_dict().keys())

    @classmethod
    def values_and_empty(cls):
        return cls.values() + [""]

    @classmethod
    def default(cls):
        pass

    @classmethod
    def choices(cls) -> tuple:
        # to get value:key in tuple form
        return tuple(cls.choice_dict().items())

    @classmethod
    def desc_by_value(cls, value, default=None):
        # to get key by given value
        return cls.choice_dict().get(value, default)


    @classmethod
    def value_by_key(cls, key, default=None):
        key = getattr(cls, key, default)
        return key.value if key else default


if __name__ == "__main__":
    pass
