import pyautogui
import time
import random

pyautogui.PAUSE = 3
pyautogui.FAILSAFE = True

width, height = pyautogui.size()
# print(str(width))
# print(str(height))


def drawRct():
    for i in range(10):
        pyautogui.moveTo(300, 300, duration=0.25)
        pyautogui.moveTo(400, 300, duration=0.25)
        pyautogui.moveTo(400, 400, duration=0.25)
        pyautogui.moveTo(300, 400, duration=0.25)


def mouseScroll():
    time.sleep(5)
    for i in range(10):
        pyautogui.scroll(-200)
        time.sleep(2)


def getXy():
    try:
        while True:
            x, y = pyautogui.position()
            print(x, y)
    except KeyboardInterrupt:
        print('\nExit.')


def playVideo(x, y):
    for i in range(4):
        pyautogui.click(x, y)
        x = x+240
        playAndComment()


def playAndComment():
    time.sleep(random.randint(5, 15))
    pyautogui.scroll(-400)
    pyautogui.scroll(-400)
    pyautogui.click(200, 300)
    pyautogui.typewrite('very good!')
    pyautogui.click(900, 400)
    pyautogui.click(710, 16)


if __name__ == '__main__':
    time.sleep(5)
    pyautogui.scroll(-300)
    for i in range(9):
        print(str(i))
        time.sleep(random.randint(3, 5))
        # pyautogui.click(360,16)
        pyautogui.scroll(-300)
        time.sleep(random.randint(1, 5))
        playVideo(404, 330)
