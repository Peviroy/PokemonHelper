from pymouse import PyMouseEvent


class PositionClicker(PyMouseEvent):
    '''Abandon--for this thread listen on mouse click event real time, thus not controlable
    '''

    def __init__(self, messages=['']):
        '''print message in every click
        '''
        PyMouseEvent.__init__(self)
        self.messages = messages
        self.pos = 0
        self.lock = False

    def click(self, x, y, button, press):
        '''click event
        '''
        if self.lock is False:
            self.lock = True
            if self.messages[0] != '':  # message helper mode
                if self.pos >= len(self.messages):
                    self.stop()

                if button == 1:
                    if press:
                        choice = input(
                            'Mark for {0}? y/N'.format(self.messages[self.pos]))
                        if choice in ['y', 'Y']:
                            print(self.messages[self.pos], x, y)
                            self.pos += 1
                else:
                    self.stop()
            else:  # no message helper
                if button == 1:
                    if press:
                        print(x, y)
                else:
                    self.stop()
            self.lock = False


import pyautogui
from utils.imageGrab import grab_screen


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
        x1, y1, x2, y2 = [point_area[0][0], point_area[0]
                          [1], point_area[1][0], point_area[1][1]]
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
