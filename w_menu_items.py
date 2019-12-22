from direct.gui.OnscreenText import OnscreenText, TextNode
from direct.gui.DirectGui import (
    DGG,
    DirectFrame,
    DirectLabel,
    DirectRadioButton)
from w_i_menu_h import IMenuHorizontal
import y_helpers


class ItemMenu(IMenuHorizontal):
    def __init__(self):
        self.COLUMN_HEIGHT = 6
        frame = DirectFrame(frameSize=(base.a2dLeft, base.a2dRight,
                                       base.a2dBottom, base.a2dTop),
                            frameColor=(0, 0, 0, 1.0))
        IMenuHorizontal.__init__(self, self.COLUMN_HEIGHT, frame=frame)
        self.menuVerticalChoicesList = []
        self.updateInventory()
        self.createVerticalButtons()
        self.addTitle()

    def createButton(self, text, index, eventArgs):
        index_row = index % self.COLUMN_HEIGHT
        index_col = index // self.COLUMN_HEIGHT
        btn = DirectRadioButton(text=text,
                                text_align=TextNode.ALeft,
                                scale=0.07,
                                frameColor=(0, 0, 0, 0.0),
                                pos=(base.a2dLeft + 0.7 + (index_col * .5), 0,
                                     (0.5 - (index_row * .25))),
                                variable=self.menuVerticalChoice,
                                value=[index],
                                text_fg=(1, 1, 1, 1),
                                command=self.menuVerticalEvent)

        self.menuVerticalButtons.append(btn)
        btn.reparentTo(self.frameMain)

    def addTitle(self):
        self.title = OnscreenText(
            'Inventory', 1, 
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
        self.menuVerticalChoicesList = []
        for item in base.gameData.items:
            itemInfo = y_helpers.find_by_id(item['id'], base.itemData.items)
            # need events to use items?
            self.menuVerticalChoicesList.append(
                {"event": "*",   "text": "{} x  {}".format(itemInfo['name'], item['amount'])})
        self.menuVerticalChoicesList.append(
            {"event": "Back-Option",   "text": "Back to Menu"})

