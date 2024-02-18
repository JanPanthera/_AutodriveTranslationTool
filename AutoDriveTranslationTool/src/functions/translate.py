# translate.py

import os
import re


class Translator:
    def __init__(self, input_path, output_path, dictionaries_path, languages,
                 output_widget=None, logger=None, console=False, whole_word=False):
        self.input_path = os.path.normpath(input_path)
        self.output_path = os.path.normpath(output_path)
        self.dictionaries_path = os.path.normpath(dictionaries_path)
        self.languages = languages
        self.output_widget = output_widget
        self.logger = logger
        self.console = console
        self.whole_word = whole_word

        self._translate_files()

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
            self._output(f"An error occurred while translating file '{input_file_path}': {e}", is_error=True)

        return False

    def _perform_translation(self, language):
        translation_counts = {}
        files_translated = 0
        files_skipped = 0

        self._output(f"--- Starting {language} Translation ---\n")
        self._output("Translating files...")
        for root, _, files in os.walk(self.input_path):
            for file in files:
                input_file_path = os.path.join(root, file)
                output_dir_path = os.path.join(self.output_path, language, os.path.relpath(root, self.input_path))

                if self._process_file(input_file_path, output_dir_path, self.patterns, translation_counts):
                    self._output(f"File translated: {os.path.join(output_dir_path, file)}")
                    files_translated += 1
                else:
                    self._output(f"File skipped: {input_file_path}", is_warning=True)
                    files_skipped += 1

        if files_translated > 0:
            total_count = sum(count for count, _ in translation_counts.values())
            self._output(f"\n{language} translation results:")
            self._output(f"  Translation Counts: {total_count}")
            for source_text, (count, target_text) in translation_counts.items():
                clean_source_text = source_text.replace(r'\b', '')
                self._output(f'    {clean_source_text} --> {target_text}: {count} replacements')

        self._output("")

    def _translate_files(self):
        self._output(f"Starting translation process for {len(self.languages)} languages: {', '.join(self.languages)}.\n")
        self._output(f"Input: {self.input_path}")
        self._output(f"Output: {self.output_path}\n")

        if self.whole_word:
            self._output("Whole word replacement is enabled.\n")
        else:
            self._output("Whole word replacement is disabled.\n")

        for language in self.languages:
            dictionary_file_name = os.path.join(self.dictionaries_path, f"Dictionary_{language}.dic")

            if not os.path.isfile(dictionary_file_name):
                self._output(f"Dictionary file '{dictionary_file_name}' not found. Skipping translation for {language}.\n", is_warning=True)
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

        self._output("Translation process finished.\n\n")
