"""
@Author: peviroy
@Date: 2020-09-18
@Last Modified by: peviroy
@Last Modified time: 2020-09-18 13:25
"""

import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])
import sys
sys.path.append(os.path.abspath(".."))

from utils.jsonHandler import json_transformer, json_getter, json_saver


class TestJsonHandlerInstance:
    testedConfigFile_1 = './ConfigFile_1.json'
    testedConfigFile_2 = './ConfigFile_2.json'
    testedConfigFile_temp = './ConfigFile_temp.json'

    def test_jsonTransformer(self):
        '''
        Test for transform function of json_transformer
        '''
        platform_name = 'pc'
        button_pos = {'A': [1, 1]}
        indivalue = {'HP': [2, 2]}
        flash = {'FLASH': [3, 3]}
        dic = json_transformer(platform_name, button_pos, indivalue, flash)
        assert dic[platform_name]['button'] == button_pos
        assert dic[platform_name]['indivalue'] == indivalue
        assert dic[platform_name]['flash'] == flash

    def test_jsonGetter(self):
        '''
        Test for 1.flag condition 2.get content  if flag is True
        '''
        with open(self.testedConfigFile_1, 'r') as file_p:  # flag is False
            data = json_getter(file_p)
            assert data.get('pc') is not None
            assert data.get('mobile') is not None

        with open(self.testedConfigFile_2, 'r') as file_p:  # flag is False
            data = json_getter(file_p)
            assert data is None

    def test_jsonSaver(self):
        '''
        Test for save function, by saving temp file and reading content from it
        '''
        with open(self.testedConfigFile_1, 'r') as file_p:
            data = json_getter(file_p)  # get data from ready-made jsonFile
            with open(self.testedConfigFile_temp, 'w+') as file_pt:
                json_saver(file_pt, data)  # save into tempFile
                # assert file exist
                assert os.path.exists(self.testedConfigFile_temp) is True
                file_pt.seek(0)
                copyed_data = json_getter(file_pt)
                assert data == copyed_data  # assert data consistency

            os.remove(self.testedConfigFile_temp)
