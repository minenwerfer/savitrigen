import os
import subprocess
import yaml
from pathlib import Path

from savitrigen.schema import CodegenSchema

class Bootstrap():
    @staticmethod
    def clone_repo(config:CodegenSchema):
        cwd = Path('source')
        if not Path(cwd / Path('.gitignore')).exists():
            process = subprocess.Popen([
                'git',
                'clone',
                config.boilerplate_repo_url,
                str(cwd)
            ])

            stdout, stderr = process.communicate()

        return cwd

    @staticmethod
    def install():
        if not Path(Path.cwd() / Path('source/node_modules')).exists():
            os.system('cd source && npm install')


