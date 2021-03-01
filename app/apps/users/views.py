from typing import Dict

from sanic import Blueprint
from sanic.request import Request
from sanic_openapi import doc

from app.bases.base_swagger_rsp import BaseRsp
from app.consts import PermKey
from app.permissions import perm_define, NeedLoginAndPermUser, IsLoginUser, IsAdminUser
from users import services

user_blueprint = Blueprint("users", url_prefix="/users")

class RegisterParams(object):
    phone : str
    nickname : str
    password : str
    code : str


class RegisterData(object):
    message = doc.String(description="响应描述信息")


class RegisterRsp(BaseRsp):
    data = RegisterData


@user_blueprint.post("/user/register")
@doc.produces(RegisterRsp, description="返回值", content_type="application/json")
async def register(request: Request) -> Dict:
    """
    注册
    """
    return await services.register(request)


@user_blueprint.post("/user/login")
async def login(request: Request) -> Dict:
    """
    登录
    """
    return await services.login(request)


@user_blueprint.get("/user/profile")
@perm_define(perm_clazz=IsLoginUser)
async def profile(request: Request) -> Dict:
    """
    获取本人信息
    """
    return await services.profile(request)


@user_blueprint.get("/user/menus")
@perm_define(perm_clazz=IsLoginUser)
async def get_user_menus(request: Request) -> Dict:
    """
    获取本人菜单信息
    """
    return await services.get_user_menus(request, "")


@user_blueprint.get("/role")
# @perm_define(perm_clazz=NeedLoginAndPermUser, perm_key=PermKey.CreateRole.value)
async def get_role_list(request: Request) -> Dict:
    """
    获取角色列表
    """
    return await services.get_role_list(request)


@user_blueprint.post("/role")
# @perm_define(perm_clazz=NeedLoginAndPermUser, perm_key=PermKey.CreateRole.value)
async def create_role(request: Request) -> Dict:
    """
    创建角色
    """
    return await services.create_role(request)


@user_blueprint.get("/role/<role_id:int>")
# @perm_define(perm_clazz=NeedLoginAndPermUser, perm_key=PermKey.CreateRole.value)
async def get_role(request: Request, role_id: int) -> Dict:
    """
    获取某个角色信息
    """
    return await services.get_role(request, role_id)


@user_blueprint.put("/role/<role_id:int>")
# @perm_define(perm_clazz=NeedLoginAndPermUser, perm_key=PermKey.UpdateRole.value)
async def update_role(request: Request, role_id: int) -> Dict:
    """
    修改角色信息
    """
    return await services.update_role(request, role_id)


@user_blueprint.delete("/role/<role_id:int>")
@perm_define(perm_clazz=NeedLoginAndPermUser, perm_key=PermKey.DestroyRole.value)
async def destroy_role(request: Request, role_id: int) -> Dict:
    """
    删除角色
    """
    return await services.destroy_role(request, role_id)


@user_blueprint.get("/user")
async def get_user_list(request: Request) -> Dict:
    """
    获取用户列表
    """
    return await services.get_user_list(request)


@user_blueprint.get("/user/<user_id:int>/roles")
# @perm_define(perm_clazz=NeedLoginAndPermUser, perm_key=PermKey.CreateRole.value)
async def get_user_roles(request: Request, user_id: int) -> Dict:
    """
    获取用户角色列表
    """
    return await services.get_user_roles(request, user_id)


@user_blueprint.put("/user/<user_id:int>/add_role")
# @perm_define(perm_clazz=NeedLoginAndPermUser, perm_key=PermKey.AddRole.value)
async def add_role(request: Request, user_id: int) -> Dict:
    """
    给用户添加角色
    """
    return await services.add_role(request, user_id)


@user_blueprint.put("/user/<user_id:int>/remove_role")
# @perm_define(perm_clazz=NeedLoginAndPermUser, perm_key=PermKey.RemoveRole.value)
async def remove_role(request: Request, user_id: int) -> Dict:
    """
    给用户移除角色
    """
    return await services.remove_role(request, user_id)


@user_blueprint.post("/init_menu_perms")
@perm_define(perm_clazz=IsAdminUser)
async def init_menu_perms(request: Request) -> Dict:
    """
    初始化菜单和权限
    """
    return await services.init_menu_perms(request)
