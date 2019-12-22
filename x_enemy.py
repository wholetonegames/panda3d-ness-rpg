import random
import copy
import y_helpers


class EnemyModel:
    def __init__(self):
        self.init_enemies()
        self.get_parties_by_label()

    def enemy_party(self, label):
        enemy_types_list = random.choice(
            self.parties_by_label[label])
        enemy_p = []
        for t in enemy_types_list:
            prototype = y_helpers.find_by_id(t['id'], self.enemies)
            for i in list(range(t['amount'])):
                e = copy.deepcopy(prototype)
                e['name'] += ' {}'.format(i+1)
                enemy_p.append(e)
        return enemy_p

    def init_enemies(self):
        self.enemies = [
            # heaven ########################
            {'id': 1,
             'name': "Ramblin' Mushroom ",
             'model': 'mush',
             'hp': 30, 'max_hp': 30,
             'xp': 5,
             'attack': {'base': 5, 'buffAdd': 0, 'buffMult': 1},
             'defense': {'base': 5, 'buffAdd': 0, 'buffMult': 1},
             'speed': {'base': 5, 'buffAdd': 0, 'buffMult': 1},
             'statusEffect': {'KO': False, 'POISONED': False, 'STUNNED': False, 'CONFUSED': False},
             'statusImmunity': [],
             'items': [],
             'description': "regular one",
            #  'strategy': 'twice',
             'magic': [1, 2]},
        ]

    def get_parties_by_label(self):
        self.parties_by_label = {
            'mush': [
                [{'id': 1, 'amount': 1}],
                [{'id': 1, 'amount': 2}],
                [{'id': 1, 'amount': 3}],
                # [{'id': 1, 'amount': 1}, {'id': 3, 'amount': 1}],
                # [{'id': 1, 'amount': 1}, {'id': 3, 'amount': 2}],
                # [{'id': 3, 'amount': 3}],
            ],
        }
