from direct.gui.OnscreenText import OnscreenText, TextNode
from direct.gui.DirectGui import (
    DGG,
    DirectFrame,
    DirectLabel,
    DirectRadioButton)
from w_i_menu import IMenu
import y_helpers


class MagicMenu(IMenu):
    def __init__(self):
        frame = DirectFrame(frameSize=(base.a2dLeft, base.a2dRight,
                                       base.a2dBottom, base.a2dTop),
                            frameColor=(0, 0, 0, 1.0))
        IMenu.__init__(self, frame=frame)
        self.menuVerticalChoicesList = []
        self.menuHorizontalChoices = [
            {"event": "Chara-Sub", "text": "*"},
            {"event": "Chara-Add", "text": "*"}
        ]
        self.characterSheetList = []
        self.characterSheetIndex = 0
        self.statsSheet = None
        for hero in base.gameData.hero_party:
            self.characterSheetList.append(hero)

        self.addTitle()
        self.characterSheet = None
        self.displayCharacterSheet(self.characterSheetIndex)

    def createButton(self, text, index, eventArgs):
        btn = DirectRadioButton(text=text,
                                text_align=TextNode.ALeft,
                                scale=0.05,
                                frameColor=(0, 0, 0, 0.0),
                                pos=(base.a2dLeft + 0.075, 0,
                                     (0.3 - (index * .06))),
                                variable=self.menuVerticalChoice,
                                value=[index],
                                text_fg=(1, 1, 1, 1),
                                command=self.menuVerticalEvent)

        self.menuVerticalButtons.append(btn)
        btn.reparentTo(self.frameMain)

    def addTitle(self):
        self.title = OnscreenText(
            'Magic Spells', 1, 
            fg=(1, 0, 0, 1), 
            pos=(base.a2dLeft + 0.7, 0.8),
            font=base.font_title,
            align=TextNode.ALeft, 
            scale=.15, 
            mayChange=1)
        self.title.reparentTo(self.frameMain)

    def cancelCommand(self):
        base.messenger.send("Back-Option")

    def updateInventory(self):
        if self.menuVerticalButtons:
            for btn in self.menuVerticalButtons:
                btn.removeNode()
        self.menuVerticalChoicesList = []
        self.menuVerticalChoice = [0]
        chara = self.characterSheetList[self.characterSheetIndex]
        for magic in chara['magic']:
            magicInfo = y_helpers.find_by_id(magic, base.magicData.items)
            # need events to use items?
            self.menuVerticalChoicesList.append(
                {"event": "*",   "text": magicInfo['name']})
        self.menuVerticalChoicesList.append(
            {"event": "Back-Option",   "text": "Back to Menu"})

        self.menuVerticalButtons = []
        self.createVerticalButtons()

        self.magic_stats(0)

    def displayCharacterSheet(self, value):
        if self.characterSheet:
            self.characterSheet.detachNode()
        self.characterSheetIndex += value
        self.characterSheetIndex = max(0, self.characterSheetIndex)
        self.characterSheetIndex = min(
            self.characterSheetIndex, len(self.characterSheetList) - 1)
        chara = self.characterSheetList[self.characterSheetIndex]
        self.characterSheet = DirectLabel(
            scale=0.12,
            text_align=TextNode.ALeft,
            pos=(base.a2dLeft + 0.7, 0, 0.5),
            pad=(0.5, 0.5),
            frameColor=(0, 0, 0, 0.0),
            text=chara['name'],
            text_fg=(1, 1, 1, 1))
        self.characterSheet.reparentTo(self.frameMain)

        self.updateInventory()

    def updateCheckbuttons(self):
        for btn in self.menuVerticalButtons:
            index = self.menuVerticalButtons.index(btn)
            isPressed = index == self.menuVerticalChoice[0]
            btn["indicatorValue"] = isPressed
            btn.setIndicatorValue()

            chara = self.characterSheetList[self.characterSheetIndex]
            if self.menuVerticalChoice[0] < len(chara['magic']):
                self.magic_stats(self.menuVerticalChoice[0])

        for btn in self.menuHorizontalButtons:
            index = self.menuHorizontalButtons.index(btn)
            isPressed = index == self.menuHorizontalChoice[0]
            btn["indicatorValue"] = isPressed
            btn.setIndicatorValue()

    def magic_stats(self, index):
        if self.statsSheet:
            self.statsSheet.detachNode()
        self.statsSheet = DirectFrame(frameSize=(base.a2dLeft, base.a2dRight,
                                                 base.a2dBottom, base.a2dTop),
                                      frameColor=(0, 1, 0, 0))
        chara = self.characterSheetList[self.characterSheetIndex]
        magic = y_helpers.find_by_id(
            chara['magic'][index], base.magicData.items)
        stats = [
            '{}'.format(magic['name']),
            '',
            'Description: {}'.format(magic['description']),
            'Costs: {}'.format(self.write_costs(magic['costs'])),
            'Targets: {}'.format(magic['target']),
        ]
        for stat in stats:
            self.add_stat(stat, stats.index(stat))
        self.statsSheet.reparentTo(self.frameMain)

    def write_costs(self, costs):
        output = ''
        for key in costs:
            output += '({} x {}) '.format(key, costs[key])
        return output

    def add_stat(self, text, index):
        stat = DirectLabel(
            scale=0.07,
            text_align=TextNode.ALeft,
            pos=(base.a2dLeft + 0.7, 0, (0.3 - (index * .1))),
            pad=(0.5, 0.5),
            frameColor=(0, 0, 0, 0.0),
            text=text,
            text_fg=(1, 1, 1, 1))
        stat.reparentTo(self.statsSheet)
