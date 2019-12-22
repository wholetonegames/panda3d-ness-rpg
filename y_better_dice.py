#http://howtomakeanrpg.com/a/better-than-dice.html
import random

class BetterThanDice:
    def __init__(self, length):
        self.length = length
        self.array = []
        self.shuffle()
        self.index = 0
        self.payload = None
        
    def shuffle(self):
        length = self.length
        array = list(range(length))
        while length > 1:
            index = random.randint(0,length-1)
            array[length-1], array[index] = array[index], array[length-1]
            length = length - 1
        self.array = array

    def getValue(self):
        self.payload = self.array[self.index]
        self.index += 1
        if self.index >= self.length:
            self.reshuffle()
        return self.payload

    def reshuffle(self):
        self.shuffle()
        self.index = 0
        
        if self.array[0] == self.payload:
            self.array[0], self.array[-1] = self.array[-1], self.array[0]

            
if __name__ == '__main__':

    x = 6
    b = BetterThanDice(x)

    printList = ''
    for n in list(range(x*4)):
        successSymbol = '_' if b.getValue() > 0 else '+'
        printList += successSymbol

    print(printList)
