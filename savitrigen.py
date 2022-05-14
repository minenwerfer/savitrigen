import yaml
import savitrigen.logging
from savitrigen.tree.frontend import FrontendTree
from savitrigen.tree.backend import BackendTree
from savitrigen.tree.project import ProjectTree
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
        backend_config = BackendConfig(
            **project_config.backend,
            plugins=project_config.plugins
        )

        frontend_config = FrontendConfig(
            **project_config.frontend,
            meta=project_config.meta,
            entities=backend_config.entities,
            plugins=project_config.plugins
        )

    Bootstrap.clone_repo(codegen_config)

    ProjectTree(project_config).create()
    BackendTree(backend_config).create()
    FrontendTree(frontend_config).create()

    Bootstrap.install()

