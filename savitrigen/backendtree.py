from savitrigen.tree import TreeClass
from savitrigen.backendconfig import BackendConfig
import os

@TreeClass('backend')
class BackendTree():
    def __init__(self, config:BackendConfig):
        self._config = config

    def create_build_json(self):
        content = self.json_dumps({})
        self.write_file('build.json', content)

    def create_entity(self, name:str):
        path = 'modules/{}'.format(name)
        self.make_dir(path)

        with self.change_dir(path):
            self.write_file('index.json'.format(name), 'Teste')
            self.write_file('{}.controller.ts'.format(name), 'Teste')
            self.write_file('{}.model.ts'.format(name), 'Teste')


