# -*- coding: utf-8 -*-
"""
端口服务层

涉及View函数的具体操作
"""
import pickle
from typing import Dict

from sanic.request import Request

import settings
from app.database import transactional
from app.exceptions import InvalidCode, UserExist
from app.utils import sha256, generate_token
from users.functions import get_user_menus_from_cache_or_db
from users.models import User, Role, UserRoleRelation
from users import repositories as user_repo
from users.repositories import get_platform_by_key


@transactional
async def register(request: Request) -> Dict:
    request_body = request.json

    phone = request_body.get("phone")
    nickname = request_body.get("nickname")
    password = request_body.get("password")
    code = request_body.get("code")

    key = f"register|{phone}"
    await request.app.redis.set(key, "0000", expire=300)  # TODO 临时设置 code=0000，有效期5分钟
    value = await request.app.redis.get(key)
    if code != value:
        raise InvalidCode()

    user = user_repo.get_user_by_phone(phone)
    if user:
        raise UserExist()

    hashed_password = sha256(password)

    user = User(phone=phone, password=hashed_password, nickname=nickname)
    user.save()
    return {"message": "注册成功"}


@transactional
async def login(request: Request) -> Dict:
    request_body = request.json
    phone = request_body["phone"]
    password = request_body["password"]

    user: User = user_repo.authenticate(phone, password)
    token: str = generate_token({"user_id": user.id}, secret=settings.JWT_SECRET_KEY, ttl=settings.JWT_TTL)
    user.token = token
    user.save()

    key: str = f"user|{user.id}"
    value: bytes = pickle.dumps(user)
    await request.app.redis.set(key, value)
    return {"token": token}


async def profile(request: Request) -> Dict:
    user: User = request.ctx.user
    return user.to_dict()


async def get_user_menus(request: Request, platform_key) -> Dict:
    user: User = request.ctx.user
    platform = get_platform_by_key(platform_key, raise_exception=True)
    user_menus = get_user_menus_from_cache_or_db(request.app, user.id, platform.id)
    return {"message": "获取用户菜单成功", "results": user_menus}


@transactional
async def get_role_list(request: Request) -> Dict:
    """
    获取角色列表
    """
    roles = user_repo.get_role_list()
    return {"message": "获取角色列表成功", "results": [role.to_dict() for role in roles]}


@transactional
async def create_role(request: Request) -> Dict:
    """
    创建角色
    """
    request_body = request.json
    name = request_body["name"]
    description = request_body["description"]
    role = Role(name=name, description=description)
    role.save()
    return {"message": "创建成功"}


@transactional
async def get_role(request: Request, role_id) -> Dict:
    """
    获取角色列表
    """
    role = user_repo.get_role(role_id, raise_exception=True)
    return {"message": "获取角色列表成功", "result": role.to_dict()}


@transactional
async def update_role(request: Request, role_id) -> Dict:
    """
    修改角色信息
    """
    request_body = request.json
    name = request_body["name"]
    description = request_body["description"]
    role = user_repo.get_role(role_id)
    role.name = name
    role.description = description
    role.save()
    return {"message": "修改成功"}


@transactional
async def destroy_role(request: Request, role_id) -> Dict:
    """
    删除角色
    """
    user_repo.delete_role(role_id, raise_exception=True)
    return {"message": "删除成功"}


async def get_user_list(request: Request) -> Dict:
    users = user_repo.get_user_list()
    return {"message": "获取成功", "results": [x.to_dict() for x in users]}


async def get_user_roles(request: Request, user_id) -> Dict:
    """
    获取用户角色
    """
    roles = user_repo.get_user_roles(user_id)
    return {"message": "获取成功", "results": [x.to_dict() for x in roles]}


@transactional
async def add_role(request: Request, user_id) -> Dict:
    """
    给用户添加角色
    """
    request_body = request.json
    role_id = request_body["role_id"]
    urr = user_repo.get_role_relate_by_uid_and_rid(user_id, role_id)
    if not urr:
        urr = UserRoleRelation(user_id=user_id, role_id=role_id)
        urr.save()
    return {"message": "用户添加角色成功"}


@transactional
async def remove_role(request: Request, user_id) -> Dict:
    """
    给用户移除角色
    """
    request_body = request.json
    role_id = request_body["role_id"]
    urr = user_repo.get_role_relate_by_uid_and_rid(user_id, role_id)
    if urr:
        urr.delete()
    return {"message": "用户移除角色成功"}


@transactional
async def init_menu_perms(request: Request) -> Dict:
    """
    初始化菜单和权限
    """
    pass
