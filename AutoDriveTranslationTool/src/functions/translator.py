# AutoDriveTranslationTool/src/functions/translator.py

import os
import re
import time
from datetime import timedelta
import xml.etree.ElementTree as ET

# Logger for debugging
from AutoDriveTranslationTool.src.core.constants import LOGGER_NAME
from GuiFramework.utilities.logging import Logger


class Translator:
    class TranslationStats:
        def __init__(self):
            """Initialize translation statistics."""
            self.total_files_translated = 0
            self.total_translations_made = 0
            self.avg_translations_per_file = 0
            self.total_time_taken = 0

            self.unique_words_translated = set()
            self.translations_per_file = {}
            self.translations_per_word = {}
            self.translations_per_language = {}

        def increment_translations(self, source_text):
            """Increment the count of translations made."""
            self.total_translations_made += 1
            self.translations_per_word[source_text] = self.translations_per_word.get(source_text, 0) + 1
            self.unique_words_translated.add(source_text)

    def __init__(self, input_files, dictionaries, output_path, output_widget=None, console_output=False, progress_bar=None, whole_word=False, localization_manager=None):
        """Initialize the translator and start the translation process."""
        start_time = time.time()
        self.logger = Logger.get_logger(LOGGER_NAME)
        self.input_files = input_files
        self.dictionaries_path = dictionaries
        self._validate_input_files()
        self._validate_dictionaries()
        self.output_path = output_path
        self.output_widget = output_widget
        if self.output_widget:
            self.output_widget.clear_console()
        self.console_output = console_output
        self.progress_bar = progress_bar
        if self.progress_bar:
            self.progress_bar.set(0)
        self.whole_word = whole_word
        self.loc = localization_manager.localize
        self.loc_param = localization_manager.localize_with_params
        self.dictionaries = self._create_merged_dictionaries()
        self.stats = self.TranslationStats()
        self._translate_files()
        end_time = time.time()
        self.stats.total_time_taken = end_time - start_time
        self._show_stats()

    def _translate_files(self):
        """Translate all input files using the loaded dictionaries."""
        self.stats.total_files_translated = len(self.input_files)

        total_major_steps = self.stats.total_files_translated * len(self.dictionaries.keys())
        major_step_increment = 1 / total_major_steps if total_major_steps != 0 else 0

        current_progress = 0
        if self.progress_bar:
            self.progress_bar.set(0)

        for language, dictionary in self.dictionaries.items():
            self.stats.translations_per_language[language] = 0

            for file_index, (file_name, input_file_path) in enumerate(self.input_files):
                translations_this_file = self._translate_file(file_name, input_file_path, language, dictionary)
                current_progress += major_step_increment
                if self.progress_bar:
                    self.progress_bar.set(min(current_progress, 1))
                    self.progress_bar.update()
                _file_name = os.path.join(os.path.basename(os.path.dirname(input_file_path)), file_name)
                self.stats.translations_per_file.setdefault(_file_name, {})[language] = translations_this_file
                self.stats.translations_per_language[language] += translations_this_file

        self.stats.avg_translations_per_file = self.stats.total_translations_made / self.stats.total_files_translated if self.stats.total_files_translated > 0 else 0
        if self.progress_bar:
            self.progress_bar.set(1)

    def _translate_file(self, file_name, input_file_path, language, dictionary):
        """Translate a single file and return the number of translations made."""
        translations_this_file = 0

        output_dir_path = os.path.join(self.output_path, language, os.path.basename(os.path.dirname(input_file_path)))
        os.makedirs(output_dir_path, exist_ok=True)
        output_file_path = os.path.join(output_dir_path, file_name)

        tree = ET.parse(input_file_path)
        root = tree.getroot()

        for mapmarker in root.iter('mapmarker'):
            for mm in mapmarker:
                for tag in ['name', 'group']:
                    element = mm.find(tag)
                    if element is not None and element.text:
                        for source_text, (regex, target_text) in dictionary.items():
                            new_text = regex.sub(target_text, element.text)
                            if new_text != element.text:
                                element.text = new_text
                                self.stats.increment_translations(source_text)
                                translations_this_file += 1

        _file_name = os.path.join(os.path.basename(os.path.dirname(input_file_path)), file_name)
        self.stats.translations_per_file.setdefault(_file_name, {})[language] = translations_this_file

        tree.write(output_file_path, encoding='utf-8')

        return translations_this_file

    def _show_stats(self):
        """Display translation statistics."""
        # Translation key: "trn_translation_summary": "Translation Summary:"
        self._output("trn_translation_summary")
        # Translation key: "trn_total_files_translated": "- Total files translated: {0}"
        self._output("trn_total_files_translated", self.stats.total_files_translated)
        # Translation key: "trn_total_translations_made": "- Total translations made: {0}"
        self._output("trn_total_translations_made", self.stats.total_translations_made)
        # Translation key: "trn_avg_translations_per_file": "- Average translations per file: {0:.2f}"
        self._output("trn_avg_translations_per_file", self.stats.avg_translations_per_file)
        # Translation key: "trn_unique_words_translated": "- Unique words translated: {0}"
        self._output("trn_unique_words_translated", len(self.stats.unique_words_translated))
        # Translation key: "trn_total_time_taken": "- Total time taken: {0}"
        self._output("trn_total_time_taken", timedelta(seconds=self.stats.total_time_taken))

        # Translation key: "trn_file_based_statistics": "\nFile-based Statistics:"
        self._output("trn_file_based_statistics")
        current_file = None
        for file, translations_by_language in self.stats.translations_per_file.items():
            if file != current_file:
                # Translation key: "trn_file_translations": "{0}:"
                self._output("trn_file_translations", file, prefix='  -')
                current_file = file
            for language, translations in translations_by_language.items():
                # Translation key: "trn_file_language_translations": "- {0} translations in {1}"
                self._output("trn_file_language_translations", translations, language, prefix='    -')

        # Translation key: "trn_translation_based_statistics": "\nTranslation-based Statistics (Top 5):"
        self._output("trn_translation_based_statistics")
        sorted_translations = sorted(self.stats.translations_per_word.items(), key=lambda item: item[1], reverse=True)[:5]
        for word, count in sorted_translations:
            # Translation key: "trn_word_translation_count": "- {0}: {1} times"
            self._output("trn_word_translation_count", word, count)

        # Translation key: "trn_language_based_statistics": "\nLanguage-based Statistics:"
        self._output("trn_language_based_statistics")
        for language, count in self.stats.translations_per_language.items():
            # Translation key: "trn_language_translation_count": "- {0}: {1} translations"
            self._output("trn_language_translation_count", language, count)

    def _output(self, message, *args, **kwargs):
        """Output a message to the console or the output widget."""
        auto_new_line = kwargs.get('auto_new_line', True)
        prefix = kwargs.get('prefix', '')

        final_message = self.loc_param(message, *args) if args and self.loc_param else self.loc(message) if self.loc else message

        final_message = f"{prefix} {final_message}"
        final_message += '\n' if auto_new_line else ''

        if self.output_widget:
            self.output_widget.write_console(final_message)

        if self.console_output:
            print(final_message, end='')
            
    def _validate_input_files(self):
        """Validate the input files to ensure they are XML files."""
        for file_name, input_file_path in self.input_files:
            if not input_file_path.endswith('.xml'):
                self.input_files.remove((file_name, input_file_path))
                self.logger.log_error(f"Input file '{input_file_path}' is not an XML file.", module_name='Translator')
                # Translation key: "trn_error_invalid_input_file": "Input file '{0}' is not an XML file."
                self._output("trn_error_invalid_input_file", input_file_path)
            try:
                ET.parse(input_file_path)
            except ET.ParseError as e:
                self.input_files.remove((file_name, input_file_path))
                self.logger.log_error(f"Error parsing XML file '{input_file_path}': {e}", module_name='Translator')
                # Translation key: "trn_error_parsing_xml_file": "Error parsing XML file '{0}': {1}"
                self._output("trn_error_parsing_xml_file", input_file_path, e)
                
    def _validate_dictionaries(self):
        """Validate the dictionaries to ensure they are .dic files."""
        for dictionary_name, dictionary_path in self.dictionaries_path:
            if not dictionary_path.endswith('.dic'):
                self.dictionaries_path.remove((dictionary_name, dictionary_path))
                self.logger.log_error(f"Dictionary '{dictionary_path}' is not a .dic file.", module_name='Translator')
                # Translation key: "trn_error_invalid_dictionary": "Dictionary '{0}' is not a .dic file."
                self._output("trn_error_invalid_dictionary", dictionary_path)

    def _create_merged_dictionaries(self):
        """Merge dictionaries from provided paths into a single dictionary."""
        merged_dictionaries = {}
        in_comment_block = False
        for dictionary_name, dictionary_path in self.dictionaries_path:
            language = os.path.basename(os.path.dirname(dictionary_path))
            merged_dictionaries.setdefault(language, {})
            with open(dictionary_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith('###*'):
                        in_comment_block = True
                    elif line.endswith('*###'):
                        in_comment_block = False
                    if in_comment_block or not line:
                        continue
                    parts = line.split(",", maxsplit=1)
                    if len(parts) == 2:
                        source_text, target_text = parts
                        regex_pattern = r'\b' + re.escape(source_text) + r'\b' if self.whole_word else re.escape(source_text)
                        regex_object = re.compile(regex_pattern, flags=re.IGNORECASE)
                        merged_dictionaries[language][source_text] = (regex_object, target_text)
        return merged_dictionaries
