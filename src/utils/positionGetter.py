"""
@Author: peviroy
@Last Modified by: peviroy
@Last Modified time: 2020-09-23
"""
import pyautogui

from utils.imageGrab import grab_screen


class PositionGetter():
    '''
    Place your mouse at the position where you want to konw, and keydown ENTER for alert box
    Usage: posGetter = PositionGetter(mode='AREA')
           posGetter(['HP', 'WF'])
    '''

    def __init__(self, mode: str):
        '''
        :param [mode]--str mode-POINT, for each pos, one point and without repeat confirmation;
                           mode-AREA, for each pos, two point and with repeat confirmation;
        '''
        self.mode = mode

    def __call__(self, position_names: list) -> dict:
        '''
        :param [position_names]-- str list, 1-D
        '''
        positions = []  # record | return
        for position_name in position_names:
            if self.mode == 'POINT':
                pyautogui.alert(
                    'Place mouse for "{0}", and key down ENTER to confirm choice'.format(position_name))
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
                            'Place mouse for "{0}-pos{1}", and key down ENTER to confirm choice'.format(position_name, index + 1))
                        currentMouseX, currentMouseY = pyautogui.position()
                        print('{0}-pos{3} lies at ({1}, {2})'.format(
                            position_name, currentMouseX, currentMouseY, index + 1))
                        point_area.append((currentMouseX, currentMouseY))
                    if self.areaCapture(point_area):
                        if pyautogui.confirm('Is this proper?') == 'OK':
                            break
                positions.append((position_name, point_area))
            else:
                print('No such mode')
        print('Summary:', dict(positions))
        return dict(positions)

    def areaCapture(self, point_area: list) -> bool:
        '''
        Note:
        -----------
            Capture a digital image from designated area
        ARGS:
        -----------
            name: {str} -- the name of image to be identified for saving img locally
            point_area {list} -- [[x1, y1], [x2, y2]]
        '''
        pos1_x, pos1_y, pos2_x, pos2_y = [
            coord for point in point_area for coord in point]
        if pos1_x > pos2_x or pos1_y > pos2_y:
            pyautogui.alert(
                'Area selection error: second point must be right below')
            return False
        # retry for 2 times to make sure: target area is captured
        for count in range(2):
            img = grab_screen(pos1_x, pos1_y, pos2_x, pos2_y)

        img.show()
        return True
