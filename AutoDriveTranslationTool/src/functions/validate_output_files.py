# validate_output_files.py

import os
import re
from AutoDriveTranslationTool.src.utilities.func_helpers import output


class Validator:
    def __init__(self, input_path, languages, output_widget=None, localization_manager=None, logger=None, console=False):
        self.input_path = os.path.normpath(input_path)
        self.languages = languages.split(',') if isinstance(languages, str) else languages
        self.output_widget = output_widget
        self.logger = logger
        self.console = console

        self.loc = localization_manager.localize
        self.loc_param = localization_manager.localize_with_params

        self._validate_output_files()

    def _output(self, message, loc_params=None, message_type=""):
        output(message, message_type, self.loc, self.output_widget, self.console, self.loc_param, loc_params, self.logger)

    def _validate_output_file(self, file_path, errors):
        with open(file_path, 'r', encoding='utf-8') as file:
            file_text = file.read()

        if not file_text.strip():
            errors.append((self.loc("vof_file_empty", 0)))
            return False

        validation_rules = [
            (r'<name>(.*?)<\/name>', 30, 'name'),
            (r'<group>(.*?)<\/group>', 20, 'group')
        ]

        for line_no, line in enumerate(file_text.splitlines(), start=1):
            for pattern, max_length, tag_name in validation_rules:
                matches = re.findall(pattern, line)
                for text_inside_tag in matches:
                    if len(text_inside_tag) > max_length:
                        error_message = self.loc_param("vof_line_exceeds_max_length", line_no, text_inside_tag, max_length, tag_name)
                        errors.append((error_message, line_no))

    def _validate_output_files(self):
        self._output("vof_starting_validation", (len(self.languages), ', '.join(self.languages)))
        self._output("vof_input", (self.input_path))

        for language in self.languages:
            self._output("vof_validating_language", (language))
            language_path = os.path.join(self.input_path, language)
            if not os.path.exists(language_path):
                self._output("vof_language_not_found", (os.path.normpath(language)), "error")
                continue

            for root, _, files in os.walk(language_path):
                relative_root = os.path.relpath(root, self.input_path)
                normalized_relative_root = os.path.normpath(relative_root)
                has_files_with_errors = False

                for file in files:
                    file_path = os.path.join(root, file)
                    file_errors = []
                    self._validate_output_file(file_path, file_errors)

                    if file_errors:
                        if not has_files_with_errors:
                            self._output(f"- {normalized_relative_root}\\:")
                            has_files_with_errors = True
                        self._output(f"  - {file}:")
                        self._output("vof_file_errors", (len(file_errors)))
                        for error_message, _ in file_errors:
                            self._output(f"        - {error_message}")
                    else:
                        if not has_files_with_errors:
                            self._output(f"- {normalized_relative_root}\\:")
                            has_files_with_errors = True
                        self._output(f"  - {file}: OK")

        self._output("vof_validation_finished_info")
        self._output("vof_validation_finished")
