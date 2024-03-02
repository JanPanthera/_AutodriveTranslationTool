# find_missing_translations.py

import os
import re
from collections import defaultdict
from src.utilities.func_helpers import output


class TranslationFinder:
    def __init__(self, input_path, output_path, dictionary_path, languages, output_widget=None, localization_manager=None, console=False, logger=None):
        self.input_path = os.path.normpath(input_path)
        self.output_path = os.path.normpath(output_path)
        self.dictionary_path = os.path.normpath(dictionary_path)
        self.languages = languages.split(',') if isinstance(languages, str) else languages
        self.output_widget = output_widget
        self.console = console
        self.loc = localization_manager.localize
        self.loc_param = localization_manager.localize_with_params
        self.logger = logger

        self._find_missing_translations()

    def _output(self, message, loc_params=None, message_type=""):
        output(message, message_type, self.loc, self.output_widget, self.console, self.loc_param, loc_params, self.logger)

    def _load_translations(self):
        translations = defaultdict(set)
        for language in self.languages:
            dictionary_file = self._get_dictionary_file(language)
            try:
                with open(dictionary_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if ',' in line:
                            word, _ = line.strip().split(',')
                            translations[language].add(word)
            except FileNotFoundError:
                self._output("fmt_dictionary_not_found", (language), "error")
        return translations

    def _get_dictionary_file(self, language):
        dictionary_file = os.path.join(self.dictionary_path, f"Dictionary_{language}.dic")
        return dictionary_file

    def _find_missing_translations_in_file(self, input_file, translations):
        word_pattern = re.compile(r'<(?:name|group)>(.*?)</(?:name|group)>')
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        words = word_pattern.findall(content)
        unique_words = set(word for phrase in words for word in phrase.split() if not word.isdigit() and re.search(r'[a-zA-Z]', word))
        missing_translations = {lang: unique_words - trans for lang, trans in translations.items()}
        return missing_translations

    def _find_missing_translations(self):
        self._output("fmt_search_missing_translations", (len(self.languages), ', '.join(self.languages)))

        translations = self._load_translations()

        for root, _, files in os.walk(self.input_path):
            for file in files:
                if file.endswith(".xml"):
                    input_file = os.path.join(root, file)
                    self._output("fmt_processing_file", (input_file))
                    missing_translations = self._find_missing_translations_in_file(input_file, translations)

                    for language, missing in missing_translations.items():
                        if missing:
                            self._output("fmt_missing_translations", (language, len(missing)))
                            for word in sorted(missing):
                                self._output(f"{word}")
                        else:
                            self._output("fmt_no_missing_translations", (language))

        self._output("")
        self._output("fmt_search_finished")
