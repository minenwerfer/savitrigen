from dataclasses import dataclass
from .backend import BackendConfig

@dataclass
class ProjectConfig(object):
    meta:dict

    plugins:list[str]
    backend:BackendConfig
