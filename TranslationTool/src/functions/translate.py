import os
import re

def _output(message, output_widget=None):
    """
    Display the given message.

    Args:
        message (str): The message to be displayed.
        output_widget (object, optional): The output widget for displaying the message. Defaults to None.

    Returns:
        None
    """
    if output_widget:
        output_widget.write_console(message + "\n")
    else:
        print(message)

def _process_file(input_file_path, output_dir_path, patterns, translation_counts, output_widget=None):
    """
    Process a file by applying the specified patterns for translation.

    Args:
        input_file_path (str): The path to the input file.
        output_dir_path (str): The path to the output directory.
        patterns (dict): A dictionary containing the patterns to search for and their corresponding target texts.
        translation_counts (dict): A dictionary to keep track of the translation counts for each pattern.
        output_widget (object, optional): The output widget for displaying translation progress.

    Returns:
        bool: True if replacements were made in the file, False otherwise.
    """
    replacements_in_file = False

    try:
        os.makedirs(output_dir_path, exist_ok=True)
        output_file_path = os.path.join(output_dir_path, os.path.basename(input_file_path))

        with open(input_file_path, 'r', encoding='utf-8') as file:
            file_text = file.read().strip()
        if not file_text:
            return False

        for pattern, target_text in patterns.items():
            new_text, count = pattern.subn(target_text, file_text)
            if count > 0:
                file_text = new_text
                translation_counts[pattern.pattern] = translation_counts.get(pattern.pattern, (0, target_text))[0] + count, target_text
                replacements_in_file = True

        if replacements_in_file:
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(file_text)
            return True

    except Exception as e:
        _output(f"An error occurred while processing file '{input_file_path}': {e}", output_widget)

    return False

def _perform_translation(input_path, output_path, patterns, language, output_widget=None):
    """
    Performs translation on the files in the input directory based on the provided patterns for a specific language.

    Args:
        input_path (str): The path to the input directory.
        output_path (str): The path to the output directory.
        patterns (dict): A dictionary containing the patterns to search for and their corresponding target texts.
        language (str): The language for which the translation is being performed.
        output_widget (object, optional): The output widget for displaying translation progress.

    Returns:
        None
    """
    translation_counts = {}
    files_processed = 0
    files_skipped = 0

    _output(f"--- {language} Translation ---", output_widget)
    _output(f"Input: {input_path}\nOutput: {output_path}\n", output_widget)

    for root, dirs, files in os.walk(input_path):
        for file in files:
            input_file_path = os.path.join(root, file)
            output_dir_path = os.path.join(output_path, os.path.relpath(root, input_path))

            if _process_file(input_file_path, output_dir_path, patterns, translation_counts, output_widget):
                files_processed += 1
            else:
                files_skipped += 1

    # Check if any files were processed
    if files_processed > 0:
        file_word = "file" if files_processed == 1 else "files"
        _output(f"Processed {files_processed} {file_word}. Skipped {files_skipped} files.", output_widget)
        _output("Translation Counts:", output_widget)
        for source_text, (count, target_text) in translation_counts.items():
            clean_source_text = source_text.replace(r'\b', '')
            _output(f'   {clean_source_text} --> {target_text}: {count} replacements', output_widget)
    else:
        _output(f"No input files found in directory: {input_path}. Skipping.", output_widget)

    _output("\n", output_widget)

def translate_files(input_path="TranslationTool/_input", output_path="TranslationTool/_output",
                    dictionaries_path="TranslationTool/_dictionaries", languages="", output_widget=None):
    """
    Translates files based on the provided dictionaries for multiple languages.

    Args:
        input_path (str, optional): The path to the input directory. Defaults to "TranslationTool/_input".
        output_path (str, optional): The path to the output directory. Defaults to "TranslationTool/_output".
        dictionaries_path (str, optional): The path to the dictionaries directory. Defaults to "TranslationTool/_dictionaries".
        languages (str, optional): The languages to translate. Defaults to "".
        output_widget (object, optional): The output widget for displaying translation progress. Defaults to None.
    """
    _output(f"Starting translation process for {len(languages)} languages: {', '.join(languages)}.\n", output_widget)

    for language in languages:
        dictionary_file_name = os.path.join(dictionaries_path, f"Dictionary_{language}.dic")
        language_output_path = os.path.join(output_path, language)

        if not os.path.isfile(dictionary_file_name):
            _output(f"Dictionary file '{dictionary_file_name}' not found. Skipping translation for {language}.\n", output_widget)
            continue

        with open(dictionary_file_name, 'r', encoding='utf-8') as file:
            dictionary_text = file.read()
        patterns = {}
        for line in dictionary_text.splitlines():
            line = line.strip()
            if line.startswith('###*') or line.endswith('*###') or not line:
                continue

            parts = line.split(",", maxsplit=1)
            if len(parts) == 2:
                source_text, target_text = parts
                patterns[re.compile(r'\b' + re.escape(source_text) + r'\b')] = target_text

        _perform_translation(input_path, language_output_path, patterns, language, output_widget)

    _output("Translation process completed.\n\n", output_widget)
