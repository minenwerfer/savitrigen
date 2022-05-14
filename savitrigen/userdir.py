import shutil
import os
from pathlib import Path

"""Usually ~/.savitrigen"""
CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.savitrigen')

"""Path that holds package files"""
SCRIPT_PATH = '/'.join(os.path.realpath(__file__).split('/')[:-1])

def make_userdir():
    config_path = Path(CONFIG_PATH)

    if not config_path.exists():
        config_path.mkdir(exist_ok=True)

    def copy_to_userdir(fname: str):
        return shutil.copytree(
            '{}/{}'.format(os.path.join(SCRIPT_PATH, '..'), fname),
            '{}/{}'.format(CONFIG_PATH, fname.split('/')[-1]),
            dirs_exist_ok=True
        )

    copy_to_userdir('config')
    copy_to_userdir('presets')


def copy_from_userdir(fname:str, dest:str, exist_ok:bool=False):
    if not exist_ok and Path(dest).exists():
        raise Exception('existing file')

    return shutil.copyfile(
        '{}/{}'.format(CONFIG_PATH, fname),
        dest
    )

def get_presets():
    directory = Path(CONFIG_PATH) / Path('presets')
    for f in directory.glob('*.yml'):
        yield f.name.split('.yml')[0]
