LINE_BREAK = '\n'
NON_BREAK_SPACE = ' '
ACTOR_SIGN = '*'
CODE_SIGN = '$'
WHO_START = '{'
WHO_END = '}'
MENU_SIGN = '%'
OPTION_SIGN = '&'
GOTO_SIGN = '@'
LABEL_START = '['
LABEL_END = ']'
PAREN_START = '('
PAREN_END = ')'
LABEL_SENTINEL = '[--end--]'
COMMENT = '#'


def removeCharacters(line, removalList):
    for item in removalList:
        line = line.replace(item, '')
    return line.strip()
