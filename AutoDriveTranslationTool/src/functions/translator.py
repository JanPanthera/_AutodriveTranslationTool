# AutoDriveTranslationTool/src/functions/translator.py

import os
import re

from AutoDriveTranslationTool.src.core.constants import LOGGER_NAME
from AutoDriveTranslationTool.src.utilities.func_helpers import output

from GuiFramework.utilities.logging import Logger

# changesg we mande:
# we now get a list of tuples containing the input file name and path
# example: [('AutoDrive_config.xml', 'C:\\__JanPanthera__\\_Workspace\\_VS-Studio\\_Projects\\_PythonWorkspace\\_AutoDriveTranslationTool\\AutoDriveTranslationTool\\_input\\map_name\\AutoDrive_config.xml')]

# we now get a list of tuples containing the dictionary file name and path
# example: [('Dictionary_Global.dic', 'C:\\__JanPanthera__\\_Workspace\\_VS-Studio\\_Projects\\_PythonWorkspace\\_AutoDriveTranslationTool\\AutoDriveTranslationTool\\_dictionaries\\Global\\Dictionary_Global.dic')]
# the dictionary files are inside a folder named after the language, we use the same folder for the output


class Translator:
    def __init__(self, input_files, dictionaries, output_path,
                 output_widget=None, progress_bar=None,
                 whole_word=False, localization_manager=None):
        self.logger = Logger.get_logger(LOGGER_NAME)
        self.input_files = input_files  # list of tuples containing the input file name and path
        self.dictionaries_path = dictionaries  # list of tuples containing the dictionary file name and path
        self.dictionaries = self._create_merged_dictionaries()  # {language: {source_text: target_text}}
        self.output_path = output_path
        self.output_widget = output_widget
        self.progress_bar = progress_bar
        self.whole_word = whole_word

        self.loc = localization_manager.localize
        self.loc_param = localization_manager.localize_with_params

        self._translate_files()

    def _create_merged_dictionaries(self):
        merged_dictionaries = {}
        for dictionary_name, dictionary_path in self.dictionaries_path:
            language = os.path.basename(os.path.dirname(dictionary_path))
            if language not in merged_dictionaries:
                merged_dictionaries[language] = {}
            with open(dictionary_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith('###*') or line.endswith('*###') or not line:
                        continue
                    parts = line.split(",", maxsplit=1)
                    if len(parts) == 2:
                        source_text, target_text = parts
                        merged_dictionaries[language][source_text] = target_text
        return merged_dictionaries

    # new
    def _translate_files(self):
        total_files = len(self.input_files)
        total_translations = sum(len(dictionary) for _, dictionary in self.dictionaries.items())
        total_operations = total_files * total_translations
        current_operation = 0

        if self.progress_bar:
            self.progress_bar.set(0)  # Initialize progress bar to 0%

        for file_index, (file_name, input_file_path) in enumerate(self.input_files):
            current_operation = self._translate_file(file_name, input_file_path, total_operations, current_operation)

    def _translate_file(self, file_name, input_file_path, total_operations, current_operation):
        for language, dictionary in self.dictionaries.items():
            output_dir_path = os.path.join(self.output_path, language, os.path.dirname(os.path.relpath(input_file_path, os.path.dirname(input_file_path))))
            os.makedirs(output_dir_path, exist_ok=True)
            output_file_path = os.path.join(output_dir_path, file_name)

            with open(input_file_path, 'r', encoding='utf-8') as file:
                file_text = file.read()

            for source_text, target_text in dictionary.items():
                if self.whole_word:
                    pattern = re.compile(r'\b' + re.escape(source_text) + r'\b')
                else:
                    pattern = re.compile(re.escape(source_text), flags=re.IGNORECASE)
                file_text, _ = re.subn(pattern, target_text, file_text)
                current_operation += 1  # Increment operation count after each translation
                if self.progress_bar:
                    self.progress_bar.set(current_operation / total_operations)  # Update progress bar after each translation
                    self.progress_bar.update()

            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(file_text)

            self._output(f"File '{file_name}' translated for '{language}' language.", message_type="info")
        return current_operation

    def _output(self, message, loc_params=(), message_type=""):
        output(message, message_type, self.loc, self.output_widget, None, self.loc_param, loc_params, self.logger)

    # old
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
        for file_name, input_file_path in self.input_files.items():
            output_dir_path = os.path.join(self.output_path, language, os.path.relpath(root, self.input_path))

            if self._process_file(input_file_path, output_dir_path, self.patterns, translation_counts):
                self._output("trn_file_translated", (os.path.join(output_dir_path, file_name)))
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

    def _translate_files_old(self):
        self._output("trn_starting_translation_process", (len(self.languages), ', '.join(self.languages)))
        # create a comma separated list of the input files
        # self.input_files is a list of tuple with the file name and path
        input_files = ", ".join([f"{file_name}" for file_name, _ in self.input_files])
        self._output("trn_input", (input_files))
        self._output("trn_output", (self.output_path))

        if self.whole_word:
            self._output("trn_whole_word_enabled", "loc")
        else:
            self._output("trn_whole_word_disabled", "loc")

        # self.dictionaries {language: {source_text: target_text}}

        for language in self.dictionaries:
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
