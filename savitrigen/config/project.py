from dataclasses import dataclass, field
from .backend import BackendConfig
from .frontend import FrontendConfig

from savitrigen.guideline import check_plugin_naming

@dataclass
class ProjectConfig(object):
    meta:dict
    plugins:list[str]
    _plugins:list[str] = field(init=False, repr=False)

    backend:BackendConfig = None
    frontend:FrontendConfig = None

    @property
    def plugins(self) -> list[str]:
        return self._plugins

    @plugins.setter
    def plugins(self, plugins:list[str]) -> None:
        if not isinstance(plugins, list):
            self._plugins = []
            return

        for p in plugins:
            check_plugin_naming(p)

        self._plugins = plugins
