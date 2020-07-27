from utils.jsonHandler import json_getter, json_saver, json_transformer
from utils.positionGetter import PositionGetter


def getPosData(POSITION_FILE):
    try:
        with open(POSITION_FILE, 'r') as file_p:
            data = json_getter(file_p)
    except FileNotFoundError:
        print('Not exist position file, trying to create one')
        open(POSITION_FILE, 'x')
        data = None

    if data is not None:  # already
        return data
    else:  # not ready
        print('|---------Collect button position-----------|')
        button_pos_label = ['A', 'B', 'GoDown',
                            'GoRight', 'Load', 'Save', 'Home', 'Speed']
        button_pos = PositionGetter(button_pos_label, mode='BUTTON').run()

        print('|---------Collect area position-------------|')
        area_pos_label = ['HP', 'WG', 'WF',
                          'SD', 'TG', 'TF']
        area_pos = PositionGetter(area_pos_label, mode='AREA').run()

        data = json_transformer(button_pos, area_pos)
        print(data)
        choice = input('Save position data to local? [T/F]')

        if choice == 'T':
            print('Saving--------')
            with open(POSITION_FILE, 'w') as file_p:
                json_saver(file_p, data)

        return data


if __name__ == "__main__":
    getPosData(POSITION_FILE='criPosition.json')
