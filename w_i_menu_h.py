from w_i_menu import IMenu


class IMenuHorizontal(IMenu):
    def __init__(self, col_height, frame):
        self.COLUMN_HEIGHT = col_height
        IMenu.__init__(self, frame=frame)

    def readKeys(self, task):
        keysPressed = sum(base.directionMap.values())

        if keysPressed == 0:
            self.isButtonUp = True

            if base.commandMap["confirm"]:
                self.menuVerticalEvent()
                base.messenger.send("playConfirm")
            elif base.commandMap["cancel"]:
                self.cancelCommand()
                base.messenger.send("playCancel")

            base.resetButtons()
            return task.cont

        if not self.isButtonUp:
            return task.cont

        if base.directionMap["up"]:
            self.navigateChoice(-1, self.menuVerticalChoice,
                                self.menuVerticalChoicesList)
            self.isButtonUp = False
        elif base.directionMap["down"]:
            self.navigateChoice(1, self.menuVerticalChoice,
                                self.menuVerticalChoicesList)
            self.isButtonUp = False
        elif base.directionMap["left"]:
            self.navigateChoice(-self.COLUMN_HEIGHT, self.menuVerticalChoice,
                                self.menuVerticalChoicesList)
            self.isButtonUp = False
            self.menuHorizontalEvent()
        elif base.directionMap["right"]:
            self.navigateChoice(self.COLUMN_HEIGHT, self.menuVerticalChoice,
                                self.menuVerticalChoicesList)
            self.isButtonUp = False
            self.menuHorizontalEvent()

        base.resetButtons()
        return task.cont

    def navigateChoice(self, value, choice, choiceList):
        choice[0] += value
        lc = len(choiceList)
        if choice[0] < 0:
            c = (lc// self.COLUMN_HEIGHT) * self.COLUMN_HEIGHT
            p = c + self.COLUMN_HEIGHT + choice[0]
            choice[0] = min(p, lc - 1)
        elif choice[0] > lc - 1:
            choice[0] = choice[0] % self.COLUMN_HEIGHT

        self.updateCheckbuttons()
