# translate.py

import os
import re
from src.utilities.func_helpers import output


class Translator:
    def __init__(self, input_path, output_path, dictionaries_path, languages, localization_manager=None,
                 output_widget=None, logger=None, console=False, whole_word=False):
        self.input_path = os.path.normpath(input_path)
        self.output_path = os.path.normpath(output_path)
        self.dictionaries_path = os.path.normpath(dictionaries_path)
        self.languages = languages
        self.output_widget = output_widget
        self.logger = logger
        self.console = console
        self.whole_word = whole_word

        self.loc = localization_manager.localize
        self.loc_param = localization_manager.localize_with_params

        self._translate_files()

    def _output(self, message, loc_params=(), message_type=""):
        output(message, message_type, self.loc, self.output_widget, self.console, self.loc_param, loc_params, self.logger)

    def _process_file(self, input_file_path, output_dir_path, patterns, translation_counts):
        replacements_in_file = False

        try:
            os.makedirs(output_dir_path, exist_ok=True)
            output_file_path = os.path.join(output_dir_path, os.path.basename(input_file_path))

            with open(input_file_path, 'r', encoding='utf-8') as file:
                file_text = file.read().strip()
            if not file_text:
                return False

            for pattern, target_text in patterns.items():
                new_text, count = re.subn(pattern, target_text, file_text)
                if count > 0:
                    file_text = new_text
                    translation_counts[pattern.pattern] = translation_counts.get(pattern.pattern, (0, target_text))[0] + count, target_text
                    replacements_in_file = True

            if replacements_in_file:
                with open(output_file_path, 'w', encoding='utf-8') as file:
                    file.write(file_text)
                return True

        except Exception as e:
            self._output("trn_error_translating_file", (input_file_path, e), "error")

        return False

    def _perform_translation(self, language):
        translation_counts = {}
        files_translated = 0
        files_skipped = 0

        self._output("trn_starting_translation", (language))
        self._output("trn_translating_files", "loc")
        for root, _, files in os.walk(self.input_path):
            for file in files:
                input_file_path = os.path.join(root, file)
                output_dir_path = os.path.join(self.output_path, language, os.path.relpath(root, self.input_path))

                if self._process_file(input_file_path, output_dir_path, self.patterns, translation_counts):
                    self._output("trn_file_translated", (os.path.join(output_dir_path, file)))
                    files_translated += 1
                else:
                    self._output("trn_file_skipped", (input_file_path), "warning")
                    files_skipped += 1

        if files_translated > 0:
            total_count = sum(count for count, _ in translation_counts.values())
            self._output("trn_translation_finished", (language))
            self._output("trn_translation_count", (total_count))
            for source_text, (count, target_text) in translation_counts.items():
                clean_source_text = source_text.replace(r'\b', '')
                self._output("trn_translation_summary", (clean_source_text, target_text, count))

        self._output("")

    def _translate_files(self):
        self._output("trn_starting_translation_process", (len(self.languages), ', '.join(self.languages)))
        self._output("trn_input", (self.input_path))
        self._output("trn_output", (self.output_path))

        if self.whole_word:
            self._output("trn_whole_word_enabled", "loc")
        else:
            self._output("trn_whole_word_disabled", "loc")

        for language in self.languages:
            dictionary_file_name = os.path.join(self.dictionaries_path, f"Dictionary_{language}.dic")

            if not os.path.isfile(dictionary_file_name):
                self._output("trn_dictionary_not_found", (dictionary_file_name, language), "warning")
                continue

            with open(dictionary_file_name, 'r', encoding='utf-8') as file:
                dictionary_text = file.read()
            self.patterns = {}
            for line in dictionary_text.splitlines():
                line = line.strip()
                if line.startswith('###*') or line.endswith('*###') or not line:
                    continue

                parts = line.split(",", maxsplit=1)
                if len(parts) == 2:
                    source_text, target_text = parts
                    if self.whole_word:
                        pattern = re.compile(r'\b' + re.escape(source_text) + r'\b')
                    else:
                        pattern = re.compile(re.escape(source_text), flags=re.IGNORECASE)
                    self.patterns[pattern] = target_text

            self._perform_translation(language)

        self._output("trn_translation_process_finished", "loc")
