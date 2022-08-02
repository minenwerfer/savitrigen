import json
from contextlib import suppress
from string import Template
from savitrigen.tree import TreeClass
from savitrigen.schema import FrontendSchema
from savitrigen.template.frontend import (
    IndexTemplate,
    ModuleIndexTemplate,
    RouterTemplate,
    StoreTemplate,
    PluginImportTemplate,
    PluginInstanceTemplate,
    LocaleImportTemplate,
    InternalRouterTemplate,
    InternalHomeComponentTemplate
)

@TreeClass('frontend')
class FrontendTree():
    def __init__(self, schema:FrontendSchema):
        super().__init__()
        self._schema = schema

    def create(self):
        self.create_build_json()
        self.create_module('internal', router_tpl=InternalRouterTemplate)

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
            'menu_entries': self._multiline_replace(
                self._schema.collections.keys(),
                Template(' '*8 + "'dashboard-${collection_name}',"),
                lambda _ : {
                    'collection_name': _
                }
            )
        })

        for locale, table in translation_table.items():
            self.update_i18n(locale, table)

        with self.change_dir('modules/internal'):
            self.make_dir('components/dashboard/c-home')
            self.write_file('components/dashboard/c-home/c-home.vue', InternalHomeComponentTemplate, {})


    def create_build_json(self):
        content = self._json_dumps({
            'name': '',
            'externals': {
                'variables': {
                    'productName': self._schema.meta.product.name,
                    'productLogo': 'logo.png',
                    'productLogoAlt': 'logo-alt.png',
                    'releases': self._schema.has_releases,
                    'notification': self._schema.has_notification,
                    'feedback': self._schema.has_feedback,
                }
            }
        })

        self.write_file('build.json', content)

    def create_module(self, name:str, router_tpl=None):
        path = self.make_dir('modules/{}'.format(name))

        store_path = self.make_dir('modules/{}/store'.format(name))
        components_path = self.make_dir('modules/{}/components'.format(name))

        with self.change_dir(path):
            self.write_file('index.ts', ModuleIndexTemplate, {})
            self.write_file('router.ts', router_tpl or RouterTemplate, {})
            self.write_file('store/index.ts', StoreTemplate, {})

    def update_i18n(self, locale:str, new_table):
        path = self.make_dir('i18n/{}'.format(locale))
        table = {}

        with self.change_dir(path):
            with suppress(FileNotFoundError):
                index_content = self.read_file('index.json')
                table = json.loads(index_content)

            table |= new_table
            self.write_file('index.json', self._json_dumps(table))
