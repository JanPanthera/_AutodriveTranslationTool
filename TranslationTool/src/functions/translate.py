import os
import re
import src.utilities.file_ops as file_ops

def output(message, output_widget=None):
    if output_widget:
        output_widget.configure(state='normal')
        output_widget.insert('end', message + "\n")
        output_widget.configure(state='disable')
        output_widget.see('end')
    else:
        print(message)

def process_file(input_file_path, output_dir_path, dictionary_text, translation_counts, output_widget=None):
    replacements_in_file = False

    try:
        os.makedirs(output_dir_path, exist_ok=True)
        output_file_path = os.path.join(output_dir_path, os.path.basename(input_file_path))

        file_text = file_ops.load_file(input_file_path)
        if not file_text.strip():
            return False

        skipping = False
        for line in dictionary_text.splitlines():
            line = line.strip()
            if line.startswith('###*'):
                skipping = True
                continue
            if line.endswith('*###'):
                skipping = False
                continue
            if skipping or not line:
                continue

            parts = line.split(",", maxsplit=1)
            if len(parts) == 2:
                source_text, target_text = parts
                pattern = r'\b' + re.escape(source_text) + r'\b'
                new_text, count = re.subn(pattern, target_text, file_text)
                if count > 0:
                    file_text = new_text
                    translation_counts[source_text] = translation_counts.get(source_text, (0, target_text))[0] + count, target_text
                    replacements_in_file = True
            else:
                output(f"Skipping line due to incorrect format: {line}", output_widget)

        if replacements_in_file:
            file_ops.save_file(output_file_path, file_text)
            return True

    except Exception as e:
        output(f"An error occurred while processing file '{input_file_path}': {e}", output_widget)

    return False

def perform_translation(input_path, output_path, dictionary_file_name, language, output_widget=None):
    translation_counts = {}
    files_processed = 0
    files_skipped = 0
    files_with_no_replacements = 0

    output(f"--- {language} Translation ---", output_widget)
    output(f"Input: {input_path}\nOutput: {output_path}\nDictionary: {dictionary_file_name}\n", output_widget)

    if not os.path.isfile(dictionary_file_name):
        output(f"Dictionary file '{dictionary_file_name}' not found. Skipping translation for {language}.\n", output_widget)
        return

    dictionary_text = file_ops.load_file(dictionary_file_name)

    for root, dirs, files in os.walk(input_path):
        if not files:
            output(f"No input files found in directory: {root}. Skipping.", output_widget)
            continue

        for file in files:
            input_file_path = os.path.join(root, file)
            output_dir_path = os.path.join(output_path, os.path.relpath(root, input_path))

            if process_file(input_file_path, output_dir_path, dictionary_text, translation_counts, output_widget):
                files_processed += 1
            else:
                files_skipped += 1

    if files_processed > 0:
        file_word = "file" if files_processed == 1 else "files"
        output(f"Processed {files_processed} {file_word}. Skipped {files_skipped} files.", output_widget)
        output("Translation Counts:", output_widget)
        for source_text, (count, target_text) in translation_counts.items():
            output(f'   {source_text} --> {target_text}: {count} replacements', output_widget)
    elif files_with_no_replacements > 0:
        output(f"No replacements needed in {files_with_no_replacements} files. Skipped {files_skipped} files.", output_widget)
    else:
        output("No translations were performed. All files were skipped.", output_widget)

    output("\n", output_widget)

def translate_files(input_path="TranslationTool/_input", output_path="TranslationTool/_output",
                    dictionaries_path="TranslationTool/_dictionaries", languages="", output_widget=None):
    output(f"Starting translation process for {len(languages)} languages: {', '.join(languages)}.\n", output_widget)

    for language in languages:
        dictionary_file_name = os.path.join(dictionaries_path, f"Dictionary_{language}.dic")
        language_output_path = os.path.join(output_path, language)

        perform_translation(input_path, language_output_path, dictionary_file_name, language, output_widget)

    output("Translation process completed.\n\n", output_widget)
