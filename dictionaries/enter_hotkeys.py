from plover_stroke import BaseStroke


class Stroke(BaseStroke):
    pass


left_bank = 'S- T- K- P- W- H- R-'.split()
right_bank = '-F -R -P -B -L -G -T -S -D -Z'.split()
vowels = 'A- O- * -E -U'.split()
numbers = '-F -R -P -B'.split()


Stroke.setup(['#'] + left_bank + vowels + right_bank)

left_bank_stroke = Stroke.from_keys(left_bank)
right_bank_stroke = Stroke.from_keys(right_bank)
vowels_stroke = Stroke.from_keys(vowels)
numbers_stroke = Stroke.from_keys(numbers)


def number_from_chord(stroke: Stroke):
    chars = numbers[::-1]
    number_code = ''.join(['1' if c in stroke else '0' for c in chars])
    return int(number_code, 2)

commands = {
    'KROL': 'Control',
    'OPGS': 'Option',
    'ALT': 'Alt',
    'KPHAPBD': 'Command',
    'SHEUFT': 'Shift',
}

keys = {
    'A*': 'A',
    'PW*': 'B',
    'KR*': 'C',
    'TK*': 'D',
    '*E': 'E',
    'TP*': 'F',
    'TKPW*': 'G',
    'H*': 'H',
    '*EU': 'I',
    'SKWR*': 'J',
    'K*': 'K',
    'HR*': 'L',
    'PH*': 'M',
    'TPH*': 'N',
    'O*': 'O',
    'P*': 'P',
    'KW*': 'Q',
    'R*': 'R',
    'S*': 'S',
    'T*': 'T',
    '*U': 'U',
    'SR*': 'V',
    'W*': 'W',
    'KP*': 'X',
    'KWR*': 'Y',
    'STKPWHR*': 'Z',
}

LONGEST_KEY = 10

def lookup_key(key):
    if key in keys:
        return keys[key]
    
    stroke = Stroke(key)
    n = number_from_chord(stroke)
    if stroke & ~numbers_stroke == Stroke('TPH-') and n <= 9:
        return str(number_from_chord(stroke))
    if stroke & ~numbers_stroke == Stroke('TP-'):
        return 'F' + number_from_chord(stroke)
    
    raise KeyError

def form_command(commands, key):
    return '\{#' + ''.join([c + '(' for c in commands]) + \
        key + (')' * len(commands)) + '\}'

def lookup(key):
    if all([chord in commands for chord in key[:-1]]):
        if key[-1] in commands:
            return form_command([commands[c] for c in key], '')
        return form_command([commands[c] for c in key[:-1]], lookup_key(key[-1]))

    raise KeyError
