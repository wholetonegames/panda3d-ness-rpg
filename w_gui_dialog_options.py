from w_i_menu import IMenu
from direct.gui.DirectGui import (
    DirectFrame,
    DirectLabel,
    DirectRadioButton)
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode


class GUIDialogOptions(IMenu):
    def __init__(self, itemList):
        self.itemList = itemList
        frame = DirectFrame(frameColor=(0, 0, 0, 0.5),
                                     borderWidth=(10, 10),
                                     # (Left,Right,Bottom,Top)
                                     frameSize=(1, 1.7, -0.44, 0.8))

        IMenu.__init__(self, frame=frame)
        self.menuVerticalChoicesList = []
        for item in self.itemList:
            index = self.itemList.index(item)
            self.menuVerticalChoicesList.append(
                {"event": "TextChoice-{}".format(index), "text": item["text"]})
        self.createVerticalButtons()

    def createButton(self, text, index, eventArgs):
        btn = DirectRadioButton(text=text,
                                text_align=TextNode.ALeft,
                                scale=0.07,
                                frameColor=(0, 0, 0, 0.0),
                                pos=(1.1, 0, (0.65 - (index * .1))),
                                variable=self.menuVerticalChoice,
                                value=[index],
                                text_fg=(1, 1, 1, 1),
                                command=self.menuVerticalEvent)
        self.menuVerticalButtons.append(btn)
        btn.reparentTo(self.frameMain)

    def cancelCommand(self):
        pass

    def reparentTo(self, target):
        self.frameMain.reparentTo(target)
