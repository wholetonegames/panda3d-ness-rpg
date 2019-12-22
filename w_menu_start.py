import webbrowser
from direct.gui.OnscreenText import OnscreenText, TextNode
from direct.gui.DirectGui import (
    DirectFrame,
    DirectLabel,
    DirectRadioButton)
from w_i_menu import IMenu


class StartMenu(IMenu):
    def __init__(self):
        frame = DirectFrame(frameSize=(base.a2dLeft, base.a2dRight,
                                       base.a2dBottom, base.a2dTop),
                            frameColor=(0, 0, 0, 1.0))
        IMenu.__init__(self, frame=frame)
        self.menuVerticalChoicesList = [
            {"event": "Menu-Start", "text": "New game"},
            {"event": "Menu-Load", "text": "Load game"},
            {"event": "Menu-Website", "text": "Visit Wholetone Games"},
            {"event": "Menu-Quit", "text": "Quit"}
        ]

        self.isFetchingSite = False

        self.addTitle()
        self.createVerticalButtons()

    def createButton(self, text, index, eventArgs):
        btn = DirectRadioButton(text=text,
                                text_align=TextNode.ACenter, 
                                scale=0.07,
                                frameColor=(0, 0, 0, 0.0),
                                pos=(0, 0,
                                     (-.10 - (index * .15))),
                                variable=self.menuVerticalChoice,
                                value=[index],
                                text_fg=(1, 1, 1, 1),
                                command=self.menuVerticalEvent)

        self.menuVerticalButtons.append(btn)
        btn.reparentTo(self.frameMain)

    def websiteTask(self):
        if not self.isFetchingSite:
            self.isFetchingSite = True
            taskMgr.add(self.openSite, 'openSite')

    def openSite(self, task):
        webbrowser.open('http://wholetonegames.blogspot.com', new=2)
        taskMgr.doMethodLater(0.1, self.afterSiteLoads, 'site Loaded')
        return task.done

    def afterSiteLoads(self, task):
        self.isFetchingSite = False
        return task.done

    def addTitle(self):
        self.title = OnscreenText(
            base.appName, 1, 
            fg=(1, 0, 0, 1), 
            pos=(0, 0.3), 
            font=base.font_title,
            align=TextNode.ACenter, 
            scale=.5, 
            mayChange=1)
        self.title.reparentTo(self.frameMain)

    def cancelCommand(self):
        pass
