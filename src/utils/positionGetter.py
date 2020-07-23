from pymouse import PyMouseEvent


class PositionClicker(PyMouseEvent):
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


if __name__ == "__main__":
    pC = PositionClicker(['HO', 'HI', 'HP'])
    pC.run()
