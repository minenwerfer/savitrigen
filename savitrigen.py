import yaml
import savitrigen.logging
from savitrigen.tree.frontend import FrontendTree
from savitrigen.tree.backend import BackendTree
from savitrigen.bootstrap import Bootstrap
from savitrigen.config import (
    CodegenConfig,
    ProjectConfig,
    BackendConfig,
    FrontendConfig
)

if __name__ == '__main__':
    with open('config.yml', 'r') as f:
        codegen_config = CodegenConfig(**yaml.safe_load(f))

    with open('tests/sample.yml', 'r') as f:
        project_config = ProjectConfig(**yaml.safe_load(f))
        backend_config = BackendConfig(**project_config.backend)

    Bootstrap.clone_repo(codegen_config)

    # frontend_config = FrontendConfig(
    #     product_name='Teste'
    # )

    # tree = FrontendTree(frontend_config)
    # tree.create_build_json()

    tree = BackendTree(backend_config)
    tree.create()
