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
        'name': 'KR-L', # you can switch to this state with this chord
        'definition_file': 'control_staging.json', # TKUPT adds entries here
        'definition_stack': [ # use these dictionaries to write translations
            'enter_hotkeys.py'  # KROL/A* -> {#Control(A)}, etc.
        ] + mainStack,
        'stack': [ # the stack of dictionaries in this mode
            'control_staging.json',
            'control.json',  # keyboard shortcuts as common words!
            'basic_commands.json',
            'numbered_commands.py',  # desktops / tabs with numbers
            'no_untranslates.py'  # translate untranslates into no-ops
            # you can't write text in this mode! press T-T to switch to text mode
        ],
        'transitions': {
            'WREU': '{STACKER:TEXT_INPUT}',
            'AFL': '{#Command(Space)}{STACKER:TEMP_TEXT}{^}', # open Alfred to run a command. when we press enter, return to control mode.
            'WREU': '{STACKER:TEMP_TEXT}'
        }
    },

    # a mode for entering text
    'TEXT': {
        'name': 'T-T',
        'definition_file': 'staging.json',
        'stack': mainStack,
    },

    # for entering one line of text; returns to control mode when finished
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
