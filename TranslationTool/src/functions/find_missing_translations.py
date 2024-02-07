import re
import os

def _output(message, output_widget=None, output_file=None):
    """Outputs messages to console, widget, and optionally to a file."""
    if output_widget:
        output_widget.write_console(message + "\n")
    else:
        print(message)
    
    if output_file:
        try:
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(message + "\n")
        except PermissionError:
            print(f"Error: Permission denied. Unable to write to file {output_file}.")

def _load_translations(dictionary_path, languages):
    """Loads translations from dictionary files for specified languages into a dictionary."""
    translations = {}
    for root, dirs, files in os.walk(dictionary_path):
        for file in files:
            if file.endswith(".dic"):
                for language in languages:
                    if language.lower() in file.lower():
                        with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                            translations[language] = set()
                            for line in f:
                                if ',' in line:
                                    word, _ = line.strip().split(',')
                                    translations[language].add(word)
                                else:
                                    print(f"Skipping line {line.strip()} as it does not contain a comma.")
    return translations

def _find_missing_translations_in_file(input_file, translations):
    """Finds missing translations in a single input file."""
    word_pattern = re.compile(r'<(?:name|group)>(.*?)</(?:name|group)>')
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    words = word_pattern.findall(content)
    unique_words = set([word for phrase in words for word in phrase.split()])

    missing_translations = {lang: unique_words - trans for lang, trans in translations.items()}
    return missing_translations

def find_missing_translations(input_path, output_path, dictionary_path, languages, output_widget=None):
    """Finds and outputs words without translations for all input files."""
    
    _output(f"Starting search for missing translations in {input_path} for {len(languages)} languages: {', '.join(languages)}.\n", output_widget, output_path)

    # Convert languages to a list if it's a string
    if isinstance(languages, str):
        languages = [lang.strip() for lang in languages.split(',')]

    # Load translations for the specified languages
    translations = _load_translations(dictionary_path, languages)

    # Prepare the output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("")

    # Search for XML files and process each
    for root, dirs, files in os.walk(input_path):
        for file in files:
            if file.endswith(".xml"):
                input_file = os.path.join(root, file)
                _output(f"\n{input_file}", output_widget, output_path)
                missing_translations = _find_missing_translations_in_file(input_file, translations)

                for language, missing in missing_translations.items():
                    if missing:
                        _output(f"\n{language} is missing ({len(missing)}) translations", output_widget, output_path)
                        for word in sorted(missing):
                            _output(f"{word}", output_widget, output_path)
                    else:
                        _output(f"{language}\n    All words have translations.", output_widget, output_path)

    _output("\nFinished search for missing translations.", output_widget, output_path)

# Example usage
# if __name__ == "__main__":
#     input_path = 'path_to_input_folder'  # Replace with the actual path to your input folder
#     output_path = 'path_to_output_file.txt'  # Replace with the actual path to your output file
#     dictionary_path = 'path_to_dictionary_folder'  # Replace with the actual path to your dictionary folder
#     languages = ["English", "German"]  # Specify the languages
# 
#     find_missing_translations(input_path, output_path, dictionary_path, languages)
