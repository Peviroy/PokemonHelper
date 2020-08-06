import os
import time
import pytesseract
import pyautogui
from PIL import Image

from utils.imageGrab import grab_screen


def mouseClick(pos_x, pos_y, press_time=0.2):
    mousePress(press_time, pos_x, pos_y)


def mousePress(press_time, pos_x, pos_y):
    '''press mouse button for <press_time> seconds
    '''
    pyautogui.mouseDown(pos_x, pos_y)
    time.sleep(press_time)
    pyautogui.mouseUp(pos_x, pos_y)


def keyClick(key, press_time=0.2):
    keyPress(press_time, key)


def keyPress(press_time, key):
    pyautogui.keyDown(key)
    time.sleep(press_time)
    pyautogui.keyUp(key)


class individuleOptimizer():
    '''[EGG] Pokémon individule value selector [个体值择优器]

        According to the principle of Pokémon incubating eggs, we simply make the process of
        egg inspection automatic through automated walking and image recgonization;

        Requirement:
            Initially, player must stand below EggGrandpa facing him;
            Then this program will execute four steps:
            loop
                1. dialogue with EggGrandpa, and walk down, then walk right until meet IndividuleConsultant
                2. exchange your first pokemon with the egg
                3. consult the individule value
                if individule value doesnt meet the standard, then continue loop(with save and load)
    '''

    def __init__(self, pos_data: dict, how_many_v=6, egg_pos=1, platform='mobile'):
        self.pos_data = pos_data
        self.how_mamy_v = how_many_v
        self.egg_pos = egg_pos
        if platform == 'mobile':
            self.Click = mouseClick
            self.Press = mousePress
        elif platform == 'pc':
            self.Click = keyClick
            self.Press = keyPress
        else:
            raise Exception('No such platform')

    def _step1(self):
        '''
        Operation:
        ------------
            A click for eight times
            GoDown Press
            GoRight Press
        '''
        A = self.pos_data['button']['A']
        GoDown = self.pos_data['button']['GoDown']
        GoRight = self.pos_data['button']['GoRight']

        # A click for eight times
        for i in range(8):
            self.Click(*A)
            time.sleep(0.7)

        # GoDown Press
        self.Press(0.15, *GoDown)
        for i in range(10):  # avoid interphone
            self.Click(*A)
            time.sleep(0.1)
        self.Press(0.15, *GoDown)

        # GoRight Press
        self.Press(1, *GoRight)
        for i in range(10):   # avoid interphone
            self.Click(*A)
            time.sleep(0.1)
        self.Press(2, *GoRight)

    def _step2(self):
        '''
        Operation:
        ------------
            Home | into home page
            A | into pokemon bag
            A | into pokemon operation page
            Speed | change game acceleration into normal
            GoDown | select the exchange function
            A | into position exchanging mode
            GoDown | select the egg 
            Speed | change game acceleration
            A | finish position exchange
            B | exit pokemon bag
            B | exit home page
        '''
        A = self.pos_data['button']['A']
        B = self.pos_data['button']['B']
        GoDown = self.pos_data['button']['GoDown']
        Home = self.pos_data['button']['Home']
        Speed = self.pos_data['button']['Speed']

        # into home page
        self.Click(*Home)
        time.sleep(0.3)

        # into pokemon bag
        self.Click(*A)
        time.sleep(0.3)

        # into pokemon operation page
        self.Click(*A)
        time.sleep(0.3)

        # change game acceleration into normal
        self.Click(*Speed)
        time.sleep(0.3)

        # select the exchange function
        self.Click(*GoDown)
        time.sleep(0.3)

        # into position exchanging mode
        self.Click(*A)
        time.sleep(0.3)

        # select the egg
        for i in range(self.egg_pos):
            self.Click(*GoDown)
            time.sleep(0.3)

        # change game acceleration
        self.Click(*Speed)
        time.sleep(0.3)

        # finish position exchange
        self.Click(*A)
        time.sleep(0.3)

        # exit pokemon bag
        self.Click(*B)
        time.sleep(0.3)

        # exit home page
        self.Click(*B)
        time.sleep(0.3)

    @staticmethod
    def _numberCapture(name, min_limit, pos1_x, pos1_y, pos2_x, pos2_y):
        # if not captured, retry for 5 times to make sure: 1.screenshot is right; number is recgonized correctly
        for count in range(5):
            img = grab_screen(pos1_x, pos1_y, pos2_x, pos2_y)
            img.save(os.path.join('../screenshots', name + '.png'))
            img = Image.open(os.path.join('../screenshots', name + '.png'))

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

    def _step3(self):
        '''
        Operation:
        ------------
            A for 4 times
            consult HP, WG, WF
            A for 1 time
            consult SD, TG, TF
        '''
        A = self.pos_data['button']['A']
        HP = self.pos_data['number']['HP']
        WG = self.pos_data['number']['WG']
        WF = self.pos_data['number']['WF']
        SD = self.pos_data['number']['SD']
        TG = self.pos_data['number']['TG']
        TF = self.pos_data['number']['TF']

        for i in range(4):
            self.Click(*A)
            time.sleep(0.3)

        count = 0

        requirement = {'HP': [31, HP], 'WG': [31, WG], 'WF': [31, WF]}
        for item in requirement:
            count += self._numberCapture(item, requirement[item][0], requirement[item][1][0][0], requirement[item][1][0][1],
                                         requirement[item][1][1][0], requirement[item][1][1][1])
        self.Click(*A)
        time.sleep(0.3)

        requirement = {'SD': [31, SD], 'TG': [30, TG], 'TF': [30, TF]}
        for item in requirement:
            count += self._numberCapture(item, requirement[item][0], requirement[item][1][0][0], requirement[item][1][0][1],
                                         requirement[item][1][1][0], requirement[item][1][1][1])

        time.sleep(0.3)

        if count >= self.how_mamy_v:
            return True
        return False

    def run(self):
        pyautogui.alert(
            'Script is about to start. Adjust the speed to 16 times and face EggGrandpa')
        time.sleep(5)
        SAVE = self.pos_data['button']['Save']
        LOAD = self.pos_data['button']['Load']

        self.Click(*SAVE)  # save archive for every 20 circles
        time.sleep(0.1)
        epoch = 1
        while True:
            for i in range(20):
                print('|-------------EPOCH:{0}--------------|'.format(epoch))
                epoch += 1

                self.Click(*LOAD)
                time.sleep(0.1)

                self._step1()
                self._step2()

                if self._step3() is True:  # meet requirement; exit
                    self.Click(*SAVE)
                    time.sleep(0.1)
                    exit()

            self.Click(*LOAD)  # load again; change to another start time
            time.sleep(2)
            self.Click(*SAVE)
