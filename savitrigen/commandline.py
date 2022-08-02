import yaml

import savitrigen.logging
from savitrigen.userdir import CONFIG_PATH, copy_from_userdir, get_presets
from savitrigen.tree.frontend import FrontendTree
from savitrigen.tree.backend import BackendTree
from savitrigen.tree.project import ProjectTree
from savitrigen.bootstrap import Bootstrap
from savitrigen.cache import Cache
from savitrigen.source import Source
from savitrigen.schema import (
    CodegenSchema,
    ProjectSchema,
    BackendSchema,
    FrontendSchema
)

def main():
    """Main code generation routine"""
    with open('{}/{}'.format(CONFIG_PATH, 'config.yml'), 'r') as f:
        codegen_schema = CodegenSchema(**yaml.safe_load(f))

    with open('savitrigen.yml', 'r') as f:
        project_schema = ProjectSchema(**yaml.safe_load(f))
        backend_schema = BackendSchema(
            **project_schema.backend,
            meta=project_schema.meta,
            plugins=project_schema.plugins
        )

        frontend_schema = FrontendSchema(
            **project_schema.frontend,
            meta=project_schema.meta,
            collections=backend_schema.collections,
            plugins=project_schema.plugins
        )

    Bootstrap.clone_repo(codegen_schema)

    project_tree, backend_tree, frontend_tree = (
        ProjectTree(project_schema),
        BackendTree(backend_schema),
        FrontendTree(frontend_schema)
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
