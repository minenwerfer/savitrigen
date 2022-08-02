from savitrigen.tree import TreeClass
from savitrigen.schema.project import ProjectSchema

@TreeClass('..')
class ProjectTree():
    def __init__(self, schema:ProjectSchema):
        super().__init__()
        self._schema = schema

    def create(self):
        self.create_package_json()

    def create_package_json(self):
        dependencies = [
            '@savitri/common',
            '@savitri/backend',
            '@savitri/frontend',
            '@savitri/components',
            '@savitri/i18n-ptbr'
        ]

        dependencies += self._schema.plugins or []
        content = self._json_dumps({
            'dependencies': {
                dep: '*'
                for dep in dependencies
            }
        })

        self.write_file('package.json', content)
