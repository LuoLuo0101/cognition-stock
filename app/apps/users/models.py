# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy import Column, BigInteger, String, DateTime, SmallInteger

from app.database import Base


class User(Base):
    """用户表"""

    __tablename__ = "user"
    __fields__ = [
        "phone",
        "email",
        "nickname",
        "head_img_url",
        "create_time",
        "update_time",
    ]

    id = Column(BigInteger, primary_key=True)
    phone = Column(String(32), nullable=True, comment="手机号码")
    email = Column(String(255), nullable=True, comment="邮箱")
    password = Column(String(128), default="", comment="密码")
    nickname = Column(String(128), default="", comment="昵称")
    head_img_url = Column(String(1024), default="", comment="头像地址")

    TYPE_NORMAL = 0     # 普通用户
    TYPE_OTHER = 1      # 其它用户...
    TYPE_ADMIN = 9      # ADMIN用户
    type = Column(SmallInteger, default=TYPE_NORMAL, comment="用户类型")

    STATUS_FREEZE = 0   # 0: 冻结
    STATUS_ACTIVE = 1   # 1: 激活
    status = Column(SmallInteger, default=STATUS_ACTIVE, comment="账户状态")
    token = Column(String(256), default="", comment="用户登陆token")
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    @property
    def is_active(self):
        return self.status == self.STATUS_ACTIVE

    @property
    def is_admin(self):
        return self.type == self.TYPE_ADMIN


class Role(Base):
    """角色表"""

    __tablename__ = "role"
    __fields__ = [
        "id",
        "name",
        "description",
        "create_time",
        "update_time",
    ]

    id = Column(BigInteger, primary_key=True)
    name = Column(String(32), comment="角色名")
    description = Column(String(256), comment="描述")

    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Platform(Base):
    """
    平台表
    """
    __tablename__ = "platform"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(32), comment="平台名称")
    TYPE_WEB = 0    # 前台对外
    TYPE_ADMIN = 1  # 后台管理
    type = Column(SmallInteger, default=TYPE_WEB, comment="平台类型")
    key = Column(String(64), unique=True, comment="平台Key")  # 唯一
    description = Column(String(256), comment="描述")

    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Menu(Base):
    """
    菜单表
    1. 页面展示，参考这个角色的菜单
    """
    __tablename__ = "menu"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(32), comment="菜单名称")
    description = Column(String(256), comment="描述")
    key = Column(String(64), unique=True, comment="菜单Key")  # 唯一
    parent_id = Column(BigInteger, default=0, comment="父级菜单ID")
    platform_id = Column(BigInteger, default=0, comment="平台ID")
    menu_url = Column(String(1024), comment="菜单图片地址")

    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Permission(Base):
    """权限表"""

    __tablename__ = "permission"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(32), comment="权限名称")
    key = Column(String(64), unique=True, comment="权限Key")  # 唯一，对应端口

    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class UserRoleRelation(Base):
    """用户角色表"""

    __tablename__ = "user_role_relation"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, comment="用户id")
    role_id = Column(BigInteger, comment="角色id")

    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class RoleMenuRelation(Base):
    """角色菜单表"""

    __tablename__ = "role_menu_relation"

    id = Column(BigInteger, primary_key=True)
    role_id = Column(BigInteger, comment="角色id")
    menu_id = Column(BigInteger, comment="菜单id")

    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class MenuPermissionRelation(Base):
    """菜单权限表"""

    __tablename__ = "menu_permission_relation"

    id = Column(BigInteger, primary_key=True)
    menu_id = Column(BigInteger, comment="菜单id")
    permission_id = Column(BigInteger, comment="权限id")

    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class UserPermissionRelation(Base):
    """
    用户权限表
        需要更新这个表的情况
            1. 修改用户角色表
            2. 修改角色菜单表
            3. 修改菜单权限表
    """

    __tablename__ = "user_permission_relation"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, comment="用户id")
    permission_id = Column(BigInteger, comment="权限id")

    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
