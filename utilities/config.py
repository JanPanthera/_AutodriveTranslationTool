
import configparser
import os
import logging

# Configure logging
log_file = "error.log"
logging.basicConfig(filename=log_file, level=logging.ERROR, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

DEFAULT_CONFIG_FILE_PATH = "config/config-default.ini"
USER_CONFIG_FILE_PATH = "config/config-custom.ini"

def load_setting(section, setting, default_value=None, use_default_config=False):
    try:
        config = configparser.ConfigParser()

        if not use_default_config and os.path.exists(USER_CONFIG_FILE_PATH):
            config.read(USER_CONFIG_FILE_PATH)
            if config.has_section(section) and config.has_option(section, setting):
                return config.get(section, setting)

        config.read(DEFAULT_CONFIG_FILE_PATH)
        if config.has_section(section) and config.has_option(section, setting):
            return config.get(section, setting)

        return default_value

    except Exception as e:
        error_message = f"Error while loading setting: {e}"
        logging.error(error_message)
        print(error_message)
        return default_value

def save_setting(section, setting, value):
    try:
        # Check if section and setting are valid strings
        if isinstance(section, str) and isinstance(setting, str):
            config = configparser.ConfigParser()
            config.read(USER_CONFIG_FILE_PATH)
            if not config.has_section(section):
                config.add_section(section)
            config.set(section, setting, value)
            with open(USER_CONFIG_FILE_PATH, "w") as config_file:
                config.write(config_file)
        else:
            error_message = "Invalid section or setting data type"
            logging.error(error_message)
            print(error_message)
    except Exception as e:
        error_message = f"Error while saving setting: {e}"
        logging.error(error_message)
        print(error_message)
        
def save_settings(save_list):
    try:
        if save_list:
            for section, setting, value in save_list:
                # Check if section and setting are valid strings
                if isinstance(section, str) and isinstance(setting, str):
                    save_setting(section, setting, value)
                else:
                    error_message = "Invalid section or setting data type"
                    logging.error(error_message)
                    print(error_message)
    except Exception as e:
        error_message = f"Error while saving settings: {e}"
        logging.error(error_message)
        print(error_message)

def reset_setting(section, setting):
    try:
        # Check if section and setting are valid strings
        if isinstance(section, str) and isinstance(setting, str):
            config = configparser.ConfigParser()
            config.read(DEFAULT_CONFIG_FILE_PATH)
            if config.has_section(section) and config.has_option(section, setting):
                config.set(section, setting, "")
                with open(USER_CONFIG_FILE_PATH, "w") as config_file:
                    config.write(config_file)
        else:
            error_message = "Invalid section or setting data type"
            logging.error(error_message)
            print(error_message)
    except Exception as e:
        error_message = f"Error while resetting setting: {e}"
        logging.error(error_message)
        print(error_message)

def reset_all_settings():
    try:
        config = configparser.ConfigParser()
        config.read(DEFAULT_CONFIG_FILE_PATH)
        with open(USER_CONFIG_FILE_PATH, "w") as config_file:
            config.write(config_file)
    except Exception as e:
        error_message = f"Error while resetting all settings: {e}"
        logging.error(error_message)
        print(error_message)

def reset_settings(reset_list):
    try:
        if reset_list:
            for section, setting in reset_list:
                # Check if section and setting are valid strings
                if isinstance(section, str) and isinstance(setting, str):
                    reset_setting(section, setting)
                else:
                    error_message = "Invalid section or setting data type"
                    logging.error(error_message)
                    print(error_message)
    except Exception as e:
        error_message = f"Error while resetting settings: {e}"
        logging.error(error_message)
        print(error_message)
