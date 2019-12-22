from w_i_menu import IMenu
from direct.gui.DirectGui import (
    DirectFrame,
    DirectLabel,
    DirectRadioButton)
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
import y_helpers


class RPGFightInput(IMenu):
    def __init__(self, hero_party, enemy_party):
        self.hero_party = hero_party
        self.enemy_party = enemy_party
        frame = DirectFrame(frameColor=(0, 0, 0, 0.5),
                            borderWidth=(10, 10),
                            # (Left,Right,Bottom,Top)
                            frameSize=(-2, 2, -1, -0.45))
        IMenu.__init__(self, frame=frame)
        self.menuVerticalChoicesList = [
            {"event": "Fight-Attack", "text": "Attack"},
            # {"event": "Fight-Magic", "text": "Magic"},
            # {"event": "Fight-Items", "text": "Items"},
            {"event": "Fight-Defend", "text": "Defend"},
            {"event": "Fight-Flee", "text": "Flee"},
        ]
        self.createVerticalButtons()

    def playerInfo(self, heroIndex):
        yPos = 0.0
        for hero in self.hero_party:
            index = self.hero_party.index(hero)
            heroName = hero["name"].upper(
            ) if index == heroIndex else hero["name"]

            yPos = -0.55 - (index * .1)
            self.characterText(heroName, (-.5, yPos))
            self.characterText(
                "HP {}/{}".format(hero['hp'], hero['max_hp']), (-.1, yPos))
            # self.characterText(
            #     "MP {}/{}".format(hero['mp'], hero['maxmp']), (.5, yPos))

        # yPos2 = yPos - .2
        # for enemy in self.enemy_party:
        #     index = self.enemy_party.index(enemy)
        #     yPos = yPos2 - (index * .1)
        #     self.characterText(enemy["name"], (-.5, yPos))
        #     self.characterText(
        #         "HP {}/{}".format(enemy['hp'], enemy['max_hp']), (-.1, yPos))

    def characterText(self, text, pos):
        txt = OnscreenText(text=text,
                           pos=pos,
                           scale=0.075,
                           wordwrap=35,
                           mayChange=False,
                           align=TextNode.ALeft,
                           fg=(1, 1, 1, 1),
                           shadow=(0, 0, 0, 1),
                           shadowOffset=(0.05, 0.05))
        txt.reparentTo(self.frameMain)

    def createButton(self, text, index, eventArgs):
        btn = DirectRadioButton(text=text,
                                text_align=TextNode.ALeft,
                                scale=0.07,
                                frameColor=(0, 0, 0, 0.0),
                                pos=(base.a2dLeft + 0.2, 0,
                                     (-0.55 - (index * .15))),
                                variable=self.menuVerticalChoice,
                                value=[index],
                                text_fg=(1, 1, 1, 1),
                                command=self.menuVerticalEvent)
        self.menuVerticalButtons.append(btn)
        btn.reparentTo(self.frameMain)

    def menuVerticalEvent(self):
        event = self.menuVerticalChoicesList[self.menuVerticalChoice[0]]["event"]
        if event == 'Fight-Flee':
            base.fadeInOutSequence(base.messenger.send, event)
        else:
            base.messenger.send(event)

    def cancelCommand(self):
        pass
