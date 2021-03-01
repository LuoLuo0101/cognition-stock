import sys
from importlib import reload
import traceback

from app.utils.common_utils import get_failure_data, get_success_data


class MyHelper(object):
    @staticmethod
    def importOrReload(module_name, *names):
        try:
            if module_name in sys.modules:
                reload(sys.modules[module_name])
            else:
                __import__(module_name, fromlist=names)

            for name in names:
                globals()[name] = getattr(sys.modules[module_name], name)

            return get_success_data({"module": globals()[name]})

        except Exception as e:
            return get_failure_data(reason=str(e), detail=str(traceback.format_exc()))
