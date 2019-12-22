from w_i_menu_h import IMenuHorizontal
from direct.gui.DirectGui import (
    DirectFrame,
    DirectLabel,
    DirectRadioButton)
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
import y_helpers


class RPGFightTarget(IMenuHorizontal):
    def __init__(self, enemy_party):
        self.COLUMN_HEIGHT = 3
        self.enemy_party = enemy_party
        frame = DirectFrame(frameColor=(0, 0, 0, 0.5),
                            borderWidth=(10, 10),
                            # (Left,Right,Bottom,Top)
                            frameSize=(-2, 2, -1, -0.45))
        IMenuHorizontal.__init__(self, self.COLUMN_HEIGHT, frame=frame)
        self.menuVerticalChoicesList = []
        for enemy in self.enemy_party:
            if y_helpers.is_character_KOed(enemy):
                continue
            index = self.enemy_party.index(enemy)
            self.menuVerticalChoicesList.append(
                {"event": "Target-{}".format(index), "text": enemy["name"]})
        self.createVerticalButtons()

    def createButton(self, text, index, eventArgs):
        index_row = index % self.COLUMN_HEIGHT
        index_col = index // self.COLUMN_HEIGHT
        btn = DirectRadioButton(text=text,
                                text_align=TextNode.ALeft,
                                scale=0.07,
                                frameColor=(0, 0, 0, 0.0),
                                pos=(base.a2dLeft + 0.2 + (index_col * .5), 0,
                                     (-0.55 - (index_row * .1))),
                                variable=self.menuVerticalChoice,
                                value=[index],
                                text_fg=(1, 1, 1, 1),
                                command=self.menuVerticalEvent)
        self.menuVerticalButtons.append(btn)
        btn.reparentTo(self.frameMain)

    def cancelCommand(self):
        base.messenger.send("Fight-Input")
