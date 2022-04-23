import re

MODULE_NAMING = [
    (lambda name: re.match(r'^[0-9]', name), 'module name cannot start with a number'),
    (lambda name: re.match(r'[A-Z]', name), 'module name must use snake_case'),
    (lambda name: name[-1:] == 's' and name[-2:] != 's', 'module name must be in singular')
]

FIELD_NAMING = [
    (lambda name: re.match(r'^[0-9]', name), 'field name cannot start with a number'),
    (lambda name: re.match(r'[A-Z]', name), 'field name must use snake_case'),
]

def check(test, message, subject) -> None:
    if test(subject):
        raise TypeError('{}: {}'.format(message, subject))

def check_module_naming(name:str) -> None:
    for t in MODULE_NAMING:
        check(*t, name)

def check_field_naming(name:str) -> None:
    for t in FIELD_NAMING:
        check(*t, name)
