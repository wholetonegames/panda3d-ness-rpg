import abc
from direct.gui.DirectGui import DirectFrame


class IMenu(metaclass=abc.ABCMeta):
    def __init__(self, frame=None):
        self.hasLoaded = False
        self.menuVerticalChoicesList = [
            {"event": "Example-Event", "text": "Override this"}]
        self.menuVerticalChoice = [0]
        self.menuHorizontalChoices = [
            {"event": "Example-Event", "text": "Override this"}]
        self.menuHorizontalChoice = [0]
        self.menuVerticalButtons = []
        self.menuHorizontalButtons = []
        self.isButtonUp = True
        self.init_frame(frame)

    def init_frame(self, frame):
        if frame:
            self.frameMain = frame
        else:
            self.frameMain = DirectFrame(
                frameSize=(base.a2dLeft, base.a2dRight,
                           base.a2dBottom, base.a2dTop),
                frameColor=(0, 0, 0, 0.0))

    def show(self):
        self.frameMain.show()

    def hide(self):
        self.frameMain.hide()

    def quit(self):
        self.frameMain.removeNode()

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
            self.navigateChoice(-1, self.menuHorizontalChoice,
                                self.menuHorizontalChoices)
            self.isButtonUp = False
            self.menuHorizontalEvent()
        elif base.directionMap["right"]:
            self.navigateChoice(1, self.menuHorizontalChoice,
                                self.menuHorizontalChoices)
            self.isButtonUp = False
            self.menuHorizontalEvent()

        base.resetButtons()
        return task.cont

    def navigateChoice(self, value, choice, choiceList):
        choice[0] += value

        if choice[0] < 0:
            choice[0] = len(choiceList) - 1
        elif choice[0] > len(choiceList) - 1:
            choice[0] = 0

        self.updateCheckbuttons()

    def updateCheckbuttons(self):
        for btn in self.menuVerticalButtons:
            index = self.menuVerticalButtons.index(btn)
            isPressed = index == self.menuVerticalChoice[0]
            btn["indicatorValue"] = isPressed
            btn.setIndicatorValue()

        for btn in self.menuHorizontalButtons:
            index = self.menuHorizontalButtons.index(btn)
            isPressed = index == self.menuHorizontalChoice[0]
            btn["indicatorValue"] = isPressed
            btn.setIndicatorValue()

    def menuVerticalEvent(self):
        base.messenger.send(
            self.menuVerticalChoicesList[self.menuVerticalChoice[0]]["event"])

    def menuHorizontalEvent(self):
        base.messenger.send(
            self.menuHorizontalChoices[self.menuHorizontalChoice[0]]["event"])

    def createVerticalButtons(self):
        for btn in self.menuVerticalChoicesList:
            index = self.menuVerticalChoicesList.index(btn)
            self.createButton(
                btn['text'],
                index,
                [btn['event']])

    @abc.abstractmethod
    def createButton(self, text, index, eventArgs):
        raise NotImplementedError('subclass must define this method')

    @abc.abstractmethod
    def cancelCommand(self):
        raise NotImplementedError('subclass must define this method')
