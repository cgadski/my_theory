states = {
    'S': {
        'name': 'S',
        'transitions': {
            'R-R': 'S',
        }
    },
    'T': {
        'name': 'T',
        'stack': [
            'no_untranslates.py'
        ],
        'transitions': {
            'R-R': 'T',
        }
    }
}