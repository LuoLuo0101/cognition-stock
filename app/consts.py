from enum import unique

from app.bases.base_enum import BaseConstEnum


@unique
class PermKey(BaseConstEnum):
    """
    对应 Permission 表的数据
    """
    UserProfile = "GET:/user/profile"           # 获取用户个人信息
    GetRoleList = "GET:/role"                   # 获取角色列表
    CreateRole = "POST:/role"                   # 创建角色
    UpdateRole = "PUT:/role/<role_id>"          # 更新角色
    DestroyRole = "DELETE:/role/<role_id>"      # 删除角色
    AddRole = "PUT:/user/<user_id>/add_role"    # 给用户添加角色
    RemoveRole = "PUT:/user/<user_id>/remove_role"    # 给用户移除角色


@unique
class CacheKey(BaseConstEnum):
    UserPerm = "USER_PERM"
    UserObj = "USER_OBJ"
    UserMenu = "USER_MENU"
