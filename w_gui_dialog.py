from direct.gui.DirectGui import DirectFrame
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
from w_gui_dialog_options import GUIDialogOptions


class GUIDialog:
    def __init__(self):
        self.mainFrame = DirectFrame(frameColor=(0, 0, 0, 0.5),
                                     borderWidth=(10, 10),
                                     frameSize=(-2, 2, -1, -0.45))
        self.textIndex = 0
        self.isCalling = False
        self.frameText = None
        self.frameActor = None
        self.frameChoices = None
        self.textList = []
        self.hide()

    def setLabel(self, labelName):
        base.textEngine.setTextLabel(labelName)
        self.textList = base.textEngine.getDialogue()
        self.processLine(self.textList[self.textIndex])

    def processLine(self, line):
        if line['type'] == 'text':
            self.dialogueLine(line)
        elif line['type'] == 'menu':
            self.choiceLine(line)

    def choiceLine(self, lineObj):
        self.setFrameText(lineObj['text'])
        self.setFrameChoices(lineObj)
        self.show()

    def dialogueLine(self, lineObj):
        self.setFrameActor(lineObj['actor'])
        self.setFrameText(lineObj['line'])
        self.show()

    def showMessage(self, txt):
        self.setFrameText(txt)
        self.show()

    def setFrameChoices(self, lineObj):
        base.resetButtons()
        if self.frameChoices:
            self.frameChoices.quit()

        optionsList = lineObj['options']
        self.frameChoices = GUIDialogOptions(optionsList)
        self.frameChoices.reparentTo(self.mainFrame)
        taskMgr.add(self.frameChoices.readKeys, "readKeysTask")
        for option in optionsList:
            index = optionsList.index(option)
            base.accept("TextChoice-{}".format(index),
                        self.chooseOption, [lineObj, index])

    def destroyFrameChoices(self, optionsList):
        self.frameChoices.quit()
        self.frameChoices = None
        taskMgr.remove("readKeysTask")
        for option in optionsList:
            index = optionsList.index(option)
            base.ignore("TextChoice-{}".format(index))

    def chooseOption(self, lineObj, index):
        base.textEngine.chooseFromMenu(lineObj, index)
        self.destroyFrameChoices(lineObj['options'])
        self.textList = base.textEngine.getDialogue()
        self.textIndex = 0
        self.processLine(self.textList[self.textIndex])

    def setFrameActor(self, text):
        if self.frameActor:
            self.frameActor.detach_node()
        self.frameActor = OnscreenText(text=text,
                                       pos=(-1.2, -0.55),
                                       scale=0.07,
                                       wordwrap=35,
                                       mayChange=False,
                                       align=TextNode.ALeft,
                                       fg=(1, 1, 1, 1),
                                       shadow=(0, 0, 0, 1),
                                       shadowOffset=(0.05, 0.05))
        self.frameActor.reparentTo(self.mainFrame)

    def setFrameText(self, text):
        if self.frameText:
            self.frameText.detach_node()
        self.frameText = OnscreenText(text=text,
                                      pos=(-1.2, -0.65),
                                      scale=0.07,
                                      wordwrap=35,
                                      mayChange=False,
                                      align=TextNode.ALeft,
                                      fg=(1, 1, 1, 1),
                                      shadow=(0, 0, 0, 1),
                                      shadowOffset=(0.05, 0.05))
        self.frameText.reparentTo(self.mainFrame)

    def show(self):
        self.mainFrame.show()

    def hide(self):
        self.mainFrame.hide()
        if self.frameText:
            self.frameText.detach_node()
        if self.frameActor:
            self.frameActor.detach_node()
        self.textIndex = 0
        self.frameText = None

    def next(self):
        if not self.isCalling:
            self.isCalling = True
            taskMgr.doMethodLater(.1, self.nextText, 'Next Text')

    def nextText(self, task):
        if self.textIndex < len(self.textList) - 1:
            self.textIndex += 1
            self.processLine(self.textList[self.textIndex])
        else:
            self.hide()

        self.isCalling = False
        return task.done

    @property
    def isShowing(self):
        return self.frameText != None

    @property
    def isChoices(self):
        return self.frameChoices != None

    def reparentTo(self, target):
        self.mainFrame.reparentTo(target)

    def removeNode(self):
        self.mainFrame.removeNode()