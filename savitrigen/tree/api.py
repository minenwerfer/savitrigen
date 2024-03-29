from savitrigen import __version__
from savitrigen.tree import TreeClass
from savitrigen.schema import dataclass_to_dict, ApiSchema
from savitrigen.util import map_fields, make_ts_typehints, extract_collections
from savitrigen.template.api import (
    ControllerTemplate,
    ModelTemplate,
    DocumentImportTemplate,
    CommonDocumentImportTemplate,
    ReferenceImportTemplate,
    IndexTemplate,
    PluginImportTemplate,
    PluginInstanceTemplate
)

@TreeClass('api')
class ApiTree():
    def __init__(self, schema:ApiSchema):
        super().__init__()

        self._schema = schema
        self._unused_keys = [
            'translation',
            'documentation'
        ]

        self._common_collections = [
            'user',
            'file'
        ]

    def create(self):
        if not self.on_cache:
            self.copy_file('sample.env', '.env')

        provide = self._json_dumps({
            'apiConfig': dataclass_to_dict(self._schema.config, convert_casing=True)
        })

        self.write_file('index.ts', IndexTemplate, {
            'provide': provide,
            'module_imports': self._multiline_replace(
                self._schema.plugins,
                PluginImportTemplate,
                lambda _ : {
                    'capitalized': self._capitalize(_.split('-')[-1]),
                    'plugin_collection': _
                },
            ),
            'module_instances': self._multiline_replace(
                self._schema.plugins,
                PluginInstanceTemplate,
                lambda _ : {
                    'capitalized': ' '*2 + self._capitalize(_.split('-')[-1])
                }
            )
        })

        for k, v in self._schema.collections.items():
            self.create_collection(k, v)

    def create_build_json(self):
        content = self.json_dumps({})
        self.write_file('build.json', content)

    def create_collection(self, name:str, _description:dict):
        """Creates collections

        Each module is supposed to contain 3 files:
            - index.json
            - moduleName.controller.ts
            - moduleName.model.ts

        Will also add a description to the controller file that may contain JSDoc symbols.
        """
        path = self.make_dir('collections/{}'.format(name))

        description = dataclass_to_dict(_description, convert_casing=True)
        documentation = description.get('documentation').strip()

        fields = _description.fields
        mapped_fields = map_fields(fields) if fields else {}

        collections = list(extract_collections(fields)) if fields else {}
        collections_names = [ collection[0] for collection in collections ]

        for k in self._unused_keys:
            if k in description:
                del description[k]

        common_params = {
            'documentation': documentation,
            'savitrigen_version': __version__,
            'copyright': self._schema.meta.owner
        }

        model_params = common_params | {
            'camel_case': self._camel_case(name),
            'pascal_case': self._pascal_case(name),
            'type_hints': make_ts_typehints(mapped_fields),
            **({
                'document_imports': self._multiline_replace(
                    collections_names,
                    lambda _ : CommonDocumentImportTemplate \
                        if _ in self._common_collections \
                        else DocumentImportTemplate,
                    lambda _ : {
                        'pascal_case': self._pascal_case(_),
                        'camel_case': self._camel_case(_)
                    }
                ),
                'reference_imports': self._multiline_replace(
                    collections_names,
                    lambda _ : ReferenceImportTemplate \
                        if _ not in self._common_collections \
                        else None,
                    lambda _ : {
                        'camel_case': self._camel_case(_),
                    }
                ),

            } if len(collections) > 0 else {})
        }

        controller_params = common_params | {
            'model_pascal_case': self._pascal_case(description.get('alias', name)),
            'pascal_case': self._pascal_case(name),
            'model_path': (lambda _ : '../{}/{}.model'.format(_, _))(self._camel_case(description['alias'])) \
                if description.get('alias') \
                else './{}.model'.format(self._camel_case(name))
        }

        with self.change_dir(path):
            self.write_file('index.json', self._json_dumps(description), patch=False)
            self.write_file('{}.controller.ts'.format(name), ControllerTemplate, controller_params)

            if not description.get('alias'):
                self.write_file('{}.model.ts'.format(name), ModelTemplate, {
                    'document_imports': '// no document imports',
                    'reference_imports': '// no reference imports',
                }, model_params)


