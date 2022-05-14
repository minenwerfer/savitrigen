#!/usr/bin/env python3

_REQUIRED_EXECUTABLES = [
    'npm',
    'node',
    'nodemon',
    'ts-node'
]

_MISSING_EXECUTABLE_ERROR = """The following executables are required to be accessible through $$PATH in order to run this program:
{}

The following one is missing: {}
"""

class MissingExecutableException(Exception):
    def __init__(self, missing:str):
        self.missing = missing
    def __str__(self):
        return _MISSING_EXECUTABLE_ERROR.format(
            ', '.join(_REQUIRED_EXECUTABLES),
            self.missing
        )

if __name__ == '__main__':
    import shutil
    import sys

    try:
        for n in _REQUIRED_EXECUTABLES:
            if shutil.which(n) is None:
                raise MissingExecutableException(n)
    except MissingExecutableException as e:
        print(e)
        sys.exit(1)

    from savitrigen.commandline import main
    main()
