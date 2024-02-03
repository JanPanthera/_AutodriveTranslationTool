import subprocess
import os

def generate_pot_file(source_dir, output_file, config_file='babel.cfg'):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    command = ['pybabel', 'extract', '-F', config_file, '-o', output_file, source_dir]
    subprocess.run(command, check=True)

def init_or_update_po_files(languages, pot_file, locale_dir):
    for lang in languages:
        po_file_path = os.path.join(locale_dir, lang, 'LC_MESSAGES', 'messages.po')
        if os.path.exists(po_file_path):
            # Update the existing .po file with new messages from the .pot file
            command = ['pybabel', 'update', '-i', pot_file, '-d', locale_dir, '-l', lang]
            print(f"Updating .po file for language: {lang}")
        else:
            # Initialize a new .po file for the language from the .pot file
            os.makedirs(os.path.dirname(po_file_path), exist_ok=True)
            command = ['pybabel', 'init', '-i', pot_file, '-d', locale_dir, '-l', lang]
            print(f"Initializing .po file for language: {lang}")
        subprocess.run(command, check=True)

def compile_po_files(languages, locale_dir):
    for lang in languages:
        command = ['pybabel', 'compile', '-d', locale_dir, '-l', lang]
        print(f"Compiling .mo file for language: {lang}")
        subprocess.run(command, check=True)

if __name__ == '__main__':
    source_dir = 'src'
    locale_dir = 'locales'
    pot_file = os.path.join(locale_dir, 'messages.pot')
    languages = ['de']  # List of language codes

    # Generate the .pot file
    generate_pot_file(source_dir, pot_file)

    # Initialize or update .po files for each language
    init_or_update_po_files(languages, pot_file, locale_dir)

    # Compile .po files into .mo files
    input("Press Enter to continue...")
    compile_po_files(languages, locale_dir)

    input("Press Enter to continue...")