"""
@Author: peviroy
@Last Modified by: peviroy
@Last Modified time: 2020-09-18
"""
import json

'''
    JSON FORMAT:
    Even if data derived into 'desktop' and 'mobile', jsonHandler only process one 'flag' and 'data'
    {
        "flag":
        "data":{
            "desktop":{
                "button": {
                    "A": [<str| button name>],
                },
                "indivalue": {
                    "HP": [<x1, y1|coordinary>],
                },
                "flash": {
                    "Flash": [<x1, y1|coordinary>],
                },
            },
            "mobile":{
                "button": {
                    "A": [<x1, y1|coordinary>],
                },
                "indivalue": {
                    "HP": [<x1, y1|coordinary>],
                },
                "flash": {
                    "Flash": [<x1, y1|coordinary>],
                },
            }
        }
    }
'''


def json_transformer(platform_name, button_pos, indivalue_area, flash_pos) -> dict:
    '''
    combine button_pos and number_area into one dict
    '''
    dic = {
        platform_name: {
            "button": button_pos,
            "indivalue": indivalue_area,
            "flash": flash_pos
        }
    }
    return dic


def json_getter(file_p) -> dict:
    '''
    Note:
    ----------
    Simply return dataInfo from JSON FILE with checker on flag and decodeError

    ARGS:
    ----------
    file_p : {_io.TextIOWrapper}  -- file pointer

    RETURN:
    ----------
    {dict | None}
    '''
    try:
        pos_data = json.load(file_p)
    except json.JSONDecodeError:
        pos_data = None
    # decode fails or disabled
    if pos_data is None or pos_data['flag'] is False:
        return None
    return pos_data['data']


def json_saver(file_p, data: dict):
    '''
    ARGS:
    ----------
    file_p : {_io.TextIOWrapper}  -- file pointer
    data : {dict} -- position dictionary to be saved into JSON FILE
    '''
    object = {
        "flag": True,
        "data": data
    }
    json.dump(object, file_p)
