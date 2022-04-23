from functools import reduce
from string import Template
from savitrigen.tree import TreeClass
from savitrigen.config import BackendConfig
from savitrigen.util import map_fields, make_ts_typehints, extract_modules
from savitrigen.template.backend import (
    ControllerTemplate,
    ModelTemplate,
    DocumentImportTemplate,
    ReferenceImportTemplate
)

@TreeClass('backend')
class BackendTree():
    def __init__(self, config:BackendConfig):
        self._config = config
        self._unused_keys = [
            'translation',
            'documentation'
        ]

    def _document_imports(self, modules:list) -> str:
        def reducer(a:str, _tuple:tuple) -> str:
            name, _ = _tuple
            return a + [DocumentImportTemplate.substitute(
                pascal_case=self._pascal_case(name),
                camel_case=self._camel_case(name)
            )]

        return "\n".join(reduce(reducer, modules, []))\

    def _reference_imports(self, modules:list) -> str:
        def reducer(a:str, _tuple:tuple) -> str:
            name, _ = _tuple
            return a + [ReferenceImportTemplate.substitute(
                camel_case=self._camel_case(name)
            )]
        return "\n".join(reduce(reducer, modules, [])) \

    def create(self):
        for k, v in self._config.modules.items():
            self.create_module(k, v)

    def create_build_json(self):
        content = self.json_dumps({})
        self.write_file('build.json', content)

    def create_module(self, name:str, _description:dict):
        """Creates modules

        Each module is supposed to contain 3 files:
            - index.json
            - moduleName.controller.ts
            - moduleName.model.ts

        Will also add a description to the controller file that may contain JSDoc symbols.
        """
        path = self.make_dir('modules/{}'.format(name))

        description = dict(module=name) | _description.__dict__
        documentation = description.get('documentation').strip()

        fields = description.get('fields')
        mapped_fields = map_fields(fields)

        modules = list(extract_modules(fields))

        for k in self._unused_keys:
            if k in description:
                del description[k]

        params = {
            'pascal_case': self._pascal_case(name),
            'camel_case': self._camel_case(name),
            'documentation': documentation,
            'type_hints': make_ts_typehints(mapped_fields),
            **({
                'document_imports': self._document_imports(modules),
                'reference_imports': self._reference_imports(modules),

            } if len(modules) > 0 else {})
        }

        controller_content = ControllerTemplate.substitute(**params)

        model_content = ModelTemplate.substitute({
            'document_imports': '// no document imports',
            'reference_imports': '// no reference imports',
        }, **params)

        with self.change_dir(path):
            self.write_file('index.json', self._json_dumps(description))
            self.write_file('{}.controller.ts'.format(name), controller_content)
            self.write_file('{}.model.ts'.format(name), model_content)


