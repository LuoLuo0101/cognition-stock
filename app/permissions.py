import functools
from typing import Dict
from typing import List

from sanic import Sanic
from sanic.request import Request

from app.consts import CacheKey
from app.exceptions import NoToken, InvalidToken
from app.exceptions import PermissionDenied
from app.utils import decode_token, get_data_from_db_or_cache, get_cache_key
from users import repositories
from users.models import User


def get_token_or_raise(request: Request) -> str:
    token: str = request.token
    if token is None:
        raise NoToken()
    return token


async def get_user_from_cache_or_db(app: Sanic, user_id: int, expire: int=2 * 60 * 60, force: bool = False) -> User:
    """
    获取用户
    """

    def get_data_callback() -> User:
        return repositories.get_user(user_id)

    key = get_cache_key(key_list=[CacheKey.UserObj.value, user_id])
    data: User = await get_data_from_db_or_cache(
        app=app, key=key, get_data_callback=get_data_callback,
        force=force, expire=expire
    )
    return data


async def get_user_perm_from_cache_or_db(app: Sanic, user_id: int, expire: int=2 * 60 * 60,
                                         force: bool = False) -> List:
    """
    获取用户权限
    """

    def get_data_callback() -> List:
        return repositories.get_user_perm_key_list(user_id)

    key = get_cache_key(key_list=[CacheKey.UserPerm.value, user_id])
    data: List = await get_data_from_db_or_cache(
        app=app,
        key=key, get_data_callback=get_data_callback,
        force=force, expire=expire
    )
    return data


def check_jwt_and_set_user(f):
    """
    登录并设置用户
    """

    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        request = kwargs.get("request")
        token: str = get_token_or_raise(request)
        payload: Dict = decode_token(token, secret=request.app.config.JWT_SECRET_KEY)
        user_id: int = payload["user_id"]
        user: User = await get_user_from_cache_or_db(request.app, user_id)
        print(payload)
        if user.token != token:
            raise InvalidToken()

        request.ctx.user = user  # 给request上下文设置user对象
        return await f(*args, **kwargs)

    return wrapper


class BasePermission(object):
    async def has_permission(self, request):
        raise NotImplementedError


class AllowAnyUser(BasePermission):
    async def has_permission(self, request):
        return True


class IsLoginUser(BasePermission):
    @check_jwt_and_set_user
    async def has_permission(self, request):
        return request.ctx.user.is_active


class IsAdminUser(BasePermission):
    @check_jwt_and_set_user
    async def has_permission(self, request):
        return request.ctx.user.is_admin


class NeedLoginAndPermUser(BasePermission):
    """
    需要登录，并有对应接口权限
    """

    @check_jwt_and_set_user
    async def has_permission(self, request) -> bool:
        if not request.ctx.user.is_active:
            return False
        perm_key_list: List = await get_user_perm_from_cache_or_db(request.app, user_id=request.ctx.user.id)
        return request.ctx.perm_key in perm_key_list


def perm_define(perm_clazz=AllowAnyUser, perm_key: str = None):
    """
    权限定义

    :param perm_clazz: 权限认证类
    :param perm_key: 接口权限Key
    :return:
    """

    def outer(func):
        @functools.wraps(func)
        async def inner(request: Request, *args, **kwargs):
            request.ctx.perm_key = perm_key
            perm = perm_clazz()
            has_perm = await perm.has_permission(request=request)
            if not has_perm:
                raise PermissionDenied()
            return await func(request, *args, **kwargs)

        return inner

    return outer
