import random
import y_helpers


class FightRound:
    def __init__(self, hero_party, enemy_party, inventory, magic_model, input_list=[]):
        self.hero_party = hero_party
        self.enemy_party = enemy_party
        self.inventory = inventory
        self.magic_model = magic_model
        self.combined_parties = self.hero_party + self.enemy_party
        self.input_list = input_list
        self.round_index = 0
        self.enemy_strategies = {'cure': self.strat_enemy_cure,
                                 'twice': self.strat_enemy_attack_twice}

        self.turnOrderList = self.create_turn_order_list()

    @property
    def is_battle_over(self):
        return next((False for x in self.hero_party if not y_helpers.is_character_KOed(x)), True) or \
            next(
                (False for x in self.enemy_party if not x['statusEffect']['KO']), True)

    @property
    def outcome(self):
        if self.is_battle_over:
            ishero_partyDefeated = next(
                (False for x in self.hero_party if not y_helpers.is_character_KOed(x)), True)
            return y_helpers.OUTCOME_DEFEAT if ishero_partyDefeated else y_helpers.OUTCOME_VICTORY

        return y_helpers.OUTCOME_DRAW

    def handle_enemy(self, enemy, order):
        if y_helpers.is_team_KOed(self.hero_party):
            return
        if 'strategy' in enemy:
            self.enemy_strategies[enemy['strategy']](enemy, order)
        else:
            self.strat_enemy_vanilla(enemy, order)

    def enemy_choose_target(self, targetType, duel, enemy):
        if targetType == y_helpers.TARGET_ANOTHER:
            duel['target'] = [random.choice(self.hero_party)]
            while y_helpers.is_character_KOed(duel['target'][0]):
                duel['target'] = [random.choice(self.hero_party)]
        elif targetType == y_helpers.TARGET_SELF:
            duel['target'] = [enemy]
        elif targetType == y_helpers.TARGET_ANOTHER_PARTY:
            duel['target'] = self.hero_party
        elif targetType == y_helpers.TARGET_OWN_PARTY:
            duel['target'] = self.enemy_party

    def handle_poison(self, element, order):
        duel = {'agent': {'name': 'POISONED',
                          'hp': 1,
                          'speed': {'base': 1, 'buffAdd': 0, 'buffMult': 1},
                          'statusEffect': {'KO': False, 'POISONED': False, 'STUNNED': False, 'CONFUSED': False}
                          }
                }
        duel['target'] = [element]
        duel['type'] = y_helpers.TYPE_POISON
        order.append(duel)

    def create_turn_order_list(self):
        order = []
        for duel in self.input_list:
            if y_helpers.is_character_KOed(duel['agent']) or duel['agent']['statusEffect']['CONFUSED']:
                continue
            duel['isHeroAgent'] = True
            order.append(duel)
        for enemy in self.enemy_party:
            if y_helpers.is_character_KOed(enemy) or enemy['statusEffect']['CONFUSED']:
                continue
            self.handle_enemy(enemy, order)
        for element in self.combined_parties:
            if element['statusEffect']['KO']:
                continue
            if element['statusEffect']['POISONED']:
                self.handle_poison(element, order)
            if element['statusEffect']['CONFUSED']:
                self.handle_confused(element, order)
        order = sorted(order, key=lambda x: y_helpers.get_stat(
            x['agent']['speed']), reverse=True)
        return order

    def handle_confused(self, element, order):
        if y_helpers.is_team_KOed(self.combined_parties):
            return
        duel = {'agent': element}
        duel['target'] = [random.choice(self.combined_parties)]
        while y_helpers.is_character_KOed(duel['target'][0]):
            duel['target'] = [random.choice(self.combined_parties)]
        duel['type'] = y_helpers.TYPE_ATTACK
        order.append(duel)

    @property
    def is_last_turn_in_round(self):
        return len(self.turnOrderList) == self.round_index + 1

    @property
    def current_turn(self):
        return self.turnOrderList[self.round_index]

    def next_turn(self):
        if self.round_index <= len(self.turnOrderList) - 1:
            self.round_index += 1

    def round_fight(self):
        turn = self.current_turn
        if self.is_battle_over:
            return
        if y_helpers.is_character_KOed(turn['agent']):
            return
        message = ''
        if turn['type'] == y_helpers.TYPE_ATTACK:
            message = self.attack()
        elif turn['type'] == y_helpers.TYPE_MAGIC:
            message = self.magic()
        elif turn['type'] == y_helpers.TYPE_POISON:
            message = self.poison()
        # this may need to change in the future if the messages don't fit
        return [message]

    def poison(self):
        turn = self.current_turn
        message = ''
        poisonDamage = 1
        for target in turn['target']:
            if target['statusEffect']['KO']:
                target['statusEffect']['POISONED'] = False
                return
            y_helpers.update_hp(target, poisonDamage)
            message += '{} took {} damage from Poison\n'.format(
                target['name'], poisonDamage)
        return message

    def can_cast_spell(self, spell):
        for cost in spell['costs']:
            letter = y_helpers.find_by_name(self.inventory, cost)
            if letter["amount"] < spell['costs'][cost]:
                return False
        return True

    def magic(self):
        turn = self.current_turn
        canCastSpell = self.can_cast_spell(turn['spell'])
        if not canCastSpell:
            return "{} cannot cast {}".format(turn['agent']['name'], turn['spell']['name'])

        for cost in turn['spell']['costs'].keys():
            letter = y_helpers.find_by_name(self.inventory, cost)
            letter['amount'] -= turn['spell']['costs'][cost]

        message = ''
        for target in turn['target']:
            message = self.cast_spell(message, target, turn)
        return message

    def cast_spell(self, message, target, turn):
        if turn['agent']['name'] == target['name']:
            message += '{} cast {}'.format(
                turn['agent']['name'], turn['spell']['name'])
        else:
            message += '{} cast {} on {}'.format(
                turn['agent']['name'], turn['spell']['name'], target['name'])

        for affect in turn['spell']['affects'].keys():
            key = turn['spell']['affects'][affect]
            if affect == 'custom':
                message += self.spells.items[key](
                    turn['agent'], self.hero_party, self.enemy_party)
            elif affect == 'statusOn':
                if key in target['statusImmunity']:
                    message += self.failed_status_message(target, key)
                else:
                    target['statusEffect'][key] = True
                    message += self.added_status_message(target, key)
            elif affect == 'statusOff':
                target['statusEffect'][key] = False
                message += self.removed_status_message(target, key)
            else:
                if affect == 'hp':
                    if key >= 1:
                        # cure
                        y_helpers.update_hp(target, key)
                        message += self.append_cure_message(target)
                    elif key <= 1:
                        m_attack = (
                            key + 0 - y_helpers.get_stat(turn['agent']['attack']))
                        y_helpers.update_hp(target, m_attack)
                        message += self.append_attack_message(
                            turn['agent'], target, m_attack)
                    else:
                        # by percentage points
                        # add later
                        pass
                else:
                    if key >= 1 or key <= -1:
                        target[affect]['buffAdd'] += key
                    else:
                        target[affect]['buffMult'] += key
        return message

    def failed_status_message(self, target, key):
        return '\nbut {} is immune to {}'.format(target['name'], key)

    def added_status_message(self, target, key):
        return '\n{} is {}'.format(target['name'], key)

    def removed_status_message(self, target, key):
        return '\n{} is not {} any more'.format(target['name'], key)

    def attack(self):
        turn = self.current_turn
        message = ''
        for target in turn['target']:
            if y_helpers.is_character_KOed(target):
                defendingParty = self.enemy_party if turn['isHeroAgent'] else self.hero_party
                target = next(
                    (x for x in defendingParty if not y_helpers.is_character_KOed(x)), None)
                if not target:
                    # maybe could call end of battle screen?
                    return
            message += self.attack_target(turn['agent'], target)
        return message

    def attack_target(self, attacker, defender):
        # make this more complex later
        defense = y_helpers.get_stat(defender['defense'])
        attack = y_helpers.get_stat(attacker['attack'])
        attackOutcome = defense - attack
        attackOutcome = min(-1, attackOutcome)
        y_helpers.update_hp(defender, attackOutcome)
        message = self.append_attack_message(attacker, defender, attackOutcome)
        return message

    def append_attack_message(self, attacker, defender, attackOutcome):
        message = '\n{} received {} damage from {}\'s attack'.format(
            defender['name'], (attackOutcome * -1), attacker['name'])
        if y_helpers.is_character_KOed(defender):
            message += '\nand collapsed\n'
        return message

    def append_cure_message(self, target):
        if target['hp'] == target['max_hp']:
            return "\nAnd {}'s HP is full".format(target['name'])
        else:
            return "\nAnd {} recovered some HP".format(target['name'])

    def gain_xp(self, messages):
        gainedXp = 0
        messages.append('The party has won')
        for enemy in self.enemy_party:
            gainedXp += enemy['xp']
        message = ''
        for hero in self.hero_party:
            if y_helpers.is_character_KOed(hero):
                continue
            message += '{} gained {} experience points\n'.format(
                hero['name'], gainedXp)
            hero['xp'] += gainedXp
        messages.append(message)

    def item_drop(self, messages):
        message = ''
        itemsDropped = []
        for enemy in self.enemy_party:
            if enemy['items']:
                for item in enemy['items']:
                    droppedItem = y_helpers.find_by_id(
                        item['id'], itemsDropped)
                    if droppedItem:
                        droppedItem['amount'] += item['amount']
                    else:
                        itemsDropped.append(item)
        for item in itemsDropped:
            inventoryItem = y_helpers.find_by_id(
                item['id'], self.inventory)
            if inventoryItem:
                inventoryItem['amount'] += item['amount']
            else:
                self.inventory.append(item)
            itemFromModel = y_helpers.find_by_id(
                item['id'], self.inventory)
            message += 'Dropped {} x {}\n'.format(
                itemFromModel['name'], item['amount'])
        if message:
            messages.append(message)

    def level_up(self, messages):
        message = ''
        for hero in self.hero_party:
            if self.has_changed_level(hero):
                message += '{} is now level {}\n'.format(
                    hero['name'], hero['level'])
        if message:
            messages.append(message)

    def battle_spoils_messages(self):
        messages = []
        if self.outcome == y_helpers.OUTCOME_DEFEAT:
            messages.append('The party has been defeated')
        elif self.outcome == y_helpers.OUTCOME_VICTORY:
            self.make_single_party()
            self.gain_xp(messages)
            self.item_drop(messages)
            self.level_up(messages)
        return messages

    def make_single_party(self):
        if self.hero_party[0]['hp'] <= 0:
            self.hero_party[0]['hp'] = 1
        self.hero_party = [self.hero_party[0]]

    def has_changed_level(self, hero):
        levelFromXP = y_helpers.get_level_estimate(hero['xp'])
        hasIncreased = levelFromXP > hero['level']
        if hasIncreased:
            hero['level'] = levelFromXP
        return hasIncreased

    def strat_enemy_vanilla(self, enemy, order):
        duel = {'agent': enemy}
        targetType = y_helpers.TARGET_ANOTHER
        self.enemy_choose_target(targetType, duel, enemy)
        duel['isHeroAgent'] = False
        duel['type'] = y_helpers.TYPE_ATTACK
        order.append(duel)

    def strat_enemy_cure(self, enemy, order):
        if enemy['hp'] != enemy['max_hp']:
            duel = {'agent': enemy}
            duel['isHeroAgent'] = False
            duel['type'] = y_helpers.TYPE_MAGIC
            spell_id = 4  # cure
            spell = y_helpers.find_by_id(spell_id, self.magic_model.items)
            duel['spell'] = spell
            targetType = spell['target']
            self.enemy_choose_target(targetType, duel, enemy)
            order.append(duel)
        else:
            self.strat_enemy_vanilla(enemy, order)

    def strat_enemy_attack_twice(self, enemy, order):
        self.strat_enemy_vanilla(enemy, order)
        self.strat_enemy_vanilla(enemy, order)
