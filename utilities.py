import configparser
from email.policy import default
import os

# Define paths for both the default and the user-specific configuration files
DEFAULT_CONFIG_FILE_PATH = "config/config-default.ini"
USER_CONFIG_FILE_PATH = "config/config-user.ini"

def load_setting(section, setting, default_value=None, default_config=False):
    config = configparser.ConfigParser()
    config_path = USER_CONFIG_FILE_PATH if os.path.exists(USER_CONFIG_FILE_PATH) or not default_config else DEFAULT_CONFIG_FILE_PATH
    config.read(config_path)
    if config.has_section(section) and config.has_option(section, setting):
        return config.get(section, setting)
    else:
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
    with open(USER_CONFIG_FILE_PATH, 'w') as user_config_file:
        config.write(user_config_file)
