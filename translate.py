import os
import argparse
import utilities.file_ops as file_ops  # Ensure this import path is correct for your project structure

def perform_translation(input_path, output_path, dictionary_file_name, language):
    translation_counts = {}
    files_processed = 0
    files_skipped = 0
    files_with_no_replacements = 0

    print(f"--- {language} Translation ---")
    print(f"Dictionary: {dictionary_file_name}\nOutput: {output_path}")

    for root, dirs, files in os.walk(input_path):
        if not files:
            print(f"No input files found in directory: {root}. Skipping.")
            continue

        for file in files:
            input_file_path = os.path.join(root, file)
            output_dir_path = root.replace("_input", output_path, 1)
            replacements_in_file = False

            try:
                os.makedirs(output_dir_path, exist_ok=True)
                output_file_path = os.path.join(output_dir_path, file)

                file_text = file_ops.load_file(input_file_path)
                if file_text == "":  # If file couldn't be loaded, skip to the next file
                    files_skipped += 1
                    continue

                dictionary_text = file_ops.load_file(dictionary_file_name)
                dictionary_list = [line.strip().split(",")[:2] for line in dictionary_text.splitlines() if not line.isspace()]

                for source_text, target_text in dictionary_list:
                    count = file_text.count(source_text)
                    if count > 0:
                        file_text = file_text.replace(source_text, target_text)
                        translation_counts[source_text] = translation_counts.get(source_text, (0, target_text))[0] + count, target_text
                        replacements_in_file = True

                if replacements_in_file:
                    file_ops.save_file(output_file_path, file_text)
                    files_processed += 1
                else:
                    files_with_no_replacements += 1

            except Exception as e:
                print(f"An error occurred while processing file '{input_file_path}': {e}")
                files_skipped += 1

    if files_processed > 0:
        file_word = "file" if files_processed == 1 else "files"
        print(f"Processed {files_processed} {file_word}. Skipped {files_skipped} files.")
        print("Translation Counts:")
        for source_text, (count, target_text) in translation_counts.items():
            print(f'   {source_text} --> {target_text}: {count} replacements')
    elif files_with_no_replacements > 0:
        print(f"No replacements needed in {files_with_no_replacements} files. Skipped {files_skipped} files.")
    else:
        print("No translations were performed. All files were skipped.")

    print("\n")  # Add a footer for clarity

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("selected_languages", nargs="+", help="The list of languages to translate to.")
    args = parser.parse_args()

    print(f"Starting translation process for {len(args.selected_languages)} languages: {', '.join(args.selected_languages)}.\n")

    for selected_language in args.selected_languages:
        dictionary_file_name = os.path.join("dictionaries", f"Dictionary_{selected_language}.dic")
        output_path = os.path.join("_output", selected_language)

        if not os.path.isfile(dictionary_file_name):
            print(f"--- {selected_language} Translation ---")
            print(f"Dictionary file '{dictionary_file_name}' not found. Skipping translation for {selected_language}.\n")
            continue

        perform_translation("_input", output_path, dictionary_file_name, selected_language)

    print("Translation process completed.")

if __name__ == "__main__":
    main()
