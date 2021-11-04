from plover_stroke import BaseStroke
LONGEST_KEY = 2


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


def run_numbered_command(stroke, value):
    number = number_from_chord(stroke)
    if number != 0:
        return value.replace("$", str(number))
    return "{}"


numbered = {
    "T-": "{#Command($)}",
    "W-": "{#Control($)}",
    "PH-": "{#Control(Shift(Option($)))}",
}


def lookup_numbered(key):
    if len(key) == 1:
        stroke = Stroke(key[0])
        for pattern in numbered:
            if all([
                left_bank_stroke & stroke == pattern,
                (stroke & right_bank_stroke) & numbers_stroke == (
                    stroke & right_bank_stroke),
                (stroke & vowels_stroke) == Stroke.from_integer(0)
            ]):
                return run_numbered_command(stroke, numbered[pattern])

    raise KeyError


def lookup(key):
    for f in [lookup_numbered]:
        try:
            return f(key)
        except KeyError:
            pass

    raise KeyError


print(lookup(['W-F']))
