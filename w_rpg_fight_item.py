from w_i_menu import IMenu
from direct.gui.DirectGui import (
    DirectFrame,
    DirectLabel,
    DirectRadioButton)
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
import y_helpers


class RPGFightItem(IMenu):
    def __init__(self, itemList):
        self.itemList = itemList
        frame = DirectFrame(frameColor=(0, 0, 0, 0.5),
                            borderWidth=(10, 10),
                            # (Left,Right,Bottom,Top)
                            frameSize=(-2, 2, -1, -0.45))
        IMenu.__init__(self, frame=frame)
        self.menuVerticalChoicesList = []
        for item in self.itemList:
            index = self.itemList.index(item)
            ItemInfo = y_helpers.find_by_id(item['id'], base.itemData.items)
            self.menuVerticalChoicesList.append(
                {"event": "Item-{}".format(index), "text": ItemInfo["name"]})
        self.createVerticalButtons()

    def createButton(self, text, index, eventArgs):
        btn = DirectRadioButton(text=text,
                                text_align=TextNode.ALeft,
                                scale=0.05,
                                frameColor=(0, 0, 0, 0.0),
                                pos=(base.a2dLeft + 0.2, 0,
                                     (-0.55 - (index * .1))),
                                variable=self.menuVerticalChoice,
                                value=[index],
                                text_fg=(1, 1, 1, 1),
                                command=self.menuVerticalEvent)
        self.menuVerticalButtons.append(btn)
        btn.reparentTo(self.frameMain)

    def cancelCommand(self):
        base.messenger.send("Fight-Input")
