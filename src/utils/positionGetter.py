import os
from pymouse import PyMouseEvent


class PositionClicker(PyMouseEvent):
    def __init__(self, messages=['']):
        '''print message in every click
        '''
        PyMouseEvent.__init__(self)
        self.messages = messages
        self.pos = 0

    def click(self, x, y, button, press):
        if self.messages[0] != '' and self.pos >= len(self.messages):
            self.stop()

        if button == 1:
            if press:
                print(self.messages[self.pos], x, y)
                self.pos += 1
        else:  # Exit if any other mouse button used
            self.stop()


class mouseInterupter(PyMouseEvent):
    def __init__(self, messages=['']):
        PyMouseEvent.__init__(self)

    def click(self, x, y, button, press):
        if button == 2:
            if press:
                self.stop()
                os._exit(0)


if __name__ == "__main__":
    # pC = PositionClicker()
    # pC.run()
    mI = mouseInterupter()
    mI.run()
