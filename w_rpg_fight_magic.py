from w_i_menu_h import IMenuHorizontal
from direct.gui.DirectGui import (
    DirectFrame,
    DirectLabel,
    DirectRadioButton)
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode


class RPGFightMagic(IMenuHorizontal):
    def __init__(self, magicList):
        self.COLUMN_HEIGHT = 4
        self.magicList = self.formatMagicList(magicList)
        frame = DirectFrame(frameColor=(0, 0, 0, 0.5),
                            borderWidth=(10, 10),
                            # (Left,Right,Bottom,Top)
                            frameSize=(-2, 2, -1, -0.45))
        IMenuHorizontal.__init__(self, self.COLUMN_HEIGHT, frame=frame)
        self.menuVerticalChoicesList = []
        for magic in self.magicList:
            index = self.magicList.index(magic)
            self.menuVerticalChoicesList.append(
                {"event": "Magic-{}".format(index), "text": magic["name"]})
        self.createVerticalButtons()

    def createButton(self, text, index, eventArgs):
        index_row = index % self.COLUMN_HEIGHT
        index_col = index // self.COLUMN_HEIGHT
        btn = DirectRadioButton(text=text,
                                text_align=TextNode.ALeft,
                                scale=0.05,
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

    def formatMagicList(self, mList):
        formattedList = base.magicData.create_readable_list(mList)
        return formattedList
