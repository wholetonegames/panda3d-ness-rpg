import os
from direct.gui.OnscreenText import OnscreenText, TextNode
from direct.gui.DirectGui import (
    DGG,
    DirectFrame,
    DirectLabel,
    DirectRadioButton)
from w_i_menu import IMenu


class SaveMenu(IMenu):
    def __init__(self):
        frame = DirectFrame(frameSize=(base.a2dLeft, base.a2dRight,
                                       base.a2dBottom, base.a2dTop),
                            frameColor=(0, 0, 0, 1.0))
        IMenu.__init__(self, frame=frame)
        self.menuVerticalChoicesList = []
        self.updateSaveSlots()
        self.createVerticalButtons()
        self.addTitle()
        self.hasLoaded = True

    def createButton(self, text, index, eventArgs):
        btn = DirectRadioButton(text=text,
                                text_align=TextNode.ALeft,
                                scale=0.07,
                                frameColor=(0, 0, 0, 0.0),
                                pos=(base.a2dLeft + 0.7, 0,
                                     (0.5 - (index * .25))),
                                variable=self.menuVerticalChoice,
                                value=[index],
                                text_fg=(1, 1, 1, 1),
                                command=self.menuVerticalEvent)

        self.menuVerticalButtons.append(btn)
        btn.reparentTo(self.frameMain)

    def addTitle(self):
        self.title = OnscreenText(
            'Save Game', 1, 
            fg=(1, 0, 0, 1), 
            pos=(base.a2dLeft + 0.7, 0.8),
            font=base.font_title,
            align=TextNode.ALeft, 
            scale=.15, 
            mayChange=1)
        self.title.reparentTo(self.frameMain)

    def cancelCommand(self):
        base.messenger.send("Back-Option")

    def menuVerticalEvent(self):
        if not self.hasLoaded:
            return

        eventName = self.menuVerticalChoicesList[self.menuVerticalChoice[0]]["event"]
        if eventName == "Back-Option":
            base.messenger.send("Back-Option")
            return

        base.gameData.selectedSaveSlot = eventName
        base.gameData.saveGame()
        for btn in self.menuVerticalButtons:
            index = self.menuVerticalButtons.index(btn)
            if index == self.menuVerticalChoice[0]:
                slot = base.gameData.saveSlotNumbers[index]
                filename = os.path.dirname(
                    base.gameData.filepath) + "/slot{}.txt".format(slot)
                mapName, totalTime = base.gameData.getSaveFileInfo(filename)
                btn['text'] = "{} {}".format(mapName, totalTime)

    def updateSaveSlots(self):
        self.menuVerticalChoicesList = []
        for slot in base.gameData.saveSlotNumbers:
            filename = os.path.dirname(
                base.gameData.filepath) + "/slot{}.txt".format(slot)
            if os.path.isfile(filename):
                mapName, totalTime = base.gameData.getSaveFileInfo(filename)
                self.menuVerticalChoicesList.append(
                    {"event": slot,  "text": "{} - total time played: {}".format(mapName, totalTime)})
            else:
                base.gameData.selectedSaveSlot = slot
                base.gameData.saveGame()
                self.menuVerticalChoicesList.append(
                    {"event": slot,  "text": "EMPTY"})

        self.menuVerticalChoicesList.append(
            {"event": "Back-Option",   "text": "Back to Menu"})
