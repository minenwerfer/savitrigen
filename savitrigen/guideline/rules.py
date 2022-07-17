import re

COLLECTION_NAMING = [
    (lambda name: re.search(r'^[0-9]', name), 'collection name cannot start with a number'),
    (lambda name: re.search(r'^[A-Z]', name), 'collection name must use camelCase'),
    (lambda name: name[-1:] == 's' and name[-2:] != 's', 'collection name must be in singular')
]

FIELD_NAMING = [
    (lambda name: re.search(r'^[0-9]', name), 'field name cannot start with a number'),
    (lambda name: re.search(r'[A-Z]', name), 'field name must use snake_case'),
]

PLUGIN_NAMING = [
    (
        lambda name: not re.search(r'plugin-([a-z]+)$', name),
        'collection must follow "plugin-name" format'
    )
]
