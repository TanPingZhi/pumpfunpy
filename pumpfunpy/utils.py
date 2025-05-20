import json

def json_deep_loads(obj):
    """
    Recursively json.loads any string that itself contains JSON,
    walking into dicts and lists.
    """
    # If it’s a str, try to parse it
    if isinstance(obj, str):
        try:
            parsed = json.loads(obj)
        except ValueError:
            return obj
        else:
            return json_deep_loads(parsed)

    # Recurse into dict
    if isinstance(obj, dict):
        return {k: json_deep_loads(v) for k, v in obj.items()}

    # Recurse into list/tuple
    if isinstance(obj, list):
        return [json_deep_loads(v) for v in obj]

    # Other types unchanged
    return obj