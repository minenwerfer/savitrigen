from dataclasses import dataclass

@dataclass
class WebSchema(object):
    meta:dict
    collections:list[str]
    default_locale:str

    menu_schema:dict

    plugins:list[str] = None

    notice:str = None
    signin_text:str = None

    has_releases:bool = False
    has_feedback:bool = False
    has_notification:bool = False
