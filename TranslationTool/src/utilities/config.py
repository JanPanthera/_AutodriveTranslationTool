#TODO: Switch to ConfigManager class
import configparser
import os

DEFAULT_CONFIG_FILE_PATH = "config/config-default.ini"
USER_CONFIG_FILE_PATH = "config/config-custom.ini"

if 'VSAPPIDDIR' in os.environ:
    DEFAULT_CONFIG_FILE_PATH = os.path.join("TranslationTool/", DEFAULT_CONFIG_FILE_PATH)
    USER_CONFIG_FILE_PATH = os.path.join("TranslationTool/", USER_CONFIG_FILE_PATH)

def load_setting(section, setting, default_value=None, use_default_config=False):
    config = configparser.ConfigParser()

    if not isinstance(section, str) or not isinstance(setting, str) or not section or not setting:
        print("Invalid section or setting name. Both must be non-empty strings.")
        return default_value

    def get_setting_value(file_path):
        try:
            if not os.path.exists(file_path):
                print(f"Configuration file {file_path} not found.")
                return None
            config.read(file_path)
            return config.get(section, setting) if config.has_section(section) and config.has_option(section, setting) else None
        except configparser.Error as e:
            print(f"Error parsing the configuration file {file_path}: {e}")
            return None

    value = get_setting_value(USER_CONFIG_FILE_PATH if not use_default_config else DEFAULT_CONFIG_FILE_PATH)
    if value is not None:
        return value

    if not use_default_config:
        # If not found in user config, try default config
        value = get_setting_value(DEFAULT_CONFIG_FILE_PATH)

    return value if value is not None else default_value

def save_setting(section, setting, value):
    if not isinstance(section, str) or not isinstance(setting, str) or not section or not setting:
        print("Invalid section or setting name. Both must be non-empty strings.")
        return

    config = configparser.ConfigParser()
    try:
        config.read(USER_CONFIG_FILE_PATH)
    except configparser.Error as e:
        print(f"Error parsing the user configuration file: {e}")
        return

    if not config.has_section(section):
        config.add_section(section)

    config.set(section, setting, str(value))

    try:
        with open(USER_CONFIG_FILE_PATH, "w") as config_file:
            config.write(config_file)
    except (IOError, OSError) as e:
        print(f"Error writing to the user configuration file: {e}")

def reset_setting(section, setting):

    config_default = configparser.ConfigParser()
    config_user = configparser.ConfigParser()

    try:
        config_default.read(DEFAULT_CONFIG_FILE_PATH)
        config_user.read(USER_CONFIG_FILE_PATH)
    except configparser.Error as e:
        print(f"Error parsing configuration files: {e}")
        return

    if config_default.has_section(section) and config_default.has_option(section, setting):
        default_value = config_default.get(section, setting)
        if not config_user.has_section(section):
            config_user.add_section(section)
        config_user.set(section, setting, default_value)
        try:
            with open(USER_CONFIG_FILE_PATH, "w") as config_file:
                config_user.write(config_file)
        except (IOError, OSError) as e:
            print(f"Error writing to the user configuration file: {e}")
    else:
        print(f"Default setting '{setting}' not found in section '{section}'.")





def save_settings(save_list):
    """
    Saves multiple settings to a configuration file based on a list of section, setting, and value tuples.

    :param save_list: A list of tuples, where each tuple contains (section, setting, value) to be saved.
    """
    if not save_list:
        return

    for section, setting, value in save_list:
        try:
            if isinstance(section, str) and isinstance(setting, str) and section and setting:
                save_setting(section, setting, value)
            else:
                raise ValueError("Invalid section or setting. Both must be non-empty strings.")
        except Exception as e:
            error_message = f"Error while saving {setting} in {section}: {e}"
            print(error_message)


def reset_settings(reset_list):
    """
    Resets multiple settings to their default values based on a list of section and setting tuples.
    
    :param reset_list: A list of tuples, where each tuple contains (section, setting) to be reset.
    """
    if not reset_list:
        return

    for section, setting in reset_list:
        try:
            reset_setting(section, setting)
        except Exception as e:
            error_message = f"Error while resetting {setting} in {section}: {e}"
            print(error_message)


def reset_all_settings(backup=False):
    """
    Resets all user settings to default values by overwriting the user configuration
    with the default configuration. Optionally creates a backup of the current user configuration.

    :param backup: If True, creates a backup of the user configuration before resetting.
    """
    try:
        # Check if the default configuration file exists
        if not os.path.exists(DEFAULT_CONFIG_FILE_PATH):
            raise FileNotFoundError(f"Default configuration file not found at {DEFAULT_CONFIG_FILE_PATH}")

        # Optionally backup the current user configuration
        if backup and os.path.exists(USER_CONFIG_FILE_PATH):
            backup_path = USER_CONFIG_FILE_PATH + '.bak'
            with open(USER_CONFIG_FILE_PATH, 'r') as original, open(backup_path, 'w') as backup_file:
                backup_file.write(original.read())

        # Read the default configuration and write it to the user configuration file
        config = configparser.ConfigParser()
        config.read(DEFAULT_CONFIG_FILE_PATH)
        with open(USER_CONFIG_FILE_PATH, "w") as config_file:
            config.write(config_file)
    except Exception as e:
        error_message = f"Error while resetting all settings: {e}"
        print(error_message)