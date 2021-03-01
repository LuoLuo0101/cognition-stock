import json
from datetime import datetime
from decimal import Decimal


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)


def to_json(response) -> str:
    return json.dumps(response, cls=CustomJSONEncoder)


if __name__ == '__main__':
    print(json.dumps({"t": datetime.now()}, cls=CustomJSONEncoder))
