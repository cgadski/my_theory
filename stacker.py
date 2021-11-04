import json
import shutil
import os

states = {
    # 'CONTROL': ['commands.json', 'numbered.py'],
    # 'INPUT': inputState,
    'INPUT_UNTIL_RETURN': ['catch_return.json']
}

def command_for_state(state):
    dicts = ['+' + file for file in states[state]]
    return '{PLOVER:SOLO_DICT:' + ','.join(dicts) + '}'

commands = { state: command_for_state(state) for state in states }

files = set()
for state in states:
    for file in states[state]:
        files.add(file)

os.mkdir('compiled')

for file in files:
    ext = file.split('.')[-1]
    if ext == 'json':
        data = json.load(open(file, 'r'))
        for key in data:
            for command in commands:
                data[key] = data[key].replace(commands[command], command)
        json.dump(data, open('compiled/' + file, 'w'))

    if ext == 'py':
        shutil.copyfile(file, './compiled/' + file)


print(files)