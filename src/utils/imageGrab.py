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


if __name__ == '__main__':
    import pytesseract

    im = grab_screen(321, 492, 358, 533)
    # im = grab_screen(355, 475, 470, 516) WG
    # im = grab_screen(468, 475, 581, 516) WF
    # im = grab_screen(278, 492, 393, 532) SD
    # im = grab_screen(394, 492, 505, 532)
    # im = grab_screen(507, 475, 616, 516) TF
    # im = grab_screen(507, 475, 616, 516)

    im.save('image.png')
    img = Image.open('image.png')
    img.show()

    text = pytesseract.image_to_string(
        img, lang="chi_sim", config='--psm 7 --oem 0 -c tessedit_char_whitelist=0123456789')
    print(text)
