from functools import reduce
from string import Template
from savitrigen.tree import TreeClass
from savitrigen.config import BackendConfig
from savitrigen.util import map_fields, make_ts_typehints, extract_modules
from savitrigen.template.backend import ControllerTemplate, ModelTemplate

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
            tpl = Template(r"import { ${pascal_case}Document } from '../${camel_case}/${camel_case}.model'")
            return a + [tpl.substitute(
                pascal_case=self._pascal_case(name),
                camel_case=self._camel_case(name)
            )]

        return "\n".join(reduce(reducer, modules, []))\
            if len(modules) > 0 else '// no document imports'

    def _reference_imports(self, modules:list) -> str:
        def reducer(a:str, _tuple:tuple) -> str:
            name, _ = _tuple
            tpl = Template(r"import '../${camel_case}/${camel_case}.model'")
            return a + [tpl.substitute(
                camel_case=self._camel_case(name)
            )]
        return "\n".join(reduce(reducer, modules, [])) \
            if len(modules) > 0 else '// no reference imports'

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
        path = 'modules/{}'.format(name)
        self.make_dir(path)

        description = dict(module=name) | _description
        documentation = description.get('documentation', 'undocumented').strip()

        fields = description.get('fields')
        mapped_fields = map_fields(fields)

        modules = list(extract_modules(fields))

        for k in self._unused_keys:
            if k in description:
                del description[k]

        params = dict(
            pascal_case=self._pascal_case(name),
            camel_case=self._camel_case(name),
            documentation=documentation,
            type_hints=make_ts_typehints(mapped_fields),
            document_imports=self._document_imports(modules),
            reference_imports=self._reference_imports(modules),
        )

        controller_content = ControllerTemplate.substitute(**params)
        model_content = ModelTemplate.safe_substitute(**params)

        with self.change_dir(path):
            self.write_file('index.json', self._json_dumps(description))
            self.write_file('{}.controller.ts'.format(name), controller_content)
            self.write_file('{}.model.ts'.format(name), model_content)


