import configparser
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

def save_window_geometry(window):
    save_setting("WindowGeometry", "width", str(window.winfo_width()))
    save_setting("WindowGeometry", "height", str(window.winfo_height()))
    save_setting("WindowGeometry", "pos_x", str(window.winfo_x()))
    save_setting("WindowGeometry", "pos_y", str(window.winfo_y()))

def load_window_geometry(window):
    width = load_setting("WindowGeometry", "width", default_value="1366")
    height = load_setting("WindowGeometry", "height", default_value="768")
    pos_x = load_setting("WindowGeometry", "pos_x", default_value="100")
    pos_y = load_setting("WindowGeometry", "pos_y", default_value="100")

    window.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
