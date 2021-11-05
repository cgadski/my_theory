mainStack = [
    'staging.json',
    'literal_stroke.py',  # STR* for a literal stroke
    'basic_commands.json',  # everyday commands for use in edit mode
    'personal.json',  # personal English / programming dictionary
    'community.json'  # big community dictionary from Plover
]


states = {
    # for keyboard shortcuts
    'CONTROL': {
        'name': 'KR-L',
        'definition_file': 'control_staging.json', # add new translations here
        'definition_stack': [ # use these dictionaries to do that
            'enter_hotkeys.py'  # KROL/A* -> {#Control(A)}, etc.
        ] + mainStack,
        'stack': [
            'control_staging.json',
            'control.json',  # keyboard shortcuts as common words!
            'basic_commands.json',
            'numbered_commands.py',  # desktops / tabs with numbers
            'no_untranslates.py'  # translate untranslates into no-ops
        ],
        'transitions': {
            'WREU': '{STACKER:TEXT_INPUT}',
            'AFL': '{#Command(Space)}{STACKER:TEMP_TEXT}{^}',
            'WREU': '{STACKER:TEMP_TEXT}'
        }
    },

    # for entering text
    'TEXT': {
        'name': 'T-T',
        'definition_file': 'staging.json',
        'stack': mainStack,
    },

    # for entering one line of text
    'TEMP_TEXT': {
        'definition_file': 'staging.json',
        'stack': mainStack,
        'transitions': {
            'R-R': '{^\n^}{STACKER:CONTROL}',
            'TPEFBG': '{#Escape}{STACKER:CONTROL}'
        }
    },

    # pretend to have no dictionaries
    'RAW': {
        'name': 'RA*U',
        'stack': [],
    }
}
