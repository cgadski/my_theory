import json
import shutil
import os

mainStack = ['commands.json', 'personal.json', 'community.json']

states = {
    'CONTROL': ['user_control.json', 'control.json', 'commands.json', 'numbered.py'],
    'INPUT': ['user_input.json'] + mainStack,
    'INPUT_UNTIL_RETURN': ['user_input.json', 'catch_return.json'] + mainStack,
}

files = set()
for state in states:
    for file in states[state]:
        files.add(file)

def command_for_state(state):
    dicts_in = states[state]
    dicts_out = [file for file in files if file not in dicts_in]
    dicts = lambda prefix, dicts: ','.join([prefix + file for file in dicts])
    return \
        '{PLOVER:PRIORITY_DICT:' + dicts('', dicts_in) + '}' + \
        '{PLOVER:TOGGLE_DICT:' + dicts('+', dicts_in) + '}' + \
        '{PLOVER:TOGGLE_DICT:' + dicts('-', dicts_out) + '}'

commands = { 
    "{STACKER:" + state + "}": command_for_state(state) for state in states }

no_replace = set(['personal.json', 'community.json'])
input_files = set(['user_input.json', 'user_control.json'])

for file in files:
    if file in input_files:
        continue

    print('Processing', file)

    ext = file.split('.')[-1]
    if ext == 'json' and file not in no_replace:
        data = json.load(open(file, 'r'))
        for key in data:
            for command in commands:
                data[key] = data[key].replace(command, commands[command])
        json.dump(data, open('compiled/' + file, 'w'))
        continue

    shutil.copyfile(file, './compiled/' + file)