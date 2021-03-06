"""
@Author: peviroy
@Last Modified by: peviroy
@Last Modified time: 2020-09-23

@Note: Script for choosing egg with desired Individule Values
"""
import os
import time
import yaml
import pytesseract
from PIL import Image

from utils.imageGrab import grab_screen
from utils.autoKeyMouse import keyClick, keyPress, mouseClick, mousePress, alert


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
        elif platform == 'desktop':
            self.Click = keyClick
            self.Press = keyPress
        else:
            raise Exception('No such platform')
        self.user_config = yaml.full_load(open('../userCfg.yaml'))

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
            time.sleep(0.6)

        # GoDown Press
        self.Press(0.1, *GoDown)
        for i in range(8):  # avoid interphone
            self.Click(*A)
            time.sleep(0.05)
        self.Press(0.1, *GoDown)

        # GoRight Press
        self.Press(0.2, *GoRight)
        for i in range(8):   # avoid interphone
            self.Click(*A)
            time.sleep(0.05)
        self.Press(1.3, *GoRight)

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
        time.sleep(0.2)

        # into pokemon bag
        self.Click(*A)
        time.sleep(0.2)

        # into pokemon operation page
        self.Click(*A)
        time.sleep(0.2)

        # change game acceleration into normal
        self.Click(*Speed)
        time.sleep(0.2)

        # select the exchange function
        self.Click(*GoDown)
        time.sleep(0.2)

        # into position exchanging mode
        self.Click(*A)
        time.sleep(0.2)

        # select the egg
        for i in range(self.egg_pos):
            self.Click(*GoDown)
            time.sleep(0.2)

        # change game acceleration
        self.Click(*Speed)
        time.sleep(0.2)

        # finish position exchange
        self.Click(*A)
        time.sleep(0.2)

        # exit pokemon bag
        self.Click(*B)
        time.sleep(0.2)

        # exit home page
        self.Click(*B)
        time.sleep(0.2)

    def _numberCapture(self, name, min_limit, pos1_x, pos1_y, pos2_x, pos2_y):
        # if not captured, retry for 5 times to make sure: 1.screenshot is right; indivalue is recgonized correctly
        for count in range(5):
            img = grab_screen(pos1_x, pos1_y, pos2_x, pos2_y)
            img.save(os.path.join('../screenshots', name + '.png'))
            img = Image.open(os.path.join('../screenshots', name + '.png'))

            indivalue = pytesseract.image_to_string(
                img, lang=self.user_config.get('pytesseract').get('lang'), config=self.user_config.get('pytesseract').get('config'))

            try:
                indivalue = int(indivalue)
                print(indivalue)
                # if name == 'HP' and indivalue == 31:   # 单个体择优
                # return 6
                if indivalue >= min_limit:
                    return 1
                return 0
            except Exception:
                continue

        print('not captured, skip this circle')
        return 0

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
        HP = self.pos_data['indivalue']['HP']
        WG = self.pos_data['indivalue']['WG']
        WF = self.pos_data['indivalue']['WF']
        SD = self.pos_data['indivalue']['SD']
        TG = self.pos_data['indivalue']['TG']
        TF = self.pos_data['indivalue']['TF']

        HP_value = self.user_config.get('indiValue').get('HP')
        WG_value = self.user_config.get('indiValue').get('WG')
        WF_value = self.user_config.get('indiValue').get('WF')
        SD_value = self.user_config.get('indiValue').get('SD')
        TG_value = self.user_config.get('indiValue').get('TG')
        TF_value = self.user_config.get('indiValue').get('TF')

        for i in range(4):
            self.Click(*A)
            time.sleep(0.3)

        count = 0

        requirement = {'_HP': [HP_value, HP],
                       '_WG': [WG_value, WG],
                       '_WF': [WF_value, WF]}
        for item in requirement:
            count += self._numberCapture(item, requirement[item][0], requirement[item][1][0][0], requirement[item][1][0][1],
                                         requirement[item][1][1][0], requirement[item][1][1][1])
        self.Click(*A)
        time.sleep(0.3)

        requirement = {'_SD': [SD_value, SD],
                       '_TG': [TG_value, TG],
                       '_TF': [TF_value, TF]}
        for item in requirement:
            count += self._numberCapture(item, requirement[item][0], requirement[item][1][0][0], requirement[item][1][0][1],
                                         requirement[item][1][1][0], requirement[item][1][1][1])

        time.sleep(0.3)

        if count >= self.how_mamy_v:
            return True
        return False

    def run(self):
        alert('Script is about to start. Adjust the speed to more than 10 times and face EggGrandpa')
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
