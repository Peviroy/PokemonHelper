import time
import pyautogui


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


def alert(msg):
    pyautogui.alert(msg)
