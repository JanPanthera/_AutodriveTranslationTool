
import configparser
import os
import logging

# Configure logging
log_file = "error.log"
logging.basicConfig(filename=log_file, level=logging.ERROR, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

DEFAULT_CONFIG_FILE_PATH = "config/config-default.ini"
USER_CONFIG_FILE_PATH = "config/config-custom.ini"

def load_setting(section, setting, default_value=None, use_default_config=False):
    """
    Loads a setting from the configuration files. Attempts to load from the user configuration
    unless use_default_config is True. If the setting is not found, falls back to the default
    configuration file. Returns a default value if the setting is not found in either.

    :param section: The section in the configuration file.
    :param setting: The setting to be loaded.
    :param default_value: The default value to return if the setting is not found.
    :param use_default_config: Flag to indicate whether to use the default configuration file.
    :return: The value of the setting if found, otherwise the default value.
    """
    config = configparser.ConfigParser()

    def get_setting_value(file_path):
        if os.path.exists(file_path):
            config.read(file_path)
            if config.has_section(section) and config.has_option(section, setting):
                return config.get(section, setting)
        return None

    if not use_default_config:
        value = get_setting_value(USER_CONFIG_FILE_PATH)
        if value is not None:
            return value

    # Attempt to load from the default configuration file
    value = get_setting_value(DEFAULT_CONFIG_FILE_PATH)
    return value if value is not None else default_value


def save_setting(section, setting, value):
    """
    Saves a single setting to the user configuration file. If the section does not exist,
    it is created. If the setting already exists, its value is updated.

    :param section: The section under which the setting should be saved.
    :param setting: The name of the setting to save.
    :param value: The value to assign to the setting.
    """
    try:
        if isinstance(section, str) and isinstance(setting, str) and section and setting:
            config = configparser.ConfigParser()
            config.read(USER_CONFIG_FILE_PATH)

            if not config.has_section(section):
                config.add_section(section)

            config.set(section, setting, str(value))  # Ensure value is in a proper format

            with open(USER_CONFIG_FILE_PATH, "w") as config_file:
                config.write(config_file)
        else:
            raise ValueError("Invalid section or setting. Both must be non-empty strings.")
    except (IOError, OSError, configparser.Error) as e:
        error_message = f"Configuration error while saving setting: {e}"
        logging.error(error_message)
        print(error_message)
    except Exception as e:
        error_message = f"Unexpected error while saving setting: {e}"
        logging.error(error_message)
        print(error_message)


def save_settings(save_list):
    """
    Saves multiple settings to a configuration file based on a list of section, setting, and value tuples.

    :param save_list: A list of tuples, where each tuple contains (section, setting, value) to be saved.
    """
    if not save_list:
        logging.info("No settings to save.")
        return

    for section, setting, value in save_list:
        try:
            if isinstance(section, str) and isinstance(setting, str) and section and setting:
                save_setting(section, setting, value)
                logging.info(f"Successfully saved {setting} in {section}.")
            else:
                raise ValueError("Invalid section or setting. Both must be non-empty strings.")
        except Exception as e:
            error_message = f"Error while saving {setting} in {section}: {e}"
            logging.error(error_message)
            print(error_message)


def reset_setting(section, setting):
    """
    Resets a specific setting to its default value within a user's configuration file.
    If the section or setting does not exist, logs an error.

    :param section: The section in the configuration file where the setting is located.
    :param setting: The setting within the section to reset to its default value.
    """
    try:
        config_default = configparser.ConfigParser()
        config_default.read(DEFAULT_CONFIG_FILE_PATH)
        
        config_user = configparser.ConfigParser()
        config_user.read(USER_CONFIG_FILE_PATH)

        if config_default.has_section(section) and config_default.has_option(section, setting):
            default_value = config_default.get(section, setting)
            config_user.set(section, setting, default_value)
            with open(USER_CONFIG_FILE_PATH, "w") as config_file:
                config_user.write(config_file)
        else:
            error_message = f"Default setting {setting} not found in section {section} of the default configuration."
            logging.error(error_message)
            print(error_message)

    except configparser.Error as e:
        error_message = f"Configuration parsing error while resetting setting: {e}"
        logging.error(error_message)
        print(error_message)
    except IOError as e:
        error_message = f"I/O error while resetting setting: {e}"
        logging.error(error_message)
        print(error_message)
    except Exception as e:
        error_message = f"Unexpected error while resetting setting: {e}"
        logging.error(error_message)
        print(error_message)


def reset_settings(reset_list):
    """
    Resets multiple settings to their default values based on a list of section and setting tuples.
    
    :param reset_list: A list of tuples, where each tuple contains (section, setting) to be reset.
    """
    if not reset_list:
        logging.info("No settings to reset.")
        return

    for section, setting in reset_list:
        try:
            reset_setting(section, setting)
            logging.info(f"Successfully reset {setting} in {section}.")
        except Exception as e:
            error_message = f"Error while resetting {setting} in {section}: {e}"
            logging.error(error_message)
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
            logging.info(f"Backup of the user configuration created at {backup_path}")

        # Read the default configuration and write it to the user configuration file
        config = configparser.ConfigParser()
        config.read(DEFAULT_CONFIG_FILE_PATH)
        with open(USER_CONFIG_FILE_PATH, "w") as config_file:
            config.write(config_file)
        logging.info("All user settings have been reset to default values.")
    except Exception as e:
        error_message = f"Error while resetting all settings: {e}"
        logging.error(error_message)
        print(error_message)