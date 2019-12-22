import os
import json
import t_helper as TextHelper

class TextParser:
    def __init__(self):
        self.path = './txt/'
        self.gameTextList = []
        self.labelDict = {}
        self.parseAllTextFiles()

    def parseAllTextFiles(self):
        index = 0

        for filename in os.listdir(self.path):
            file = open(self.path+filename, 'r')
            for line in file:
                if len(line) < 1 or line == TextHelper.LINE_BREAK:
                    continue
                if line[0] == TextHelper.LABEL_START:
                    self.indexLabel(line, index)
                elif line[0] == TextHelper.COMMENT:
                    continue
                self.gameTextList.append(line)
                index += 1

        # adding a last label to guard against crashes
        self.indexLabel(TextHelper.LABEL_SENTINEL, len(self.gameTextList))

    def indexLabel(self, label, index):
        label = TextHelper.removeCharacters(
            label, [TextHelper.LABEL_START, TextHelper.LABEL_END, TextHelper.LINE_BREAK])
        self.labelDict[label] = index

    def save(self):
        with open('t_data.py', 'w') as f:
            f.write('labelDict = ' + json.dumps(self.labelDict))
            f.write('\n')
            f.write('gameTextList = ' + json.dumps(self.gameTextList))


if __name__ == '__main__':
    t = TextParser()
    t.save()
