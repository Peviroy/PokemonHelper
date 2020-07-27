import sys
import os

os.chdir(os.path.split(os.path.realpath(__file__))[0])
sys.path.append(os.path.abspath("."))

import time
import pytesseract
from pymouse import PyMouse
from PIL import Image

from positionDefiner import getPosData
from utils.imageGrab import grab_screen

POSITION_FILE = 'criPosition.json'
MOUSE = PyMouse()


def mouseClick(pos_x, pos_y, press_time=0.2):
    mousePress(press_time, pos_x, pos_y)


def mousePress(press_time, pos_x, pos_y):
    '''press mouse button for <press_time> seconds
    '''
    MOUSE.press(pos_x, pos_y)
    time.sleep(press_time)
    MOUSE.release(pos_x, pos_y)


def work_1(Load, A, GoDown, GoRight):
    '''first step: 同老爷爷对话， 并走至个体查询员跟前
    Requirement:
    ------------
        初始条件需要站立在老爷爷跟前(下方), 且面朝老爷爷
    Operation:
    ------------
        Load键读取存档
        A键Click八次
        GoDown键Press
        GoRight键Press
    '''
    mouseClick(*Load)
    time.sleep(0.3)

    for i in range(8):
        mouseClick(*A)
        time.sleep(0.7)

    mousePress(0.15, *GoDown)
    for i in range(10):  # 防止出现对讲机
        mouseClick(*A)
        time.sleep(0.1)
    mousePress(0.15, *GoDown)

    mousePress(0.1, *GoRight)

    for i in range(10):  # 防止出现对讲机
        mouseClick(*A)
        time.sleep(0.1)

    mousePress(0.6, *GoRight)


def work_2(A, B, Home, GoDown, GoRight, Speed):
    '''second step: 替换精灵
    Requirement:
    ------------
        Home键已经选择在精灵选项上
    Operation:
    ------------
        Home键
        A键进入精灵背包
        A键选择首位
        Speed调回原速
        GoDown选择换位
        Speed调回快速
        A键确定换位功能
        GoRight选择右首精灵
        A键完成换位
        B键退出精灵背包
        B键退出Home页
    '''
    mouseClick(*Home)
    time.sleep(0.3)

    mouseClick(*A)
    time.sleep(0.3)

    mouseClick(*A)
    time.sleep(0.3)

    mouseClick(*Speed)
    time.sleep(0.3)

    # mouseClick(press_time=0.02, *GoDown)
    mouseClick(*GoDown)
    time.sleep(0.3)

    mouseClick(*A)
    time.sleep(0.3)

    mouseClick(*GoDown)
    time.sleep(0.3)

    mouseClick(*Speed)
    time.sleep(0.3)

    mouseClick(*A)
    time.sleep(0.3)

    mouseClick(*B)
    time.sleep(0.3)

    mouseClick(*B)
    time.sleep(0.3)


def numberCapture(name, min_limit, pos1_x, pos1_y, pos2_x, pos2_y):
    count = 0  # if not captured, retry for 10; 确保截取到正确的图片。逻辑: 图片正确那么必有数字结果。要求：壁纸没有扰乱向
    while count <= 5:
        img = grab_screen(pos1_x, pos1_y, pos2_x, pos2_y)
        img.save(os.path.join('../screenshots', name + '.png'))
        img = Image.open(os.path.join('../screenshots', name + '.png'))
        number = pytesseract.image_to_string(
            img, lang="chi_sim", config='--psm 7 --oem 0 -c tessedit_char_whitelist=0123456789')
        try:  # 避免数字错乱以及空
            number = int(number)
            print(number)
            # 若一切正常，在此退出
            # if name == 'HP' and number == 31:   # 单个体择优
            # return 6
            if number == min_limit or number == min_limit + 1:
                return 1
            return 0
        except Exception:
            count += 1  # 若有异常，重复5次未果则退出
    print('not captured, skip this circle')
    return -1


def work_3(A, HP, WG, WF, SD, TG, TF):
    '''second step: 同个体员对话
    Requirement:
    ------------
        经由step1 step2
    Operation:
    ------------
        A键Click四次
        查询HP, WG, WF
        A键Click一次
        查询SD, TG, TF
        若成功那么返回True
    '''
    for i in range(4):
        mouseClick(*A)
        time.sleep(0.3)

    count = 0

    requirement = {'HP': [31, HP], 'WG': [31, WG], 'WF': [31, WF]}
    for item in requirement:
        count += numberCapture(item, requirement[item][0], requirement[item][1][0][0], requirement[item][1][0][1],
                               requirement[item][1][1][0], requirement[item][1][1][1])
    mouseClick(*A)
    time.sleep(0.3)

    requirement = {'SD': [31, SD], 'TG': [30, TG], 'TF': [30, TF]}
    for item in requirement:
        count += numberCapture(item, requirement[item][0], requirement[item][1][0][0], requirement[item][1][0][1],
                               requirement[item][1][1][0], requirement[item][1][1][1])

    time.sleep(0.3)

    if count >= 5:  # 6v
        return True
    return False


def work_4(Load, Save):
    '''重新载入，隔时间保存
    '''
    mouseClick(*Load)
    time.sleep(2)

    mouseClick(*Save)


def main_worker(pos_data):
    # position constant
    A = pos_data['button']['A']
    B = pos_data['button']['B']
    GoDown = pos_data['button']['GoDown']
    GoRight = pos_data['button']['GoRight']
    Load = pos_data['button']['Load']
    Save = pos_data['button']['Save']
    Home = pos_data['button']['Home']
    Speed = pos_data['button']['Speed']

    HP = pos_data['number']['HP']
    WG = pos_data['number']['WG']
    WF = pos_data['number']['WF']
    SD = pos_data['number']['SD']
    TG = pos_data['number']['TG']
    TF = pos_data['number']['TF']
    # work_2(A, B, Home, GoDown, GoRight, Speed)

    flag = False
    while True:
        mouseClick(*Save)  # 每20轮进行一次存档
        time.sleep(0.3)
        for i in range(20):
            print('|-------------------------|')
            work_1(Load, A, GoDown, GoRight)
            work_2(A, B, Home, GoDown, GoRight, Speed)
            flag = work_3(A, HP, WG, WF, SD, TG, TF)

            if flag is True:
                mouseClick(*Save)  # 每20轮进行一次存档
                time.sleep(0.3)
                exit()
        work_4(Load, Save)


def main():
    pos_data = getPosData()
    main_worker(pos_data)


if __name__ == "__main__":
    main()
