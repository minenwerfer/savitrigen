from dataclasses import dataclass

@dataclass
class CodegenSchema(object):
    boilerplate_repo_url:str
    rules:dict
