import json


def json_deep_loads(obj):
    if isinstance(obj, str):
        try:
            parsed = json.loads(obj)
        except ValueError:
            return obj
        else:
            return json_deep_loads(parsed)

    if isinstance(obj, dict):
        return {k: json_deep_loads(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [json_deep_loads(v) for v in obj]

    return obj
