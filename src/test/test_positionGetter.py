"""
@Author: peviroy
@Date: 2020-09-23
@Last Modified by: peviroy
@Last Modified time: 2020-09-23 10:31
"""

import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])
import sys
sys.path.append(os.path.abspath(".."))

from utils.positionGetter import PositionGetter


class TestPositionGetterInstance:
    def test_PointMode(self):
        posGetter = PositionGetter(mode='POINT')
        assert isinstance(posGetter(['Up', 'Down']), dict)

    def test_AreaMode(self):
        posGetter = PositionGetter(mode='AREA')
        assert isinstance(posGetter(['HP', 'WG', 'WF']), dict)
