import y_helpers


class MagicModel:
    def __init__(self):
        self.init_spells()

    def create_readable_list(self, idList):
        readableList = []
        for idNumber in idList:
            item = y_helpers.find_by_id(idNumber, self.items)
            readableList.append(item)
        return readableList

    def init_spells(self):
        self.items = [
            ## add / remove HP ##
            {'id': 1,
             'name': 'FIRE',
             'costs': self.costs_from_name('FIRE'),
             'description': 'deals some damage to a group of enemies',
             'target': y_helpers.TARGET_ANOTHER_PARTY,
             'affects': {'hp': -1}},
            {'id': 3,
             'name': 'LIGHTNING',
             'costs': self.costs_from_name('LIGHTNING'),
             'description': 'deal great damage to one enemy',
             'target': y_helpers.TARGET_ANOTHER,
             'affects': {'hp': -1}},
            {'id': 4,
             'name': 'CURE',
             'costs': self.costs_from_name('CURE'),
             'description': 'regain some HP',
             'target': y_helpers.TARGET_SELF,
             'affects': {'hp': 1}},
            ## status magic ##
            {'id': 2,
             'name': 'ICE',
             'costs': self.costs_from_name('ICE'),
             'description': 'stuns an enemy, except if immune',
             'target': y_helpers.TARGET_ANOTHER,
             'affects': {'statusOn': 'STUNNED'}},
            {'id': 7,
             'name': 'WAKE',
             'costs': self.costs_from_name('WAKE'),
             'description': 'removes STUNNED',
             'target': y_helpers.TARGET_SELF,
             'affects': {'statusOff': 'STUNNED'}},
            {'id': 5,
             'name': 'HEAL',
             'costs': self.costs_from_name('HEAL'),
             'description': 'removes POISONED',
             'target': y_helpers.TARGET_SELF,
             'affects': {'statusOff': 'POISONED'}},
            {'id': 6,
             'name': 'VENOM',
             'costs': self.costs_from_name('VENOM'),
             'description': 'adds POISONED',
             'target': y_helpers.TARGET_ANOTHER,
             'affects': {'statusOn': 'POISONED'}},
            {'id': 8,
             'name': 'TRICK',
             'costs': self.costs_from_name('TRICK'),
             'description': 'adds CONFUSED',
             'target': y_helpers.TARGET_ANOTHER,
             'affects': {'statusOn': 'CONFUSED'}},
            ## add /  remove characters ##
            {'id': 9,
             'name': 'DOUBLE',
             'costs': self.costs_from_name('DOUBLE'),
             'description': 'the party now has two characters',
             'target': y_helpers.TARGET_SELF,
             'affects': {'custom': 'duplicate'}},
            {'id': 10,
             'name': 'TRIPLE',
             'costs': self.costs_from_name('TRIPLE'),
             'description': 'the party now has three characters',
             'target': y_helpers.TARGET_SELF,
             'affects': {'custom': 'triplicate'}},
            {'id': 11,
             'name': 'SACRIFICE',
             'costs': self.costs_from_name('SACRIFICE'),
             'description': 'lose one character to take down an enemy',
             'target': y_helpers.TARGET_SELF,
             'affects': {'custom': 'sacrifice'}},
            ## buff / debuff ##
            {'id': 12,
             'name': 'QUICK',
             'costs': self.costs_from_name('QUICK'),
             'description': 'speed up by 10%',
             'target': y_helpers.TARGET_SELF,
             'affects': {'speed': 0.1}},
            {'id': 13,
             'name': 'SLOW',
             'costs': self.costs_from_name('SLOW'),
             'description': 'speed down by 10%',
             'target': y_helpers.TARGET_ANOTHER,
             'affects': {'speed': -0.1}},
            {'id': 14,
             'name': 'FURY',
             'costs': self.costs_from_name('FURY'),
             'description': 'attack up by 10%',
             'target': y_helpers.TARGET_SELF,
             'affects': {'attack': 0.1}},
            {'id': 15,
             'name': 'CALM',
             'costs': self.costs_from_name('CALM'),
             'description': 'attack down by 10%',
             'target': y_helpers.TARGET_ANOTHER,
             'affects': {'attack': -0.1}},
            {'id': 16,
             'name': 'GUARD',
             'costs': self.costs_from_name('GUARD'),
             'description': 'defense up by 10%',
             'target': y_helpers.TARGET_SELF,
             'affects': {'defense': 0.1}},
            {'id': 17,
             'name': 'FOOL',
             'costs': self.costs_from_name('FOOL'),
             'description': 'defense down by 10%',
             'target': y_helpers.TARGET_ANOTHER,
             'affects': {'defense': -0.1}},
            ## using all letters :) ##
            {'id': 18,
             'name': 'ZAP',
             'costs': self.costs_from_name('ZAP'),
             'description': 'small electric attack',
             'target': y_helpers.TARGET_ANOTHER,
             'affects': {'hp': -1}},
            {'id': 19,
             'name': 'REJUVENATE',
             'costs': self.costs_from_name('REJUVENATE'),
             'description': 'regain all HP',
             'target': y_helpers.TARGET_SELF,
             'affects': {'hp': 1}},
            {'id': 20,
             'name': 'EXTERMINATE',
             'costs': self.costs_from_name('EXTERMINATE'),
             'description': 'kills opposing party',
             'target': y_helpers.TARGET_ANOTHER_PARTY,
             'affects': {'statusOn': 'KO'}},
        ]

    def costs_from_name(self, letter_array):
        output = {}
        for letter in letter_array:
            if letter in output:
                output[letter] += 1
            else:
                output[letter] = 1
        return output


if __name__ == "__main__":
    m = MagicModel()
    s = set([])
    for i in m.items:
        # print(i['costs'])
        for x in i['costs']:
            s.add(x)

    print(s)
    print(len(s))
