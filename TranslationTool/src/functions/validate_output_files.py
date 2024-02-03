import os
import re
import src.utilities.file_ops as file_ops

def output(message, output_widget=None, is_error=False):
    # Modify this function to handle error messages differently if needed
    prefix = "[ERROR] " if is_error else ""
    final_message = f"{prefix}{message}\n"
    if output_widget:
        output_widget.configure(state='normal')
        output_widget.insert('end', final_message)
        output_widget.configure(state='disable')  # Could also be 'readonly'
        output_widget.see('end')
    else:
        print(final_message)

def validate_output_file(file_path, errors):
    # Assume file_ops.load_file and other necessary imports and functions are defined elsewhere
    file_text = file_ops.load_file(file_path)
    if not file_text.strip():
        errors.append((file_path, "File is empty or only contains whitespace."))
        return False

    name_tag_pattern = r'<name>(.*?)<\/name>'
    group_tag_pattern = r'<group>(.*?)<\/group>'

    for line_no, line in enumerate(file_text.splitlines(), start=1):
        for pattern, max_length, tag_name in [(name_tag_pattern, 30, 'name'), (group_tag_pattern, 20, 'group')]:
            for match in re.finditer(pattern, line):
                text_inside_tag = match.group(1)
                if len(text_inside_tag) > max_length:
                    errors.append((file_path, f"Line {line_no}: <{tag_name}> tag content exceeds max length ({len(text_inside_tag)}/{max_length} characters)."))

def validate_output_files(input_path="_output", languages=None, output_widget=None):
    if isinstance(languages, (str, list)):
        languages_list = [lang.strip() for lang in languages.split(',')] if isinstance(languages, str) else languages
    else:
        output("Invalid 'languages' parameter. It must be a comma-separated string or a list of strings.", output_widget, is_error=True)
        return

    output(f"Validating output files for the following languages: {', '.join(languages_list)}\n", output_widget)

    errors = []  # Collect all errors in a list

    for language in languages_list:
        language_path = os.path.join(input_path, language)
        if not os.path.exists(language_path):
            output("", output_widget)  # Add a newline before the error message for better readability
            output(f"Language output path {language_path} does not exist. No Files? Skipping.", output_widget, is_error=True)
            continue

        for root, dirs, files in os.walk(language_path):
            if not files:
                continue  # Skip directories without files silently

            for file in files:
                file_path = os.path.join(root, file)
                validate_output_file(file_path, errors)
                
            if errors:
                output(f"Validation Errors Found for {language}:", output_widget, is_error=False)
                for file_path, error_message in errors:
                    output(f"{error_message}", output_widget, is_error=True)
                errors = []
            else:
                output(f"No validation errors found for {language}.", output_widget)

    output("\nValidation complete.", output_widget)