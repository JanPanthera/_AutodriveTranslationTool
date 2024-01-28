import os
import argparse
from TranslationTool import SUPPORTED_LANGUAGES

def perform_translation(input_path, output_path, translation_list_file_name):
    translation_counts = {}

    for (root, dirs, files) in os.walk(input_path):
        # Check if there are any files in the current directory
        if not files:
            print(f"Error ~ No input files found in directory: {root}\n")
            continue  # Skip this directory and move on to the next one
        
        for file in files:
            input_file_path = os.path.join(root, file)
            output_dir_path = root.replace("input", output_path, 1)
            os.makedirs(output_dir_path, exist_ok=True)
            output_file_path = os.path.join(output_dir_path, file)

            with open(input_file_path) as auto_config_read:
                with open(output_file_path, "w") as auto_config_write:
                    with open(translation_list_file_name) as f:
                        file_text = auto_config_read.read()
                        for line in f:
                            if line.isspace():
                                continue
                            source_text, target_text = line.strip().split(",")[:2]
                            count = file_text.count(source_text)
                            if count > 0:
                                file_text = file_text.replace(source_text, target_text)
                                translation_counts[source_text] = (count, target_text)
                        auto_config_write.write(file_text)

    print("Translation Counts:")
    for source_text, (count, target_text) in translation_counts.items():
        print(f'"{source_text}" was replaced {count} times with "{target_text}".')

    print("\nTranslation complete!\n\n")

def main():
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument('selected_language', metavar='Selected_Language', type=str, help='The selected language')
    args = parser.parse_args()

    translation_list_file_names = {lang: f"TranslationList_{lang}.txt" for lang in SUPPORTED_LANGUAGES}
    translation_list_file_name = os.path.join("translationLists", translation_list_file_names.get(args.selected_language, "DefaultTranslationList.txt"))
    output_path = os.path.join("output", args.selected_language)

    print(f"Translating to {args.selected_language} \nUsing translation list: {translation_list_file_name}\nOutput path: {output_path}\n")

    # Check if the translation list file exists before performing translation
    if os.path.exists(translation_list_file_name):
        perform_translation("input", output_path, translation_list_file_name)
    else:
        print(f"Error ~ Translation list file '{translation_list_file_name}' does not exist. Translation aborted.")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main entry point

if __name__ == "__main__":
    main()
