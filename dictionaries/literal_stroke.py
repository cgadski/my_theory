LONGEST_KEY = 2


def lookup(key):
    if key[0] != 'STR*':
        raise KeyError
    if len(key) == 1:
        return '[literal stroke]'
    if len(key) == 2:
        return key[1]
    raise KeyError

