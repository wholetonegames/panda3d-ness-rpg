import t_helper as TextHelper
import t_data


class TextEngine:
    def __init__(self, messageCallback):
        self.messageCallback = messageCallback
        self.labelDict = t_data.labelDict
        self.gameTextList = t_data.gameTextList
        self.lineIndex = 0
        self.currentLabel = ''
        self.nextlabel = ''
        self.currentActor = ''
        self.actorDict = {}

    def setTextLabel(self, label):
        self.currentLabel = TextHelper.removeCharacters(label, [TextHelper.GOTO_SIGN,
                                                                TextHelper.LABEL_START,
                                                                TextHelper.LABEL_END,
                                                                TextHelper.LINE_BREAK])
        self.nextlabel = next((key for key, value in self.labelDict.items()
                               if value > self.labelDict[self.currentLabel]), self.currentLabel)
        self.lineIndex = self.labelDict[self.currentLabel] + 1

    def getLine(self):
        return self.gameTextList[self.lineIndex]

    def registerActor(self, actorKey, actorObj):
        self.actorDict[actorKey] = actorObj

    def getActorName(self, actorKey):
        if 'name' in self.actorDict[actorKey]:
            return self.actorDict[actorKey]["name"]
        else:
            return 'no name error'

    def setActor(self, line):
        actor = TextHelper.removeCharacters(line, [TextHelper.ACTOR_SIGN,
                                                   TextHelper.NON_BREAK_SPACE,
                                                   TextHelper.LINE_BREAK])
        if len(actor) == 0:
            self.currentActor = ''
        else:
            self.currentActor = self.getActorName(actor)

    def replaceActorInline(self, line):
        index = line.find(TextHelper.WHO_START)
        while index > -1:
            start = line.find(TextHelper.WHO_START)
            end = line.find(TextHelper.WHO_END)
            character = line[start+1:end]
            name = self.getActorName(character)
            line = line[:start] + name + line[end+1:]
            index = line.find(TextHelper.WHO_START)
        return line

    def displayLine(self, line):
        actor = self.currentActor
        if line.find(TextHelper.WHO_START) > -1:
            line = self.replaceActorInline(line)
        return {'line': line, 'actor': actor, 'type': 'text'}

    def callTextCode(self, line):
        line = TextHelper.removeCharacters(
            line, [TextHelper.CODE_SIGN, TextHelper.PAREN_START, TextHelper.PAREN_END])
        messageList = line.split(",")
        argsList = None
        if len(messageList) > 1:
            argsList = self.formatArgsList(messageList[1:])
        self.messageCallback(messageList[0], argsList)

    def formatArgsList(self, argsList):
        newArgslist = []
        for item in argsList:
            newItem = TextHelper.removeCharacters(
                item, [TextHelper.LABEL_END, TextHelper.LABEL_START])
            newArgslist.append(newItem)
        return newArgslist

    def getDialogue(self):
        index = self.lineIndex
        nextLabelIndex = self.labelDict[self.nextlabel]
        dialogue = []
        while index < nextLabelIndex:
            line = TextHelper.removeCharacters(
                self.gameTextList[index], [TextHelper.LINE_BREAK])
            processedLine = self.processLine(line)
            index += 1

            if not processedLine:
                continue

            dialogue.append(processedLine)

        return dialogue

    def processLine(self, line):
        if not line:
            return

        if line[0] == TextHelper.ACTOR_SIGN:
            self.setActor(line)
        elif line[0] == TextHelper.CODE_SIGN:
            self.callTextCode(line)
        elif line[0] == TextHelper.GOTO_SIGN:
            self.setTextLabel(line)
        elif line[0] == TextHelper.MENU_SIGN:
            return self.getTextMenu()
        else:
            return self.displayLine(line)

    def getTextMenu(self):
        menu = {}
        menu['type'] = 'menu'

        nextLabelIndex = self.labelDict[self.nextlabel]
        index = self.lineIndex + 1

        if index >= nextLabelIndex:
            return

        menu['text'] = TextHelper.removeCharacters(
            self.gameTextList[index], [TextHelper.LINE_BREAK])
        menu['options'] = []
        index += 1

        while index < nextLabelIndex:
            line = TextHelper.removeCharacters(
                self.gameTextList[index], [TextHelper.LINE_BREAK])

            if len(line) < 1:
                index += 1
                continue

            if line[0] == TextHelper.MENU_SIGN:
                break
            elif line[0] == TextHelper.OPTION_SIGN:
                option = {}
                option['text'] = TextHelper.removeCharacters(self.gameTextList[index],
                                                             [TextHelper.LINE_BREAK, TextHelper.OPTION_SIGN])
                index += 1
                option['action'] = TextHelper.removeCharacters(self.gameTextList[index],
                                                               [TextHelper.LINE_BREAK, TextHelper.OPTION_SIGN])
                menu['options'].append(option)
                index += 1
            else:
                index += 1

        return menu

    def chooseFromMenu(self, menu, index):
        self.processLine(menu['options'][index]['action'])
