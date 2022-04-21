from savitrigen.tree import TreeClass
from savitrigen.backendconfig import BackendConfig

@TreeClass('backend')
class BackendTree(Tree):
    def __init__(self, config:BackendConfig):
        self._config = config

    def create_build_json(self):
        content = self.json_dumps({})
        self.path.write_file('packages/backend/build.json', content)


