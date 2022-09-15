from dataclasses import dataclass, field

@dataclass
class WebConfig(object):
    signup_form:bool = None
    releases:bool = None
    feedback:bool = None

@dataclass
class WebSchema(object):
    meta:dict
    collections:list[str]
    default_locale:str

    menu_schema:dict
    config:WebConfig
    _config:dict = field(init=False, repr=False)

    plugins:list[str] = None


    @property
    def config(self) -> dict:
        return self._config

    @config.setter
    def config(self, value:dict) -> None:
        self._config = WebConfig(**value)
