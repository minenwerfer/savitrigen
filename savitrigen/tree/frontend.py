from savitrigen.tree import TreeClass
from savitrigen.config import FrontendConfig
from savitrigen.template.frontend import (
    IndexTemplate,
    RouterTemplate,
    StoreTemplate
)

@TreeClass('frontend')
class FrontendTree():
    def __init__(self, config:FrontendConfig):
        self._config = config

    def create_build_json(self):
        content = self._json_dumps({
            'name': '',
            'externals': {
                'variables': {
                    'productName': self._config.product_name,
                    'productLogo': self._config.product_logo,
                    'productLogoAlt': self._config.product_logo_alt,
                    'releases': self._config.has_releases,
                    'notification': self._config.has_notification,
                    'feedback': self._config.has_feedback,

                }
            }
        })

        self.write_file('build.json', content)


    def create_module(self, name:str):
        path = self.make_dir('modules/{}'.format(name))

        store_path = self.make_dir('modules/{}/store'.format(name))
        components_path = self.make_dir('modules/{}/components'.format(name))

        index_content = IndexTemplate.substitute()
        router_content = RouterTemplate.substitute()
        store_content = StoreTemplate.substitute()

        with self.change_dir(path):
            self.write_file('index.ts', index_content)
            self.write_file('router.ts', router_content)
            self.write_file('store/index.ts', store_content)
