# -*- coding: utf-8 -*-
"""
DB操作层

只涉及DB操作，最好不涉及业务
"""
from typing import List

from app.exceptions import AuthenticationFailed, ObjNotFound
from app.utils import sha256
from users.models import User, UserPermissionRelation, Permission, Role, UserRoleRelation, RoleMenuRelation, Menu, \
    Platform


def authenticate(phone: str, password: str) -> User:
    hashed_password = sha256(password)
    user: User = User.query.filter(
        User.phone == phone, User.password == hashed_password
    ).first()
    if not user:
        raise AuthenticationFailed()
    return user


def get_user(user_id: int) -> User:
    user: User = User.get(user_id)
    return user


def get_user_by_phone(phone: str) -> User:
    user: User = User.query.filter_by(phone=phone).first()
    return user


def get_user_perm_key_list(user_id: int) -> List:
    uprs = UserPermissionRelation.query.filter_by(user_id=user_id).all()
    perm_id_list = [x.permission_id for x in uprs]
    perms = Permission.query.filter(Permission.id.in_(perm_id_list)).all()
    return [p.key for p in perms]


def get_role(role_id, raise_exception=False) -> Role:
    role: Role = Role.get(role_id)
    if not role and raise_exception:
        raise ObjNotFound()
    return role


def get_user_list() -> List:
    users = User.query.filter_by().all()
    return users


def delete_role(role_id, raise_exception=False) -> None:
    role: Role = Role.get(role_id)
    if not role:
        if raise_exception:
            raise ObjNotFound()
    else:
        role.delete()


def get_user_roles(user_id):
    """
    获取用户角色
    """
    urrs = UserRoleRelation.query.filter_by(user_id=user_id).all()
    role_id_list = [x.role_id for x in urrs]
    roles = []
    if role_id_list:
        roles = Role.query.filter(Role.id.in_(role_id_list)).all()
    return roles


def get_user_menu_by_role_id_list(role_id_list: List):
    """
    获取用户菜单权限
    """
    rmrs = RoleMenuRelation.query.filter(RoleMenuRelation.role_id.in_(role_id_list)).all()
    return rmrs


def get_menu_by_menu_id_list(menu_id_list: List, platform_id: int):
    """
    通过菜单ID和平台ID获取菜单列表
    """
    menus = Menu.query.filter(
        Menu.id.in_(menu_id_list),
        Menu.platform_id == platform_id
    ).all()
    return menus


def get_role_relate_by_uid_and_rid(user_id, role_id):
    """
    通过用户ID和角色ID获取用户角色关联信息
    """
    urr: UserRoleRelation = UserRoleRelation.query.filter_by(
        user_id=user_id,
        role_id=role_id,
    ).first()
    return urr


def get_role_list():
    """
    获取角色列表
    """
    roles = Role.query.filter_by().all()
    return roles


def get_platform_by_key(platform_key: str, raise_exception=False) -> Platform:
    """
    通过平台Key获取平台
    """
    platform = Platform.query.filter_by(key=platform_key).first()
    if not platform and raise_exception:
        raise ObjNotFound()
    return platform
