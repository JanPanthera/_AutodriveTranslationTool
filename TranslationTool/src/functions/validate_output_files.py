import os
import re

class Validator:
    def __init__(self, input_path="TranslationTool/_output", languages="", output_widget=None, logger=None, console=False):
        self.input_path = os.path.normpath(input_path)
        self.languages = languages.split(',') if isinstance(languages, str) else languages
        self.output_widget = output_widget
        self.logger = logger
        self.console = console

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

    def _validate_output_file(self, file_path, errors):
        with open(file_path, 'r', encoding='utf-8') as file:
            file_text = file.read()

        if not file_text.strip():
            errors.append(("File is empty or only contains whitespace.", 0))
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
                        error_message = f"Line {line_no}: \"{text_inside_tag}\" exceeds max length of ({len(text_inside_tag)}/{max_length} characters). <{tag_name}>"
                        errors.append((error_message, line_no))

    def validate_output_files(self):
        self._output(f"Starting validation process for {len(self.languages)} languages: {', '.join(self.languages)}.\n")
        self._output(f"Input: {self.input_path}")

        for language in self.languages:
            self._output(f"\nValidation results for {language}:")
            language_path = os.path.join(self.input_path, language)
            if not os.path.exists(language_path):
                self._output(f"- {os.path.normpath(language)}\\: No files found for validation.")
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
                        self._output(f"    - Total errors: {len(file_errors)}")
                        for error_message, _ in file_errors:
                            self._output(f"        - {error_message}")
                    else:
                        if not has_files_with_errors:
                            self._output(f"- {normalized_relative_root}\\:")
                            has_files_with_errors = True
                        self._output(f"  - {file}: OK")

        self._output("\nReview the errors above and adjust your XML content to meet the length requirements for <name> and <group> tags.\n")
        self._output("Validation process finished.")
