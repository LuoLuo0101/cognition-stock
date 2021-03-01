from typing import Dict


def get_success_data(data: Dict={}):
    return {
        "is_success": True,
        "data": data
    }


def get_failure_data(reason: str="", detail: str="", data: Dict={}):
    return {
        "is_success": False,
        "reason": reason,
        "detail": detail,   # traceback
        "data": data
    }
