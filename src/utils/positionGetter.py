import pyautogui
from utils.imageGrab import grab_screen
import pytesseract
from PIL import Image
import os


def numberCapture(name, min_limit, pos1_x, pos1_y, pos2_x, pos2_y):
    # if not captured, retry for 5 times to make sure: 1.screenshot is right; number is recgonized correctly
    for count in range(5):
        img = grab_screen(pos1_x, pos1_y, pos2_x, pos2_y)
        img.save(os.path.join('../../screenshots', name + '.png'))
        img = Image.open(os.path.join('../../screenshots', name + '.png'))

        number = pytesseract.image_to_string(
            img, lang="chi_sim", config='--psm 7 --oem 0 -c tessedit_char_whitelist=0123456789')

        try:
            number = int(number)
            print(number)
            # if name == 'HP' and number == 31:   # 单个体择优
            # return 6
            if number == min_limit or number == min_limit + 1:
                return 1
            return 0
        except Exception:
            continue

    print('not captured, skip this circle')
    return -1


class PositionGetter():
    '''Place your mouse at the position where you want to konw, and keydown ENTER for alert box
    Usage: PositionGetter(['HO', 'HI', 'HP']).run()
    '''

    def __init__(self, position_names, mode='BUTTON'):
        '''
        :param [position_names]--list
        '''
        self.position_names = position_names
        self.mode = mode

    def run(self):
        '''
        :param [mode]--str mode-BUTTON, for each pos, one point and without confirm;
                           mode-AREA, for each pos, two point and with confirmation;
        '''
        positions = []  # record | return
        for position_name in self.position_names:
            if self.mode == 'BUTTON' or self.mode == 'FLASH':
                pyautogui.alert(
                    'Place mouse for "{0}", and key down ENTER'.format(position_name))
                currentMouseX, currentMouseY = pyautogui.position()
                print('{0} lies at ({1}, {2})'.format(
                    position_name, currentMouseX, currentMouseY))
                positions.append(
                    (position_name, (currentMouseX, currentMouseY)))

            elif self.mode == 'AREA':
                while True:  # exit when confirmed
                    point_area = []  # area consists of two point
                    for index in range(2):
                        pyautogui.alert(
                            'Place mouse for "{0}-{1}", and key down ENTER'.format(position_name, index + 1))
                        currentMouseX, currentMouseY = pyautogui.position()
                        print('{0}-{3} lies at ({1}, {2})'.format(
                            position_name, currentMouseX, currentMouseY, index + 1))
                        point_area.append((currentMouseX, currentMouseY))
                    if self._showImageArea(point_area):
                        numberCapture('TT', 0, point_area[0][0], point_area[0][1],
                                      point_area[1][0], point_area[1][1])
                        if pyautogui.confirm('Is this proper?') == 'OK':
                            break
                positions.append((position_name, point_area))
            else:
                print('No such mode')
        print('Summary:', dict(positions))
        return dict(positions)

    def _showImageArea(self, point_area):
        '''
        :param [point_area]-list | example: [(1, 1), (2, 2)]
        '''
        x1, y1, x2, y2 = [point_area[0][0], point_area[0][1],
                          point_area[1][0], point_area[1][1]]
        if x1 > x2 or y1 > y2:
            print('Area selection error: second point must be right below')
            return False
        img = grab_screen(x1, y1, x2, y2)
        img.show()
        return True


if __name__ == "__main__":
    print("|---------------Testing for BUTTON mode'----------------|")
    PositionGetter(['HO', 'HI', 'HP']).run()
    print("|---------------Testing for Area mode'------------------|")
    PositionGetter(['HO', 'HI', 'HP'], mode='AREA').run()
