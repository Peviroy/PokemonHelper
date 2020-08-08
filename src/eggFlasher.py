import random
import time

from utils.imageGrab import grab_screen
from utils.autoKeyMouse import mouseClick, mousePress, keyClick, keyPress, alert


def getPixle(pos_x, pos_y):
    flag = True
    pixle_corrent = None
    while flag:
        pixle_corrent = grab_screen(
            pos_x, pos_y, pos_x + 1, pos_y + 1).getdata()[0]
        for _ in range(3):
            # if correspond 3 times, we suppose it's the correct pixle
            if grab_screen(pos_x, pos_y, pos_x + 1, pos_y + 1).getdata()[0] == pixle_corrent:
                flag = False
            else:  # if not correspond, continue loop
                flag = True
                break
    return pixle_corrent


class eggFlasher():
    '''Pokémon egg flasher [蛋闪确定器]

        According to the principle of Pokémon egg flash, we simply make the process of
        egg flash inspection automatic through automated A and pixle comparation;

        Requirement:
            Initially, the egg should be about to hatch, in other word, at the point of 'humph~'
            Then this program will execute four steps:
            1. click A, after egg hatched, capture non-flash pixle color
            loop True
                loop for 20
                    2. load, delay, A, compare
                if not flash, then continue loop(with save and load)
    '''

    def __init__(self, pos_data, platform):
        self.pos_data = pos_data
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
            A | into pokemon hatched point
            Capture pixle
        '''
        A = self.pos_data['button']['A']
        FLASH_POINT = self.pos_data['flash']['Flash']

        self.Click(*A)
        time.sleep(0.9)

        return getPixle(*FLASH_POINT)

    def _step2(self, pixle):
        '''
        Operation:
            A | into pokemon hatched point
            Capture pixle
            Compare pixle
        '''
        A = self.pos_data['button']['A']
        FLASH_POINT = self.pos_data['flash']['Flash']

        self.Click(*A)
        time.sleep(1.4)
        this_pixle = getPixle(*FLASH_POINT)
        print('A:', pixle)
        print('B:', this_pixle)

        if abs(pixle[0] - this_pixle[0]) >= 3 or abs(pixle[1] - this_pixle[1]) >= 3 or abs(pixle[2] - this_pixle[2]) >= 3:
            return True
        return False

    def run(self):
        alert('Script is about to start. Adjust the speed to more than 10 times and save archive at the moment of "hamph"')
        time.sleep(5)

        SAVE = self.pos_data['button']['Save']
        LOAD = self.pos_data['button']['Load']

        self.Click(*SAVE)  # save archive for every 20 circles
        time.sleep(0.2)
        non_flash_pixle = self._step1()
        epoch = 1
        while True:
            for i in range(20):
                print('|-------------EPOCH:{0}--------------|'.format(epoch))
                epoch += 1

                self.Click(*LOAD)  # load
                time.sleep(int((random.random() * 51 + 100) / 1000))   # delay

                if self._step2(non_flash_pixle) is True:  # compare pixle
                    self.Click(*SAVE)
                    time.sleep(0.1)
                    print('Egg flashed !!! ')
                    exit()

            self.Click(*LOAD)  # load again; change to another start time
            time.sleep(2)
            self.Click(*SAVE)
