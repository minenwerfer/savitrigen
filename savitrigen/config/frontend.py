from dataclasses import dataclass

@dataclass
class FrontendConfig(object):
    product_name: str
    product_logo: str           = 'logo.png'
    product_logo_alt: str       = ''

    notice: str                 = None
    signin_text: str            = None

    has_feedback: bool          = False
    has_notification: bool      = False
    has_releases: bool          = False
