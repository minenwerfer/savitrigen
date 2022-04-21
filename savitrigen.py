import yaml
import savitrigen.logging
from savitrigen.config import Config
from savitrigen.frontendtree import FrontendTree
from savitrigen.frontendconfig import FrontendConfig
from savitrigen.bootstrap import Bootstrap

if __name__ == '__main__':
    with open('config.yml', 'r') as f:
        global_config = Config(**yaml.safe_load(f))

    Bootstrap.clone_repo(global_config)

    frontend_config = FrontendConfig(
        product_name='Teste'
    )

    tree = FrontendTree(frontend_config)
    tree.create_build_json()
