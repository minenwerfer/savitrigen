import yaml

import savitrigen.logging
from savitrigen.userdir import CONFIG_PATH, copy_from_userdir, get_presets
from savitrigen.tree.frontend import FrontendTree
from savitrigen.tree.backend import BackendTree
from savitrigen.tree.project import ProjectTree
from savitrigen.bootstrap import Bootstrap
from savitrigen.cache import Cache
from savitrigen.source import Source
from savitrigen.config import (
    CodegenConfig,
    ProjectConfig,
    BackendConfig,
    FrontendConfig
)

def main():
    """Main code generation routine"""
    with open('{}/{}'.format(CONFIG_PATH, 'config.yml'), 'r') as f:
        codegen_config = CodegenConfig(**yaml.safe_load(f))

    with open('savitrigen.yml', 'r') as f:
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

    project_tree, backend_tree, frontend_tree = (
        ProjectTree(project_config),
        BackendTree(backend_config),
        FrontendTree(frontend_config)
    )

    Source().create([project_tree, backend_tree, frontend_tree])
    Cache().create([project_tree, backend_tree, frontend_tree])

    Bootstrap.install()


def preset(name:str):
    """Copies ~/.savitrigen/presets/[name].yml to current directory"""
    copy_from_userdir('presets/{}.yml'.format(name), 'savitrigen.yml')

def list_presets():
    for p in get_presets():
        print(' - {}'.format(p))

def print_version():
    from savitrigen import __version__
    print(__version__)
