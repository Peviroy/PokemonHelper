import json

'''
    JSON FORMAT:
    {
        "flag": false,
        "pos": {
            "button": {
                "A": null,
                "GoDown": null,
                "GoRight": null,
                "Load": null,
                "Save": null,
            },
            "number": {
                "HP": null,
                "WG": null,
                "WF": null,
                "SD": null,
                "TG": null,
                "TF": null
            }
        }
    }
'''


def json_transformer(button_pos: dict, number_area: dict):
    '''combine button_pos and number_area into one dict
    Example:
    --------
        button_pos =  {
            "A": button_pos[0],
            "B": button_pos[1],
            "GoDown": button_pos[2],
            "GoRight": button_pos[3],
            "Load": button_pos[3],
            "Save": button_pos[4],
            "Home": button_pos[5],
            "Speed": button_pos[6],
        }
    '''
    obj = {
        "button": button_pos,
        "number": number_area
    }
    return obj


def json_getter(file_p):
    '''
    ARGS:
    ----------
    file_p : [file pointer]

    RETURN:
    ----------
    python object or None
    '''
    try:
        pos_data = json.load(file_p)
    except json.JSONDecodeError:
        pos_data = None
    if pos_data is None or pos_data['flag'] is False:
        return None
    return pos_data['data']


def json_saver(file_p, data):
    '''
    ARGS:
    ----------
    file_p : [file pointer]
    data : [dictionary]
    '''
    object = {
        "flag": True,
        "data": data
    }
    print(json.dumps(object))
    json.dump(object, file_p)
