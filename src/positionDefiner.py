from jsonHandler import json_getter, json_saver, json_transformer
from utils.positionGetter import PositionClicker


POSITION_FILE = 'criPosition.json'

# 1028 524


def getPosData():
    with open(POSITION_FILE, 'r') as file_p:
        data = json_getter(file_p)
    if data is not None:  # already
        return data
    else:  # not ready
        button_pos_label = ['A', 'B', 'GoDown',
                            'GoRight', 'Load', 'Save', 'Home', 'Speed']
        number_area_label = ['HP', '_HP2', 'WG', '_WG2', 'WF',
                             '_WF2', 'SD', '_SD2', 'TG', '_TG2', 'TF', '_TF2']

        labels = []
        labels.extend(button_pos_label)
        labels.extend(number_area_label)

        PositionClicker(labels).run()

        button_pos = []
        print('input format: <pos_x> <pos_y>')
        for name in button_pos_label:
            raw_pos = input(name + '> ')
            try:
                pos1, pos2 = raw_pos.split(' ')
                button_pos.append((int(pos1), int(pos2)))
            except ValueError:
                print('Not valid input format!')

        number_area = []
        print('input example: <pos1_x> <pos1_y> <pos2_x> <pos2_y>')
        for name in number_area_label:
            if name[0] == '_':
                continue
            raw_pos = input(name + '> ')
            try:
                pos1, pos2, pos3, pos4 = raw_pos.split(' ')
                number_area.append(
                    [(int(pos1), int(pos2)), (int(pos3), int(pos4))])
            except ValueError:
                print('Not valid input format!')

        data = json_transformer(button_pos, number_area)
        choice = input('Save position data to local? [T/F]')

        if choice == 'T':
            print('Saving--------')
            with open(POSITION_FILE, 'w') as file_p:
                json_saver(file_p, data)

        return data


if __name__ == "__main__":
    getPosData()
