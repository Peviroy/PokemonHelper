"""
@Author: peviroy
@Date: 2020-09-18
@Last Modified by: peviroy
@Last Modified time: 2020-09-24 17:30
"""

import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])
import sys
sys.path.append(os.path.abspath(".."))


from modes.positionDefiner import PostionDefiner
from utils.jsonHandler import json_getter


class TestPositionDefinerInstance:
    testedPositionFile_complete = './ConfigFile_1.json'
    testedPositionFile_new = './ConfigFile_construct.json'

    def test_getDataFromFile(self):
        posDefiner = PostionDefiner(self.testedPositionFile_complete)
        mobile_data = posDefiner.run('mobile')
        assert mobile_data is not None
        assert mobile_data.get('button') is not None

    def test_construnctData(self):
        posDefiner = PostionDefiner(self.testedPositionFile_new)
        new_data = posDefiner.run('mobile')
        assert new_data is not None

        with open(self.testedPositionFile_new, 'r') as file_p:  # flag is False
            data = json_getter(file_p)
            assert data.get('mobile') != {}
            assert data.get('desktop') == {}

    def test_appendNewPlatformData(self):
        posDefiner = PostionDefiner(self.testedPositionFile_new)
        new_data = posDefiner.run('desktop')
        assert new_data is not None

        with open(self.testedPositionFile_new, 'r') as file_p:  # flag is False
            data = json_getter(file_p)
            assert data.get('mobile') != {}
            assert data.get('desktop') != {}

    def test_appendNewAddonData(self):
        posDefiner = PostionDefiner(self.testedPositionFile_new)
        new_data = posDefiner.run('desktop', addon='FLASH')
        assert new_data is not None

        with open(self.testedPositionFile_new, 'r') as file_p:  # flag is False
            data = json_getter(file_p)
            assert data.get('mobile') != {}
            assert data.get('desktop') != {}

    def test_rewriteData(self):
        '''
        Note: Pytest runs the test in the same order as they are found in the test module
        '''
        with open(self.testedPositionFile_new, 'r') as file_p:  # flag is False
            data = json_getter(file_p)
            old_mobile_data = data.get('mobile')
        posDefiner = PostionDefiner(self.testedPositionFile_new)
        new_data = posDefiner.run('mobile', rewrite=True)
        assert new_data is not None

        with open(self.testedPositionFile_new, 'r') as file_p:  # flag is False
            data = json_getter(file_p)
            assert data.get('mobile') != {}
            assert data.get('mobile') != old_mobile_data

        # final remove
        os.remove(self.testedPositionFile_new)
