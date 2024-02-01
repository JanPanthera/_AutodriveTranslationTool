
import os
import logging

# Configure logging
log_file = "error.log"
logging.basicConfig(filename=log_file, level=logging.ERROR, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

def load_file(file_path):
    try:
        if not os.path.exists(file_path):
            error_message = f"File not found: {file_path}"
            logging.error(error_message)
            return ""
        with open(file_path, "r") as file:
            return file.read()
    except Exception as e:
        error_message = f"Error while loading file {file_path}: {e}"
        logging.error(error_message)
        print(error_message)
        return ""

def save_file(file_path, file_contents):
    try:
        with open(file_path, "w") as file:
            file.write(file_contents)
    except Exception as e:
        error_message = f"Error while saving file {file_path}: {e}"
        logging.error(error_message)
        print(error_message)

def load_file_to_textbox(textbox, file_path):
    try:
        textbox.delete("1.0", "end")
        if not os.path.exists(file_path):
            error_message = f"File not found: {file_path}"
            logging.error(error_message)
            textbox.insert("1.0", error_message)
            return
        with open(file_path, "r") as file:
            textbox.insert("1.0", file.read())
    except Exception as e:
        error_message = f"Error while loading file {file_path}: {e}"
        logging.error(error_message)
        print(error_message)

def save_file_from_textbox(textbox, file_path):
    try:
        with open(file_path, "w") as file:
            file.write(textbox.get("1.0", "end-1c"))
    except Exception as e:
        error_message = f"Error while saving file {file_path}: {e}"
        logging.error(error_message)
        print(error_message)

def create_file(file_path):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            file.write("")
    except Exception as e:
        error_message = f"Failed to create file {file_path}: {e}"
        logging.error(error_message)
        print(error_message)

def delete_file(file_path):
    try:
        os.remove(file_path)
    except Exception as e:
        error_message = f"Failed to delete file {file_path}: {e}"
        logging.error(error_message)
        print(error_message)

def get_all_file_names_in_directory(directory):
    try:
        return os.listdir(directory)
    except Exception as e:
        error_message = f"Error while listing files in directory {directory}: {e}"
        logging.error(error_message)
        print(error_message)
        return []
