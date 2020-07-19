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


def json_transformer(button_pos, number_area):
    obj = {
        "button": {
            "A": button_pos[0],
            "GoDown": button_pos[1],
            "GoRight": button_pos[2],
            "Load": button_pos[3],
            "Save": button_pos[4]
        },
        "number": {
            "HP": number_area[0],
            "WG": number_area[1],
            "WF": number_area[2],
            "SD": number_area[3],
            "TG": number_area[4],
            "TF": number_area[5]
        }
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
    pos_data = json.load(file_p)
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


if __name__ == "__main__":
    # |----------------json formatter test------------------------|
    A = [1, 1]
    GoDown = [2, 2]
    GoRight = [3, 3]
    Load = [4, 4]
    Save = [5, 5]
    HP = [[1, 1], [1, 1]]
    WG = [[2, 2], [2, 2]]
    WF = [[3, 3], [3, 3]]
    SD = [[4, 4], [4, 4]]
    TG = [[5, 5], [5, 5]]
    TF = [[6, 6], [6, 6]]
    obj = json_transformer([A, GoDown, GoRight, Load, Save],
                           [HP, WG, WF, SD, TG, TF])
    print(obj)

    # |----------------empty json reader test---------------------|
    json_data = False
    try:
        file_p = open('criPositionTest.json', 'r')
        json_data = json_getter(file_p)
        print(json_data)
    except FileNotFoundError:
        print('file not exists')

    # |----------------empty json reader test---------------------|
    if json_data is False:
        print('writing data')
        with open('criPositionTest.json', 'w') as file_p:
            json_saver(file_p, obj)
