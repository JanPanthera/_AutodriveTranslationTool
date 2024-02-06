import configparser
import logging
import os


class ConfigManager():
    def __init__(self, custom_logger=None, default_config_path='config/config-default.ini', custom_config_path='config/config-custom.ini'):
        """
        Initialize the ConfigManager class.

        Args:
            custom_logger: The custom logger object.
            default_config_path (str): The path to the default configuration file.
            custom_config_path (str): The path to the custom configuration file.
        """
        if custom_logger is None:
            custom_logger = logging.getLogger(__name__)
        self.custom_logger = custom_logger
        self.default_config_path = default_config_path
        self.custom_config_path = custom_config_path
        self.default_config = configparser.ConfigParser()
        self.custom_config = configparser.ConfigParser()
        self.dynamic_store = {}
        self.load_config()

    def load_config(self):
        """
        Load the configuration from the default and custom configuration files in to memory.

        Raises:
            FileNotFoundError: If the configuration file is not found.
            configparser.Error: If there is an error while loading the configuration.
        """
        try:
            if 'VSAPPIDDIR' in os.environ:
                self.default_config_path = os.path.join("TranslationTool/", self.default_config_path)
                self.custom_config_path = os.path.join("TranslationTool/", self.custom_config_path)

            if not os.path.exists(self.custom_config_path) and os.path.exists(self.default_config_path):
                with open(self.default_config_path, 'r', encoding='utf-8') as default_file:
                    default_content = default_file.read()
                with open(self.custom_config_path, 'w', encoding='utf-8') as custom_file:
                    custom_file.write(default_content)

            self.default_config.read(self.default_config_path, encoding='utf-8')
            self.custom_config.read([self.default_config_path, self.custom_config_path], encoding='utf-8')
        except FileNotFoundError as e:
            self.custom_logger.error(f"Configuration file not found: {e}")
        except configparser.Error as e:
            self.custom_logger.error(f"Failed to load configuration: {e}")

    def save_setting(self, section, option, value):
        """
        Save a setting in the custom configuration file.

        Args:
            section (str): The section name.
            option (str): The option name.
            value: The value to be saved.
        """
        try:
            if not self.custom_config.has_section(section):
                self.custom_config.add_section(section)
            self.custom_config.set(section, option, str(value))
            with open(self.custom_config_path, 'w', encoding='utf-8') as f:
                self.custom_config.write(f)
        except configparser.Error as e:
            self.custom_logger.error(f"Failed to save '{option}' in section '{section}': {e}")

    def save_settings(self, settings):
        """
        Save multiple settings in the custom configuration file.

        Args:
            settings (list): A list of tuples containing the section, option, and value for each setting.
        """
        try:
            for section, option, value in settings:
                self.save_setting(section, option, value)
        except configparser.Error as e:
            self.custom_logger.error(f"Failed to save multiple settings: {e}")

    def load_setting(self, section, option, default_value=None, force_default=False):
        """
        Load a setting from the custom configuration file.

        Args:
            section (str): The section name.
            option (str): The option name.
            default_value: The default value to return if the setting is not found.
            force_default (bool): Whether to force using the default configuration file.

        Returns:
            The value of the setting, or the default value if the setting is not found.
        """
        try:
            if force_default:
                return self.default_config.get(section, option)
            else:
                return self.custom_config.get(section, option, fallback=default_value)
        except configparser.NoSectionError:
            self.custom_logger.warning(f"Section '{section}' not found in configuration. Using default value.")
            return default_value
        except configparser.Error as e:
            self.custom_logger.error(f"Failed to load setting '{option}' in section '{section}': {e}")
            return default_value

    def reset_setting(self, section, option):
        """
        Reset a setting to its default value in the custom configuration file.

        Args:
            section (str): The section name.
            option (str): The option name.
        """
        try:
            default_value = self.load_setting(section, option, force_default=True)
            self.save_setting(section, option, default_value)
        except configparser.Error as e:
            self.custom_logger.error(f"Failed to reset '{option}' in section '{section}': {e}")

    def reset_settings(self, settings):
        """
        Reset multiple settings to their default values in the custom configuration file.

        Args:
            settings (list): A list of tuples containing the section and option for each setting.
        """
        try:
            for section, option in settings:
                self.reset_setting(section, option)
        except configparser.Error as e:
            self.custom_logger.error(f"Failed to reset multiple settings: {e}")

    def reset_all_settings(self):
        """
        Reset all settings to their default values in the custom configuration file.
        """
        try:
            default_settings = [(section, option) for section in self.custom_config.sections() for option in self.custom_config.options(section)]
            self.reset_settings(default_settings)
        except configparser.Error as e:
            self.custom_logger.error(f"Failed to reset all settings: {e}")

    def add_var(self, name, value):
        """
        Add a variable to the dynamic store.

        Args:
            name (str): The name of the variable.
            value: The value of the variable.
        """
        self.dynamic_store[name] = value

    def add_vars(self, variables):
        """
        Add multiple variables to the dynamic store.

        Args:
            variables (dict): A dictionary containing the variables to be added.
        """
        self.dynamic_store.update(variables)

    def remove_var(self, name):
        """
        Remove a variable from the dynamic store.

        Args:
            name (str): The name of the variable to be removed.
        """
        self.dynamic_store.pop(name, None)

    def remove_vars(self, names):
        """
        Remove multiple variables from the dynamic store.

        Args:
            names (list): A list of variable names to be removed.
        """
        for name in names:
            self.dynamic_store.pop(name, None)

    def set_var(self, name, value):
        """
        Set the value of a variable in the dynamic store.

        Args:
            name (str): The name of the variable.
            value: The new value of the variable.
        """
        self.dynamic_store[name] = value

    def set_vars(self, variables):
        """
        Set the values of multiple variables in the dynamic store.

        Args:
            variables (dict): A dictionary containing the variable names and their new values.
        """
        self.dynamic_store.update(variables)

    def get_var(self, name, default_value=None):
        """
        Get the value of a variable from the dynamic store.

        Args:
            name (str): The name of the variable.
            default_value: The default value to return if the variable is not found.

        Returns:
            The value of the variable, or the default value if the variable is not found.
        """
        return self.dynamic_store.get(name, default_value)