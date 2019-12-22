import math

TARGET_SELF = 'Own Character'
TARGET_ANOTHER = 'Opposing Character'
TARGET_OWN_PARTY = 'Own Party'
TARGET_ANOTHER_PARTY = 'Opposing Party'
TARGET_TYPES = (TARGET_SELF, TARGET_ANOTHER,
                TARGET_OWN_PARTY, TARGET_ANOTHER_PARTY)
OUTCOME_DRAW = 'ONGOING'
OUTCOME_VICTORY = 'VICTORY'
OUTCOME_DEFEAT = 'DEFEAT'
TYPE_POISON = 'Poison'
TYPE_ATTACK = 'Attacking'
TYPE_MAGIC = 'Magic'
TYPE_DEFENSE = 'Defending'
TYPE_ITEM = 'Item'
TYPES = (TYPE_ATTACK, TYPE_MAGIC)


def get_experience_estimate(level):
    return int(50 * (2**(level/3) - 2**(1/3)) / (2**(1/3) - 1))


def get_level_estimate(xp):
    if(xp == 0):
        return 1
    return math.ceil((3 * (math.log(1/50 * (2**(1/3) - 1) * xp + 2**(1/3)))) / math.log(2))


def find_by_id(givenId, idList):
    return next((item for item in idList if item['id'] == givenId), None)


def find_index_by_id(givenId, idList):
    return next((idList.index(item) for item in idList if item['id'] == givenId), -1)


def find_by_name(array, name):
    try:
        return next((item for item in array if item.name == name), None)
    except:
        return next((item for item in array if item['name'] == name), None)


def stringify_time_units(value):
    return str(value).zfill(2)

def is_character_KOed(fighter):
    if fighter['hp'] <= 0:
        fighter['statusEffect']['KO'] = True
    elif fighter['statusEffect']['KO']:
        fighter['hp'] = 0
    return fighter['statusEffect']['KO'] or fighter['statusEffect']['STUNNED']


def is_team_KOed(team):
    KO = 0
    for fighter in team:
        if is_character_KOed(fighter):
            KO += 1
    return len(team) == KO


def pretty_print_time(seconds):
    secondsBase = int(seconds)
    hourFromSeconds = 60 * 60
    minuteFromSeconds = 60
    hours = secondsBase // hourFromSeconds
    minutes = (secondsBase % hourFromSeconds) // minuteFromSeconds
    seconds = secondsBase % minuteFromSeconds

    return "{} h {} m {}s".format(stringify_time_units(hours),
                                  stringify_time_units(minutes),
                                  stringify_time_units(seconds))


def get_stat(stat):
    return int((stat['base'] * stat['buffMult']) + stat['buffAdd'])


def update_hp(chara, value):
    chara['hp'] += value
    chara['hp'] = max(0, chara['hp'])
    chara['hp'] = min(chara['max_hp'], chara['hp'])
