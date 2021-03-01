# -*- coding: utf-8 -*-
"""
DB操作二次封装层

缓存会在这用到
"""
from typing import List

from sanic import Sanic

from app.consts import CacheKey
from app.utils import get_data_from_db_or_cache, get_cache_key, get_data_with_key, concat_data_with_data_relate
from users import repositories as user_repo


async def get_user_menus_from_cache_or_db(app: Sanic, user_id: int, platform_id: int,
                                          expire: int=2 * 60 * 60, force: bool = False) -> List:
    """
    获取用户拥有的菜单权限

    [{
        "id": 1,
        "name": "一级菜单",
        "parent_id": null,
        "children": [{
            "id": 3,
            "name": "二级菜单",
            "parent_id": 1,
            "children": [{
                "id": 5,
                "name": "三级菜单",
                "parent_id": 3,
                "children": []
            }]
        }]
    }]
    """

    def get_data_callback() -> List:
        roles = user_repo.get_user_roles(user_id)
        role_id_list = [x.id for x in roles]
        if not role_id_list:
            return []
        # 角色菜单关联
        rmrs = user_repo.get_user_menu_by_role_id_list(role_id_list=role_id_list)
        if not rmrs:
            return []
        menu_id_list = [x.menu_id for x in rmrs]
        menus = user_repo.get_menu_by_menu_id_list(menu_id_list=menu_id_list, platform_id=platform_id)
        menu_list = [menu.to_dict() for menu in menus]
        data_relate = get_data_with_key(menu_list)
        root_list = data_relate.get(None)
        return concat_data_with_data_relate(root_list, data_relate)

    key = get_cache_key(key_list=[CacheKey.UserMenu.value, platform_id, user_id])
    data: List = await get_data_from_db_or_cache(
        app=app, key=key, get_data_callback=get_data_callback, force=force, expire=expire
    )
    return data

