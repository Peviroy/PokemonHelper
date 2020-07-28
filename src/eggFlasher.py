import pyautogui
import random
import time

from utils.imageGrab import grab_screen


def mouseClick(pos_x, pos_y, press_time=0.2):
    mousePress(press_time, pos_x, pos_y)


def mousePress(press_time, pos_x, pos_y):
    '''press mouse button for <press_time> seconds
    '''
    pyautogui.mouseDown(pos_x, pos_y)
    time.sleep(press_time)
    pyautogui.mouseUp(pos_x, pos_y)


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

    def __init__(self, pos_data):
        self.pos_data = pos_data

    def _step1(self):
        '''
        Operation:
            A | into pokemon hatched point
            Capture pixle
        '''
        A = self.pos_data['button']['A']
        FLASH_POINT = self.pos_data['flash']['Flash']

        mouseClick(*A)
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

        mouseClick(*A)
        time.sleep(0.9)
        this_pixle = getPixle(*FLASH_POINT)
        print('A:', pixle)
        print('B:', this_pixle)

        if abs(pixle[0] - this_pixle[0]) >= 10 or abs(pixle[1] - this_pixle[1]) >= 10 or abs(pixle[2] - this_pixle[2]) >= 10:
            return True
        return False

    def run(self):
        pyautogui.alert(
            'Script is about to start. Adjust the speed to 16 times and save archive at the moment of "hamph"')

        SAVE = self.pos_data['button']['Save']
        LOAD = self.pos_data['button']['Load']

        mouseClick(*SAVE)  # save archive for every 20 circles
        time.sleep(0.2)
        non_flash_pixle = self._step1()
        epoch = 1
        while True:
            for i in range(20):
                print('|-------------EPOCH:{0}--------------|'.format(epoch))
                epoch += 1

                mouseClick(*LOAD)  # load
                time.sleep(int((random.random() * 51 + 100) / 1000))   # delay

                if self._step2(non_flash_pixle) is True:  # compare pixle
                    mouseClick(*SAVE)
                    time.sleep(0.1)
                    print('Egg flashed !!! ')
                    exit()

            mouseClick(*LOAD)  # load again; change to another start time
            time.sleep(2)
            mouseClick(*SAVE)
