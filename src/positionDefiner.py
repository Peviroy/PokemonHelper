from utils.jsonHandler import json_getter, json_saver, json_transformer
from utils.positionGetter import PositionGetter


def getButtonPos(data):
    try:
        button_data = data['button']
    except Exception:
        button_data = None
    return button_data


def setButtonPos():
    print('|---------Collect button position-----------|')
    button_pos_label = ['A', 'B', 'GoDown',
                        'GoRight', 'Load', 'Save', 'Home', 'Speed']
    button_pos = PositionGetter(button_pos_label, mode='BUTTON').run()
    return button_pos


def getFlashPos(data):
    '''Helper of getPosData
    '''
    try:
        flash_data = data['flash']
    except Exception:
        flash_data = None
    return flash_data


def setFlashPos():
    print('|---------Collect button position-----------|')
    button_pos_label = ['Flash']
    button_pos = PositionGetter(button_pos_label, mode='FLASH').run()
    return button_pos


def getNumberPos(data):
    '''Helper of getPosData
    '''
    try:
        number_data = data['number']
    except Exception:
        number_data = None
    return number_data


def setNumberPos():
    print('|---------Collect number position-------------|')
    area_pos_label = ['HP', 'WG', 'WF',
                      'SD', 'TG', 'TF']
    area_pos = PositionGetter(area_pos_label, mode='AREA').run()
    return area_pos


def getPosData(POSITION_FILE, addon='None', rewrite=False):
    '''
    :param addon :except for main button, if 'Flash', Flash_point is required; if 'Indivalue', HP, TF and others are required
    '''
    try:
        with open(POSITION_FILE, 'r') as file_p:
            data = json_getter(file_p)
    except FileNotFoundError:
        print('Not exist position file, trying to create one')
        open(POSITION_FILE, 'x')
        data = None

    if data is None and rewrite is True:  # override context
        button_pos = None
        number_pos = None
        flash_pos = None

        button_pos = setButtonPos()
        if addon == 'Indivalue':
            number_pos = setNumberPos()
            flash_pos = getFlashPos(data)
        elif addon == 'Flash':
            flash_pos = setFlashPos()
            number_pos = getNumberPos(data)
        data = json_transformer(
            button_pos, number_area=number_pos, flash_pos=flash_pos)
        print(data)

        choice = input('Save position data to local? [T/F]')
        if choice == 'T':
            print('Saving--------')
            with open(POSITION_FILE, 'w') as file_p:
                json_saver(file_p, data)
        return data
    elif data is not None and rewrite is True:  # complete the rest
        button_pos = getButtonPos(data)
        number_pos = getNumberPos(data)
        flash_pos = getFlashPos(data)

        if button_pos is None:
            button_pos = setButtonPos()
        if addon == 'Indivalue':
            number_pos = setNumberPos()
            flash_pos = getFlashPos(data)
        elif addon == 'Flash':
            flash_pos = setFlashPos()
            number_pos = getNumberPos(data)
        data = json_transformer(
            button_pos, number_area=number_pos, flash_pos=flash_pos)
        print(data)

        choice = input('Save position data to local? [T/F]')
        if choice == 'T':
            print('Saving--------')
            with open(POSITION_FILE, 'w') as file_p:
                json_saver(file_p, data)
        return data
    else:  # ready: data or not rewrite
        return data


if __name__ == "__main__":
    getPosData(POSITION_FILE='criPosition.json', addon='Indivalue')
