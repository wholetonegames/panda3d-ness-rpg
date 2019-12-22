from direct.gui.OnscreenText import OnscreenText, TextNode
from direct.gui.DirectGui import (
    DGG,
    DirectFrame,
    DirectLabel,
    DirectRadioButton)
from w_i_menu import IMenu
import y_helpers


class OptionMenu(IMenu):
    def __init__(self):
        frame = DirectFrame(frameSize=(base.a2dLeft, base.a2dRight,
                                       base.a2dBottom, base.a2dTop),
                            frameColor=(0, 0, 0, 1.0))
        IMenu.__init__(self, frame=frame)
        self.menuVerticalChoicesList = [
            {"event": "Option-Items", "text": "Items"},
            # {"event": "Option-Equip", "text": "Equip"},
            # {"event": "Option-Magic", "text": "Magic"},
            {"event": "Option-Save", "text": "Save"},
            {"event": "Option-Config", "text": "Config"},
            {"event": "Back-Field", "text": "Back to Game"},
            {"event": "Option-Quit", "text": "Back to Start Menu"}]
        self.menuHorizontalChoices = [
            {"event": "Chara-Sub", "text": "*"},
            {"event": "Chara-Add", "text": "*"}]
        self.characterSheetList = []
        self.characterSheetIndex = 0
        for hero in base.gameData.hero_party:
            self.characterSheetList.append(hero)

        self.createVerticalButtons()
        self.addTitle()
        self.charaName = None
        self.statsSheet = None
        self.displayCharacterSheet(self.characterSheetIndex)

    def createButton(self, text, index, eventArgs):
        btn = DirectRadioButton(text=text.upper(),
                                text_align=TextNode.ALeft,
                                scale=0.05,
                                frameColor=(0, 0, 0, 0.0),
                                pos=(base.a2dLeft + 0.075, 0,
                                     (0.3 - (index * .15))),
                                variable=self.menuVerticalChoice,
                                value=[index],
                                text_fg=(1, 1, 1, 1),
                                command=self.menuVerticalEvent)

        self.menuVerticalButtons.append(btn)
        btn.reparentTo(self.frameMain)

    def addTitle(self):
        self.title = OnscreenText(
            'Character Stats', 1, 
            fg=(1, 0, 0, 1), 
            pos=(base.a2dLeft + 0.7, 0.8),
            font=base.font_title,
            align=TextNode.ALeft, 
            scale=.15, 
            mayChange=1)
        self.title.reparentTo(self.frameMain)

    def cancelCommand(self):
        base.messenger.send("Back-Field")

    def displayCharacterSheet(self, value):
        if self.charaName:
            self.charaName.detachNode()
            self.statsSheet.detachNode()
        self.characterSheetIndex += value
        self.characterSheetIndex = max(0, self.characterSheetIndex)
        self.characterSheetIndex = min(
            self.characterSheetIndex, len(self.characterSheetList) - 1)
        chara = self.characterSheetList[self.characterSheetIndex]
        self.charaName = DirectLabel(
            scale=0.12,
            text_align=TextNode.ALeft,
            pos=(base.a2dLeft + 0.7, 0, 0.5),
            pad=(0.5, 0.5),
            frameColor=(0, 0, 0, 0.0),
            text=chara['name'],
            text_fg=(1, 1, 1, 1))
        self.charaName.reparentTo(self.frameMain)

        self.statsSheet = DirectFrame(frameSize=(base.a2dLeft, base.a2dRight,
                                                 base.a2dBottom, base.a2dTop),
                                      frameColor=(0, 1, 0, 0))

        next_xp = y_helpers.get_experience_estimate(chara['level'] + 1)
        stats = [
            'Health Points: {} / {}'.format(chara['hp'], chara['max_hp']),
            'Level: {}'.format(chara['level']),
            '',
            'Attack: {}'.format(y_helpers.get_stat(chara['attack'])),
            'Defense: {}'.format(y_helpers.get_stat(chara['defense'])),
            'Speed: {}'.format(y_helpers.get_stat(chara['speed'])),
            '',
            'Experience Points: {}'.format(chara['xp']),
            'Points needed to level up: {}'.format(next_xp - chara['xp']),
        ]
        for stat in stats:
            self.add_stat(stat, stats.index(stat))
        self.statsSheet.reparentTo(self.frameMain)

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
