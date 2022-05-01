from dataclasses import dataclass

@dataclass
class FrontendConfig(object):
    notice:str = None
    signin_text:str = None

    has_releases:bool = False
    has_feedback:bool = False
    has_notification:bool = False
