import os
import re

def _output(message, output_widget=None, logger=None, console=False, is_error=False, is_warning=False):
    if logger:
        if is_error:
            logger.error(message)
        elif is_warning:
            logger.warning(message)
        else:
            logger.info(message)
    message = message + "\n"
    if is_error:
        message = f"ERROR: {message}"
    if is_warning:
        message = f"WARNING: {message}"
    if output_widget:
        output_widget.write_console(message)
    if console:
        print(message, end='')

def _process_file(input_file_path, output_dir_path, patterns, translation_counts, output_widget=None, logger=None):
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
            _output(f"File processed: {input_file_path}", output_widget, logger)
            return True

    except Exception as e:
        _output(f"An error occurred while processing file '{input_file_path}': {e}", output_widget, logger, is_error=True)

    return False

def _perform_translation(input_path, output_path, patterns, language, output_widget=None, logger=None):
    translation_counts = {}
    files_processed = 0
    files_skipped = 0

    _output(f"--- {language} Translation ---", output_widget, logger)
    _output(f"Input: {input_path}\nOutput: {output_path}\n", output_widget, logger)

    for root, _, files in os.walk(input_path):
        for file in files:
            input_file_path = os.path.join(root, file)
            output_dir_path = os.path.join(output_path, os.path.relpath(root, input_path))

            if _process_file(input_file_path, output_dir_path, patterns, translation_counts, output_widget, logger):
                files_processed += 1
            else:
                files_skipped += 1
                
    _output("", output_widget, logger)

    if files_processed > 0:
        file_word = "file" if files_processed == 1 else "files"
        _output(f"Processed {files_processed} {file_word}. Skipped {files_skipped} files.\n", output_widget, logger)
        _output("Translation Counts:", output_widget, logger)
        for source_text, (count, target_text) in translation_counts.items():
            clean_source_text = source_text.replace(r'\b', '')
            _output(f'   {clean_source_text} --> {target_text}: {count} replacements', output_widget, logger)
    else:
        _output(f"No input files found in directory: {input_path}. Skipping.", output_widget, logger, is_warning=True)

    _output("", output_widget, logger)

def translate_files(input_path="TranslationTool/_input", output_path="TranslationTool/_output",
                    dictionaries_path="TranslationTool/_dictionaries", languages="",
                    output_widget=None, logger=None):
    _output(f"Starting translation process for {len(languages)} languages: {', '.join(languages)}.\n", output_widget, logger)

    for language in languages:
        dictionary_file_name = os.path.join(dictionaries_path, f"Dictionary_{language}.dic")
        language_output_path = os.path.join(output_path, language)

        if not os.path.isfile(dictionary_file_name):
            _output(f"Dictionary file '{dictionary_file_name}' not found. Skipping translation for {language}.\n", output_widget, logger, is_warning=True)
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

        _perform_translation(input_path, language_output_path, patterns, language, output_widget, logger)

    _output("Translation process completed.\n\n", output_widget, logger)
