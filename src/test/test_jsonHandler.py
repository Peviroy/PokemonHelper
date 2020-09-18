"""
@Author: peviroy
@Date: 2020-09-18
@Last Modified by: peviroy
@Last Modified time: 2020-09-18
"""

import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])
import sys
sys.path.append(os.path.abspath(".."))

from utils.jsonHandler import json_transformer


class TestJsonHandlerInstance:
    def test_jsonTransformer(self):
        platform_name = 'pc'
        button_pos = {'A': [1, 1]}
        indivalue = {'HP': [2, 2]}
        flash = {'FLASH': [3, 3]}
        dic = json_transformer(platform_name, button_pos, indivalue, flash)
        assert dic[platform_name]['button'] == button_pos
        assert dic[platform_name]['indivalue'] == indivalue
        assert dic[platform_name]['flash'] == flash
