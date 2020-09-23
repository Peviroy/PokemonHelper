"""
@Author: peviroy
@Last Modified by: peviroy
@Last Modified time: 2020-09-21

@Note: The screenshot function is based on X11, using cpp lib "prtscn.so"
"""
import ctypes
import os
from PIL import Image

LibName = 'prtscn.so'
AbsLibPath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + LibName
grab = ctypes.CDLL(AbsLibPath)


def grab_screen(x1, y1, x2, y2):
    w, h = x2 - x1, y2 - y1
    size = w * h
    objlength = size * 3

    grab.getScreen.argtypes = []
    result = (ctypes.c_ubyte * objlength)()

    grab.getScreen(x1, y1, w, h, result)
    return Image.frombuffer('RGB', (w, h), result, 'raw', 'RGB', 0, 1)
