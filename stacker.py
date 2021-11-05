import json
from config import states as state_configs
from os import listdir


def check_states():
    for _, config in state_configs.items():
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

    for _, config in state_configs.items():
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
        if file not in used_files:
            raise Exception(file + " is not used!")

    return used_files


def generated_dictionaries():
    for state, config in state_configs.items():
        yield state + '.json'
        if config['definition_file'] is not None:
            yield state + '_T.json'


dictionaries = list(check_files()) + list(generated_dictionaries())


def transition_command(stack):
    unused = [d for d in dictionaries if d not in stack]

    def dicts(command, prefix, dicts):
        if dicts == []:
            return ''
        inner = ','.join([prefix + file for file in dicts])
        return '{PLOVER:' + command + ':' + inner + '}'
    return \
        dicts('TOGGLE_DICT', '+', stack) + \
        dicts('PRIORITY_DICT', '', stack) + \
        dicts('TOGGLE_DICT', '-', unused)


def transition_to_state(state):
    return transition_command([state + '.json'] + state_configs[state]['stack'])


def transition_to_state_t(state):
    config = state_configs[state]
    return transition_command(
        [config['definition_file']] +
        [state + '_T.json'] + config['definition_stack'])


def global_commands():
    commands = {}
    for remote_state, config in state_configs.items():
        if config['name'] is not None:
            commands[config['name']] = transition_to_state(remote_state)
    return commands


def state_commands(state):
    config = state_configs[state]
    commands = global_commands()
    commands_t = None

    for stroke, command in config['transitions'].items():
        for new_state in state_configs:
            command = command.replace(
                '{STACKER:' + new_state + '}', transition_to_state(new_state))
        commands[stroke] = command

    if config['definition_file'] is not None:
        commands['TKUPT'] = transition_to_state_t(state) + \
            '{PLOVER:ADD_TRANSLATION}'

        commands_t = {
            'TA*B': '{#Tab}{^}',
            'TAB': '{#Tab}{^}',
            'R-R': '{^\n^}' + transition_to_state(state),
            'TPEFBG': '{#Escape}' + transition_to_state(state),
        }

    return commands, commands_t


for state in state_configs:
    commands, commands_t = state_commands(state)
    with open('./generated/' + state + '.json', 'w') as f:
        json.dump(commands, f, indent=2)

    if commands_t is not None:
        with open('./generated/' + state + '_T.json', 'w') as f:
            json.dump(commands_t, f, indent=2)
