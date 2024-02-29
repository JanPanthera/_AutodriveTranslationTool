# find_missing_translations.py

import os
import re


class TranslationFinder:
    def __init__(self, input_path, output_path, dictionary_path, languages, output_widget=None, localization_manager=None, console=False, logger=None):
        self.input_path = os.path.normpath(input_path)
        self.output_path = os.path.normpath(output_path)
        self.dictionary_path = os.path.normpath(dictionary_path)
        self.languages = languages.split(',') if isinstance(languages, str) else languages
        self.output_widget = output_widget
        self.console = console
        self.loc = localization_manager.translate_with_params # localization_manager can be None add error handling
        self.logger = logger

        self._find_missing_translations()

    def _output(self, message, is_error=False, is_warning=False):
        if self.logger:
            if is_error:
                self.logger.error(message)
            elif is_warning:
                self.logger.warning(message)
            else:
                self.logger.info(message)
        message = message + "\n"
        if is_error:
            message = f"ERROR: {message}"
        elif is_warning:
            message = f"WARNING: {message}"
        if self.output_widget:
            self.output_widget.write_console(message)
        if self.console:
            print(message, end='')

    def _load_translations(self):
        translations = {}
        for language in self.languages:
            dictionary_file = self._get_dictionary_file(language)
            try:
                with open(dictionary_file, 'r', encoding='utf-8') as f:
                    translations[language] = set()
                    for line in f:
                        if ',' in line:
                            word, _ = line.strip().split(',')
                            translations[language].add(word)
            except FileNotFoundError:
                self._output(f"Dictionary file for {language} not found.", is_error=True)
        return translations

    def _get_dictionary_file(self, language):
        dictionary_file = os.path.join(self.dictionary_path, f"Dictionary_{language}.dic")
        return dictionary_file

    def _find_missing_translations_in_file(self, input_file, translations):
        word_pattern = re.compile(r'<(?:name|group)>(.*?)</(?:name|group)>')
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        words = word_pattern.findall(content)
        unique_words = set([word for phrase in words for word in phrase.split()])
        missing_translations = {lang: unique_words - trans for lang, trans in translations.items()}
        return missing_translations

    def _find_missing_translations(self):
        # Prepare the dynamic data
        num_languages = len(self.languages)
        languages_str = ', '.join(self.languages)
        # Localize the message with dynamic data
        localized_message = self.loc(
            "search_missing_translations",
            num_languages=num_languages,
            languages=languages_str
        )
        self._output(localized_message)

        translations = self._load_translations()

        for root, _, files in os.walk(self.input_path):
            for file in files:
                if file.endswith(".xml"):
                    input_file = os.path.join(root, file)
                    self._output(f"Processing file: {input_file}")
                    missing_translations = self._find_missing_translations_in_file(input_file, translations)

                    for language, missing in missing_translations.items():
                        if missing:
                            self._output(f"{language} is missing {len(missing)} translations:")
                            for word in sorted(missing):
                                self._output(f"{word}")
                        else:
                            self._output(f"{language} has all words translated.")

        self._output("")
        self._output("Search for missing translations finished.")
