from config import states
from os import listdir


def check_states():
    for _, config in states.items():
        if 'stack' not in config:
            config['stack'] = []
        if 'name' not in config:
            config['name'] = None
        if 'definition_file' not in config:
            config['definition_file'] = None
        if 'definition_file' in config and 'definition_stack' not in config:
            config['definition_stack'] = config['stack']
        if 'transitions' not in config:
            config['transitions'] = {}


check_states()


def get_used_files():
    used_files = set()

    for _, config in states.items():
        for k in ['stack', 'definition_stack']:
            if k in config:
                [used_files.add(d) for d in config[k]]

    return used_files


def check_files():
    used_files = get_used_files()
    available_files = listdir('./dictionaries')

    for file in used_files:
        if file not in available_files:
            raise Exception(file + " is not available!")

    for file in available_files:
        if file not in available_files:
            raise Exception(file + " is not used!")
    
    return used_files

dictionaries = check_files()

def transition_command(stack):
    unused = [d for d in dictionaries if d not in stack]

    def dicts(command, prefix, dicts): 
        if dicts == []:
            return ''
        inner = ','.join([prefix + file for file in dicts])
        return '{PLOVER:' + command + ':' + inner + '}'
    return \
        dicts('TOGGLE_DICT', '+', stack) + \
        dicts('PRIORITY_DICT', '+', stack) + \
        dicts('TOGGLE_DICT', '-', unused)

def name_commands():
    commands = {}
    for state, config in states.items():
        if config['name'] is not None:
            commands[config['name']] = transition_command(
                [state + '.json'] + config['stack'])
    return commands

print(name_commands())
