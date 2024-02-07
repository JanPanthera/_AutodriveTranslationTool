import os
import re

def _output(message, output_widget=None, is_error=True):
    """
    Writes the given message to the output widget or console.

    Args:
        message (str): The message to be written.
        output_widget (object, optional): The output widget to write the message to. Defaults to None.
        is_error (bool, optional): Indicates if the message is an error message. Defaults to True.
    """
    prefix = "ERROR: " if is_error else ""
    if output_widget:
        output_widget.write_console(prefix + message + "\n")
    else:
        print(prefix + message)

def _validate_output_file(file_path, errors):
    """
    Validates the content of the given file and adds any errors to the errors dictionary.

    Args:
        file_path (str): The path of the file to be validated.
        errors (dict): The dictionary to store the validation errors.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        file_text = file.read()

    if not file_text.strip():
        errors[file_path].append(("File is empty or only contains whitespace.", 0))
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
                    error_message = f"Line {line_no}: <{tag_name}> tag content exceeds max length ({len(text_inside_tag)}/{max_length} characters)."
                    errors[file_path].append((error_message, line_no))

def validate_output_files(input_path="_output", languages=None, output_widget=None):
    """
    Validates the output files in the specified input path for the given languages.

    Args:
        input_path (str, optional): The path where the output files are located. Defaults to "_output".
        languages (str or list, optional): The languages to validate. Can be a comma-separated string or a list of strings. Defaults to None.
        output_widget (object, optional): The output widget to write the validation results. Defaults to None.
    """
    if not isinstance(languages, (str, list)):
        _output("Invalid 'languages' parameter. It must be a comma-separated string or a list of strings.", output_widget, is_error=True)
        return

    languages_list = [lang.strip() for lang in languages.split(',')] if isinstance(languages, str) else languages
    _output(f"Starting validation for languages: {', '.join(languages_list)}\n", output_widget, is_error=False)

    errors = {lang: {} for lang in languages_list}

    for language in languages_list:
        language_path = os.path.join(input_path, language)
        if not os.path.exists(language_path):
            _output(f"No output path for {language}. Skipping.", output_widget, is_error=False)
            continue

        for root, dirs, files in os.walk(language_path):
            relative_root = os.path.relpath(root, language_path)  # Get the relative path from language directory
            for file in files:
                file_path = os.path.join(root, file)
                if relative_root not in errors[language]:
                    errors[language][relative_root] = {}
                if file_path not in errors[language][relative_root]:
                    errors[language][relative_root][file_path] = []
                _validate_output_file(file_path, errors[language][relative_root])

    for language, subfolders in errors.items():
        _output(f"\nValidation results for {language}:", output_widget, is_error=False)
        for subfolder, file_errors in subfolders.items():
            if any(file_errors.values()):
                _output(f"- {subfolder}:", output_widget, is_error=False)
                for file_path, error_list in file_errors.items():
                    if error_list:
                        _output(f"  - {os.path.basename(file_path)}:", output_widget, is_error=False)
                        _output(f"    - Total errors: {len(error_list)}", output_widget, is_error=False)
                        error_summary = {}
                        for error in error_list:
                            line_no, error_message = error  # Assuming error is a tuple (line_no, error_message)
                            if error_message in error_summary:
                                error_summary[error_message].append(line_no)
                            else:
                                error_summary[error_message] = [line_no]
                        for error_message, lines in error_summary.items():
                            lines_str = ', '.join(map(str, lines))
                            _output(f"    - {error_message}: Lines {lines_str}", output_widget, is_error=False)
            else:
                _output(f"- {subfolder}: No validation errors.", output_widget, is_error=False)

    _output("\nValidation complete. Review the errors above and adjust your XML content to meet the length requirements for <name> and <group> tags.", output_widget, is_error=False)
