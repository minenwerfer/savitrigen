import os
import subprocess
import yaml
from pathlib import Path

from savitrigen.config import Config

class Bootstrap():
    @staticmethod
    def clone_repo(config:Config):
        cwd = Path('/tmp') / Path(Path.cwd().name)

        process = subprocess.Popen([
            'git',
            'clone',
            config.boilerplate_repo_url,
            str(cwd)
        ])

        stdout, stderr = process.communicate()
        os.chdir(str(cwd))
        return cwd

