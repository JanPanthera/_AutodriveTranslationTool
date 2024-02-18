# pre_translate_dictionary.py

import logging


def _output(message, output_widget=None):
    """Outputs messages either to a widget or to console."""
    if output_widget:
        output_widget.write_console(message + "\n")
    else:
        print(message)


def update_local_dictionary(global_dict_path, local_dict_path, output_path, logger=None, output_widget=None):
    """Updates the local dictionary based on the global dictionary."""
    # Read global dictionary
    global_dict = {}
    with open(global_dict_path, 'r', encoding='utf-8') as f:
        for line in f:
            if ',' in line:
                word, translation = line.strip().split(',')
            else:
                logging.warning(f"Skipping line {line} as it does not contain a comma.")
        global_dict[word] = translation

    # Update local dictionary
    updated_local_dict = []
    with open(local_dict_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',')
            word = parts[0]
            if word in global_dict:
                # Word found in global dictionary
                translation = global_dict[word]
                updated_local_dict.append(f"{word},{translation}")
                if logger:
                    logger.info(f"Updated: {word} -> {translation}")
                _output(f"Updated: {word} -> {translation}", output_widget)
            else:
                # Word not found in global dictionary, keep original line
                updated_local_dict.append(line.strip())
                if logger:
                    logger.info(f"Unchanged: {line.strip()}")
                _output(f"Unchanged: {line.strip()}", output_widget)

    # Write updated local dictionary to file
    with open(output_path, 'w', encoding='utf-8') as f:
        for entry in updated_local_dict:
            f.write(f"{entry}\n")
    _output("Local dictionary updated successfully.", output_widget)
