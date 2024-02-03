# localization.py
import gettext

def setup_localization(locale_dir='locales', language='en'):
    """
    Set up localization for the application.

    :param locale_dir: Directory where the localization files are stored.
    :param language: Language code to use for localization.
    """
    localedir = locale_dir
    lang = gettext.translation('messages', localedir=localedir, languages=[language], fallback=True)
    lang.install()
