# localization.py
import gettext

class LocalizationManager:
    def __init__(self, default_language='en', locale_dir='locales'):
        self.default_language = default_language
        self.locale_dir = locale_dir
        self.current_language = default_language
        self.language_mapping = {
            'English': 'en',
            'French': 'fr',
            'German': 'de',
            # Add more languages as needed
        }

    def setup_localization(self, language=None):
        """
        Set up localization for the application using the specified language.
        If no language is specified, the current language is used.
        """
        if language:
            self.current_language = language
        lang_code = self.get_language_code(self.current_language)
        lang = gettext.translation('messages', localedir=self.locale_dir, languages=[lang_code], fallback=True)
        lang.install()

    def get_language_code(self, english_name):
        """
        Retrieve the language code for the given English language name.
        """
        return self.language_mapping.get(english_name, self.default_language)

    def change_language(self, english_name):
        """
        Change the current language and re-setup localization.
        """
        self.setup_localization(english_name)