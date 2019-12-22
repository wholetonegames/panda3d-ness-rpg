from direct.gui.OnscreenText import OnscreenText, TextNode
from direct.gui.DirectGui import (
    DGG,
    DirectFrame,
    DirectLabel,
    DirectRadioButton)
from w_i_menu import IMenu


class ConfigMenu(IMenu):
    def __init__(self):
        frame = DirectFrame(frameSize=(base.a2dLeft, base.a2dRight,
                                       base.a2dBottom, base.a2dTop),
                            frameColor=(0, 0, 0, 1.0))
        IMenu.__init__(self, frame=frame)
        self.menuVerticalChoicesList = [
            {"event": "*", "text": "Text Display Time"},
            {"event": "*", "text": "Sound Effects Volume Level"},
            {"event": "*", "text": "Music Volume Level"},
            {"event": "Back-Option", "text": "Back to Menu"}
        ]
        self.menuHorizontalChoices = [
            {"event": "Chara-Sub", "text": "*"},
            {"event": "Chara-Add", "text": "*"}
        ]
        self.statsSheet = None
        self.createVerticalButtons()
        self.addTitle()
        self.config_stats()

    def createButton(self, text, index, eventArgs):
        btn = DirectRadioButton(text=text,
                                text_align=TextNode.ALeft,
                                scale=0.05,
                                frameColor=(0, 0, 0, 0.0),
                                pos=(base.a2dLeft + 0.7, 0,
                                     (0.5 - (index * .15))),
                                variable=self.menuVerticalChoice,
                                value=[index],
                                text_fg=(1, 1, 1, 1),
                                command=self.menuVerticalEvent)

        self.menuVerticalButtons.append(btn)
        btn.reparentTo(self.frameMain)

    def addTitle(self):
        self.title = OnscreenText(
            'Configurations', 1, 
            fg=(1, 0, 0, 1), 
            pos=(base.a2dLeft + 0.7, 0.8),
            font=base.font_title,
            align=TextNode.ALeft, 
            scale=.15, 
            mayChange=1)
        self.title.reparentTo(self.frameMain)

    def cancelCommand(self):
        base.messenger.send("Back-Option")

    def change_config(self, value):
        index = self.menuVerticalChoice[0]
        stats = [
            self.change_text_display_time,
            self.change_sfx_vol,
            self.change_bgm_vol,
        ]
        if index < len(stats):
            stats[index](value)
            self.config_stats()

    def change_text_display_time(self, value):
        payload = base.gameData.textDisplayTime + (value * 0.5)
        payload = max(payload, 0.5)
        payload = min(payload, 10.0)
        base.gameData.textDisplayTime = payload

    def change_bgm_vol(self, value):
        payload = base.gameData.bgm_vol + (value * 0.1)
        payload = max(payload, 0.0)
        payload = min(payload, 1.0)
        base.gameData.bgm_vol = payload
        # send update by event later

    def change_sfx_vol(self, value):
        payload = base.gameData.sfx_vol + (value * 0.1)
        payload = max(payload, 0.0)
        payload = min(payload, 1.0)
        base.gameData.sfx_vol = payload
        # send update by event later

    def config_stats(self):
        if self.statsSheet:
            self.statsSheet.detachNode()
        self.statsSheet = DirectFrame(frameSize=(base.a2dLeft, base.a2dRight,
                                                 base.a2dBottom, base.a2dTop),
                                      frameColor=(0, 1, 0, 0))
        stats = [
            '{} seconds'.format(base.gameData.textDisplayTime),
            '{} %'.format(int(base.gameData.sfx_vol * 100)),
            '{} %'.format(int(base.gameData.bgm_vol * 100)),
        ]
        i = 0
        for stat in stats:
            self.add_stat(stat, i)
            i += 1
        self.statsSheet.reparentTo(self.frameMain)

    def add_stat(self, text, index):
        stat = DirectLabel(
            scale=0.05,
            text_align=TextNode.ALeft,
            pos=(0, 0, (0.5 - (index * .15))),
            pad=(0.5, 0.5),
            frameColor=(0, 0, 0, 0.0),
            text=text,
            text_fg=(1, 1, 1, 1))
        stat.reparentTo(self.statsSheet)

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
            self.menuHorizontalChoice[0] = 0
            self.isButtonUp = False
            self.menuHorizontalEvent()
        elif base.directionMap["right"]:
            self.menuHorizontalChoice[0] = 1
            self.isButtonUp = False
            self.menuHorizontalEvent()

        base.resetButtons()
        return task.cont
