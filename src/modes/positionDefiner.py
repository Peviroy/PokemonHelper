"""
@Author: peviroy
@Last Modified by: peviroy
@Last Modified time: 2020-09-24
@Note: Script for defining key areas or keyboard map
"""
from utils.jsonHandler import json_getter, json_saver, json_transformer
from utils.positionGetter import PositionGetter


class PostionDefiner():
    '''
    Constructor of positionData.json, build step by step;
    1. button_data is initially constructed
    2. flash, indivalue can be construcetd via 'addon' mode
    '''

    def __init__(self, position_file: str):
        self.position_file = position_file
        self.data = self._load_data(position_file) or {}  # {} for default

    def run(self, platform_name: str, addon: str = '', rewrite: bool = False) -> dict:
        platforms = ['desktop', 'mobile']
        assert platform_name in platforms
        self.platfroom_name = platform_name

        # IF, get data or construct data
        if self.data.get(self.platfroom_name, {}) != {} and addon == '' and rewrite is False:
            return self.data[platform_name]
        elif self.data.get(self.platfroom_name, {}) == {} or rewrite is True:  # make data
            button = None
            indivalue = None
            flash = None
        else:  # data is not None and addon is not None  | addon mode
            button = self._get_attr_fromData('BUTTON')
            indivalue = self._get_attr_fromData('INDIVALUE')
            flash = self._get_attr_fromData('FLASH')

        if button is None:
            button = self._set_attr_value('BUTTON')
        if addon.lower() == 'indivalue':
            indivalue = self._set_attr_value('INDIVALUE')
        elif addon.lower() == 'flash':
            flash = self._set_attr_value('FLASH')

        # FORMAT data
        platform_data = json_transformer(
            platform_name, button_pos=button, indivalue_area=indivalue, flash_pos=flash)

        # Save data or not
        while True:
            choice = input('Save position data to local? [T/f]')
            if choice.lower() == 't' or choice == '':  # save
                # get another part of data, for data consists of 'mobile' and 'desktop'
                platforms.remove(platform_name)
                other_platform_name = platforms[0]
                other_platform_data = self.data.get(other_platform_name, {})
                new_data = {}
                new_data.update(platform_data)
                print(new_data)
                new_data.update({other_platform_name: other_platform_data})
                print(new_data)
                print('Saving--------')
                with open(self.position_file, 'w') as file_p:
                    json_saver(file_p, new_data)
                break
            elif choice.lower() == 'f':  # not
                break
            else:
                continue

        # Last, only specified platform data is returned
        print('New updated data:\n', new_data)
        return platform_data

    def _load_data(self, position_file):
        data = None
        try:
            with open(position_file, 'r') as file_p:
                data = json_getter(file_p)
        except FileNotFoundError:
            print('Not exist position file, trying to create one')
            with open(position_file, 'x'):
                pass
        return data

    def _get_attr_fromData(self, attr_name: str) -> dict:
        '''
        load attr value from self.data
        '''
        assert attr_name.lower() in ['indivalue', 'flash', 'button']
        try:
            attr_data = self.data[self.platfroom_name][attr_name.lower()]
        except Exception:
            attr_data = None
        return attr_data

    def _set_attr_value(self, attr_name: str) -> dict:
        '''
        set attr value using utils.positionGetter; the format of deffirent attr is determined
        '''
        assert attr_name.lower() in ['indivalue', 'flash', 'button']
        attr_value = {}
        if attr_name.lower() == 'button':
            print('|---------Collect button position-------------|')
            button_label = ['A', 'B', 'GoDown',
                            'GoRight', 'Load', 'Save', 'Home', 'Speed']
            posGetter = PositionGetter('POINT')
            attr_value = posGetter(button_label)

        elif attr_name.lower() == 'flash':
            print('|---------Collect flash position--------------|')
            flash_label = ['Flash']
            posGetter = PositionGetter('POINT')
            attr_value = posGetter(flash_label)
        else:  # indivalue
            print('|---------Collect indivalue position----------|')
            indivalue_label = ['HP', 'WG', 'WF',
                               'SD', 'TG', 'TF']
            posGetter = PositionGetter('AREA')
            attr_value = posGetter(indivalue_label)

        return attr_value
