import json
from contextlib import suppress
from string import Template
from savitrigen.tree import TreeClass
from savitrigen.schema import WebSchema, dataclass_to_dict
from savitrigen.template.web import (
    IndexTemplate,
    ModuleIndexTemplate,
    RouterTemplate,
    PluginImportTemplate,
    PluginInstanceTemplate,
    LocaleImportTemplate,
    DashboardRouterTemplate,
    DashboardHomeComponentTemplate
)

@TreeClass('web')
class WebTree():
    def __init__(self, schema:WebSchema):
        super().__init__()
        self._schema = schema

    def create(self):
        self.create_build_json()
        self.create_module('dashboard', router_tpl=DashboardRouterTemplate)

        translation_table = {}
        for collection_name, collection in [(k, v) for k, v in self._schema.collections.items() if v.translation]:
            for locale, translation in collection.translation.items():
                if locale not in translation_table:
                    translation_table[locale] = {}

                translation_table[locale] |= {
                    collection_name: translation
                }


        self.write_file('index.ts', IndexTemplate, {
            'module_imports': self._multiline_replace(
                self._schema.plugins,
                PluginImportTemplate,
                lambda _ : {
                    'capitalized': self._capitalize(_.split('-')[-1]),
                    'plugin_name': _
                }
            ),
            'module_instances': self._multiline_replace(
                self._schema.plugins,
                PluginInstanceTemplate,
                lambda _ : {
                    'capitalized': ' '*4 + self._capitalize(_.split('-')[-1])
                }
            ),
            'default_locale': self._schema.default_locale,
            'locale_imports': self._multiline_replace(
                translation_table.keys(),
                LocaleImportTemplate,
                lambda _ : {
                    'locale_key': ' '*6 + _,
                    'locale': _
                }
            ),
            'menu_schema': self._json_dumps(self._schema.menu_schema)
        })

        for locale, table in translation_table.items():
            self.update_i18n(locale, table)

        with self.change_dir('modules/dashboard'):
            self.write_file('views/home.vue', DashboardHomeComponentTemplate, {})

    def create_build_json(self):
        config = {
            'productName': self._schema.meta.product.name,
            'productLogo': 'logo.png',
            'productLogoAlt': 'logo-alt.png',
            **dataclass_to_dict(self._schema.config, convert_casing=True)
        }

        content = self._json_dumps({
            'name': '',
            'externals': {
                'variables': config
            }
        })

        self.write_file('build.json', content)

    def create_module(self, name:str, router_tpl=None):
        path = self.make_dir('modules/{}'.format(name))

        store_path = self.make_dir('modules/{}/stores'.format(name))
        components_path = self.make_dir('modules/{}/views'.format(name))

        with self.change_dir(path):
            self.write_file('index.ts', ModuleIndexTemplate, {})
            self.write_file('router.ts', router_tpl or RouterTemplate, {})

    def update_i18n(self, locale:str, new_table):
        path = self.make_dir('i18n/{}'.format(locale))
        table = {}

        with self.change_dir(path):
            with suppress(FileNotFoundError):
                index_content = self.read_file('index.json')
                table = json.loads(index_content)

            table |= new_table
            self.write_file('index.json', self._json_dumps(table), patch=False)
