import json

def convert_dict_to_str(json_dict):
    """
        return str from the json dict passed


        """
    try:
        json_object = json.dumps(json_dict, indent=4)

        return str(json_object).encode()

    except Exception as e:
        raise ValueError(f"Cannot convert {json_dict} to string")

def parse_json_in_to_dict(json_str):
    """
    return dict from the json object passed

    :param json_str : Json Obj   : Json read from program socket
    :return:        : Dict       : Dict representation of json
    """
    try:
        return json.loads(json_str)
    except Exception as e:
        # raise ValueError(f"Cannot convert {json_str} to jsonObj")
        return {}