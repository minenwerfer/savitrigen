from savitrigen.tree import TreeClass
from savitrigen.config import FrontendConfig
import os

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
