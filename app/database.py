# -*- coding: utf-8 -*-

import functools
from datetime import datetime
from typing import Dict, List

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

import settings
from app.utils import get_current_task, classproperty


class MyBase(object):
    # sqlalchemy.exc.InvalidRequestError: Table 'brand' is already defined for this MetaData instance.
    # Specify 'extend_existing=True' to redefine options and columns on an existing Table object.
    __table_args__ = {'extend_existing': True}  # 防止重新创建表的时候报错

    def to_dict(self) -> Dict:
        fields: List = getattr(self, "__fields__", None)
        if not fields:
            fields = self.__table__.columns.keys()
        dict_vals = {}
        for key in fields:
            val = getattr(self, key)
            if isinstance(val, datetime):
                val = val.strftime("%Y-%m-%d %H:%M:%S")
            dict_vals[key] = val
        return dict_vals

    @classproperty
    def query(cls):
        return Session().query(cls)

    @classmethod
    def filter_by(cls, **kwargs):
        return Session().query(cls).filter_by(**kwargs)

    @classmethod
    def values(cls, *fields):
        query_fields = []
        for field_name in fields:
            if hasattr(cls, field_name):
                query_fields.append(getattr(cls, field_name))
        return Session().query(*query_fields)

    @classmethod
    def filter(cls, *criterion):
        return Session().query(cls).filter(*criterion)

    @classmethod
    def all(cls):
        return Session().query(cls).all()

    @classmethod
    def with_for_update(cls):
        return Session().query(cls).with_for_update()

    @classmethod
    def from_dict(cls, kwargs):
        return cls(**kwargs)

    @classmethod
    def get(cls, pk):
        return Session().query(cls).get(pk)

    @classmethod
    def batch_insert(cls, data_list: List, commit: bool=False):
        if not data_list:
            return []
        res = Session().execute(cls.__table__.insert(), data_list)
        if commit:
            Session().commit()
        return res

    def save(self, commit=False):
        Session().add(self)
        if commit:
            Session().commit()

    def fill_data(self, **kwargs):
        """
        填充表值
        """
        for arg_name, arg_val in kwargs.items():
            if hasattr(self, arg_name):
                setattr(self, arg_name, arg_val)

    def update(self, commit=False, **kwargs):
        self.fill_data(**kwargs)
        self.save(commit=commit)

    def delete(self):
        Session().delete(self)

    def commit(self):
        Session().commit()


Base = declarative_base(cls=MyBase)


engine: Engine = create_engine(
    settings.DB_SETTINGS["dsn"],
    pool_size=settings.DB_SETTINGS["pool_size"],
    pool_recycle=settings.DB_SETTINGS["pool_recycle"],
    max_overflow=settings.DB_SETTINGS["max_overflow"],
    pool_pre_ping=True,
    echo=False,  # 是否输出SQL日志
)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory, scopefunc=get_current_task)


def init_db() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def transactional(f):
    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        rv = await f(*args, **kwargs)
        Session().commit()
        return rv
    return wrapper


if __name__ == "__main__":
    from app.apps.users.models import *

    init_db()
