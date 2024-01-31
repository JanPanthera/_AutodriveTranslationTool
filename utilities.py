import configparser
import subprocess
import sys
import os

DEFAULT_CONFIG_FILE_PATH = "config/config-default.ini"
USER_CONFIG_FILE_PATH = "config/config-custom.ini"

def load_setting(section, setting, default_value=None, use_default_config=False):
    config = configparser.ConfigParser()
    if not use_default_config and os.path.exists(USER_CONFIG_FILE_PATH):
        config.read(USER_CONFIG_FILE_PATH)
        if config.has_section(section) and config.has_option(section, setting):
            return config.get(section, setting)
    config.read(DEFAULT_CONFIG_FILE_PATH)
    if config.has_section(section) and config.has_option(section, setting):
        return config.get(section, setting)
    return default_value

def save_setting(section, setting, value):
    config = configparser.ConfigParser()
    config.read(USER_CONFIG_FILE_PATH)
    if not config.has_section(section):
        config.add_section(section)
    config.set(section, setting, value)
    with open(USER_CONFIG_FILE_PATH, "w") as config_file:
        config.write(config_file)

def reset_settings():
    config = configparser.ConfigParser()
    config.read(DEFAULT_CONFIG_FILE_PATH)
    with open(USER_CONFIG_FILE_PATH, "w") as user_config_file:
        config.write(user_config_file)

def reset_setting(section, setting):
    save_setting(section, setting, load_setting(section, setting, use_default_config=True))

def save_window_geometry(window_geometry):
    size_part, pos_x, pos_y = window_geometry.split('+')
    width, height = size_part.split('x')
    save_setting("WindowGeometry", "width", width)
    save_setting("WindowGeometry", "height", height)
    save_setting("WindowGeometry", "pos_x", pos_x)
    save_setting("WindowGeometry", "pos_y", pos_y)

def load_window_geometry():
    width = load_setting("WindowGeometry", "width", default_value="1366")
    height = load_setting("WindowGeometry", "height", default_value="768")
    pos_x = load_setting("WindowGeometry", "pos_x", default_value="100")
    pos_y = load_setting("WindowGeometry", "pos_y", default_value="100")
    return f"{width}x{height}+{pos_x}+{pos_y}"

import ctypes

def get_dpi_scaling_factor():
    """
    Queries the system's DPI settings to calculate the DPI scaling factor.

    Returns:
        scaling_factor (float): The system's DPI scaling factor, with 1.0 indicating no scaling.
    """
    # Default scaling factor
    scaling_factor = 1.0

    try:
        # Query the DPI Awareness (Windows 10 and above)
        awareness = ctypes.c_int()
        errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))

        if errorCode == 0:  # S_OK
            # Get the system DPI
            dpi = ctypes.windll.user32.GetDpiForSystem()
            # Calculate the scaling factor (96 DPI is the default)
            scaling_factor = dpi / 96.0
    except (AttributeError, OSError):
        # AttributeError if the functions aren't available (non-Windows or older Windows),
        # OSError if there's a problem calling the Windows API
        pass  # Maintain the default scaling factor of 1.0

    return scaling_factor

def run_script(console_output, window, script, args, after_callback):
    console_output.configure(state='normal')
    console_output.delete("1.0", 'end')

    def read_output(process, is_stderr=False):
        next_line = process.stderr.readline() if is_stderr else process.stdout.readline()

        if next_line:
            console_output.insert('end', next_line)
            console_output.see('end')  # Auto-scroll to the bottom
            after_callback(1, lambda: read_output(process, is_stderr))
        elif process.poll() is None:
            after_callback(1, lambda: read_output(process, is_stderr))
        else:
            if not is_stderr:  # Start reading stderr
                after_callback(1, lambda: read_output(process, True))
            else:
                console_output.configure(state='disabled')  # Disable edits once process is complete

    try:
        # Create the command to run the script with its arguments
        command = [sys.executable, script] + args
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        after_callback(1, lambda: read_output(process))
    except Exception as e:
        console_output.insert('end', f"Failed to run the script: {e}\n")
        console_output.configure(state='disabled')

def load_file(textbox, file_path):
    textbox.delete("1.0", "end")
    if not os.path.exists(file_path):
        textbox.insert("1.0", f"File not found: {file_path}")
        return
    with open(file_path, "r") as file:
        textbox.insert("1.0", file.read())

def save_file(textbox, file_path):
    with open(file_path, "w") as file:
        file.write(textbox.get("1.0", "end-1c"))

def create_file(file_path):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure the directory exists
        with open(file_path, "w") as file:
            file.write("")
    except Exception as e:
        print(f"Failed to create file {file_path}: {e}")

def delete_file(file_path):
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"Failed to delete file {file_path}: {e}")

def get_all_file_names_in_directory(directory):
    files = os.listdir(directory)
    return files