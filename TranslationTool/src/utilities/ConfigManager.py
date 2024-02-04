import configparser
import os

class ConfigManager():
    def __init__(self, default_config_path='config/config-default.ini', custom_config_path='config/config-custom.ini'):
        self.default_config_path = default_config_path
        self.custom_config_path = custom_config_path
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        """Load the custom configuration file into memory, falling back to the default if necessary."""
        if 'VSAPPIDDIR' in os.environ:  # Adjust paths if running in Visual Studio
            self.default_config_path = os.path.join("TranslationTool/", self.default_config_path)
            self.custom_config_path = os.path.join("TranslationTool/", self.custom_config_path)

        if not os.path.exists(self.custom_config_path) and os.path.exists(self.default_config_path):
            # Copy default config to custom if custom does not exist but default does
            with open(self.default_config_path, 'r', encoding='utf-8') as default_file, open(self.custom_config_path, 'w', encoding='utf-8') as custom_file:
                custom_file.write(default_file.read())

        self.config.read([self.default_config_path, self.custom_config_path], encoding='utf-8')  # Custom will override default

    def get(self, section, option, default_value=None):
        """Get a value from the configuration, returning a default if not found."""
        try:
            return self.config.get(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return default_value

    def save(self, section, option, value):
        """Save a value to the custom configuration."""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, str(value))
        # Ensure that the configuration is written with UTF-8 encoding
        with open(self.custom_config_path, 'w', encoding='utf-8') as f:
            self.config.write(f)

    def save_settings(self, settings):
        """Save multiple settings to the custom configuration."""
        for section, option, value in settings:
            if not self.config.has_section(section):
                self.config.add_section(section)
            self.config.set(section, option, value)
        # Ensure that the configuration is written with UTF-8 encoding
        with open(self.custom_config_path, 'w', encoding='utf-8') as f:
            self.config.write(f)

    def reset_settings(self, settings):
        """Reset specific settings to their default values by removing them from the custom configuration."""
        for section, option in settings:
            if self.config.has_section(section) and self.config.has_option(section, option):
                self.config.remove_option(section, option)
        # Ensure that the configuration is written with UTF-8 encoding
        with open(self.custom_config_path, 'w', encoding='utf-8') as f:
            self.config.write(f)

    def reset_all_settings(self):
        """Reset all settings to their default values by removing the custom configuration file."""
        if os.path.exists(self.custom_config_path):
            os.remove(self.custom_config_path)
        self.load_config()