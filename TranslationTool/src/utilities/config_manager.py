# config_manager.py

import configparser
import os

from TranslationTool.src.utilities.utils import trigger_debug_break

class ConfigManager():
    def __init__(self, custom_logger, default_config_path='config/config-default.ini', custom_config_path='config/config-custom.ini'):
        """
        Initialize the ConfigManager with paths to the default and custom configuration files.
        Also sets up a custom logger for logging messages and a dynamic store for runtime variables.

        Args:
            custom_logger: Logger object for logging messages.
            default_config_path (str): Path to the default configuration file.
            custom_config_path (str): Path to the custom configuration file, which overrides the default.
        """
        self.custom_logger = custom_logger
        self.default_config_path = default_config_path
        self.custom_config_path = custom_config_path
        self.config = configparser.ConfigParser()
        self.dynamic_store = {}  # Store for additional runtime variables
        self.load_config()  # Load configurations immediately upon initialization

    def load_config(self):
        """
        Load configuration files into memory, using the custom configuration to override the default.
        Adjusts file paths if running in a Visual Studio environment and copies the default configuration
        to the custom path if the custom file does not exist but the default does.
        """
        try:
            # Adjust configuration paths if running within Visual Studio to accommodate different working directories
            if 'VSAPPIDDIR' in os.environ:
                self.default_config_path = os.path.join("TranslationTool/", self.default_config_path)
                self.custom_config_path = os.path.join("TranslationTool/", self.custom_config_path)

            # Copy default configuration to custom configuration path if only the default exists
            if not os.path.exists(self.custom_config_path) and os.path.exists(self.default_config_path):
                with open(self.default_config_path, 'r', encoding='utf-8') as default_file, open(self.custom_config_path, 'w', encoding='utf-8') as custom_file:
                    custom_file.write(default_file.read())

            # Read the configuration files, allowing the custom configuration to override the default settings
            self.config.read([self.default_config_path, self.custom_config_path], encoding='utf-8')
        except Exception as e:
            # Log failure and trigger a debug break if in a debug environment
            self.custom_logger.error(f"Failed to load configuration: {e}")
            trigger_debug_break()

    def get(self, section, option, default_value=None):
        """
        Retrieve a configuration value from the specified section and option.
        Returns a default value if the specified section or option is not found.

        Args:
            section (str): The section in the configuration file.
            option (str): The option within the section to retrieve.
            default_value: The default value to return if the section or option is not found.

        Returns:
            The configuration value if found; otherwise, the specified default value.
        """
        try:
            return self.config.get(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError):
            # Log a warning and return the default value if the section or option is missing
            self.custom_logger.warning(f"Section '{section}' or option '{option}' not found in configuration. Using default value.")
            return default_value

    def save(self, section, option, value):
        """
        Save a configuration value to the specified section and option in the custom configuration file.

        Args:
            section (str): The section in the configuration file to save the value under.
            option (str): The option within the section where the value will be saved.
            value: The value to be saved.
        """
        try:
            # Add the section if it doesn't already exist
            if not self.config.has_section(section):
                self.config.add_section(section)
            # Set the option value within the section
            self.config.set(section, option, str(value))
            # Write the updated configuration to the custom configuration file
            with open(self.custom_config_path, 'w', encoding='utf-8') as f:
                self.config.write(f)
            # Log the successful save operation
            self.custom_logger.info(f"Saved '{option}' in section '{section}' to configuration.")
        except Exception as e:
            # Log failure and trigger a debug break if in a debug environment
            self.custom_logger.error(f"Failed to save '{option}' in section '{section}': {e}")
            trigger_debug_break()

    def save_settings(self, settings):
        """
        Save multiple configuration settings to the custom configuration file.

        Args:
            settings (list of tuples): A list where each tuple contains (section, option, value) to be saved.
        """
        try:
            for section, option, value in settings:
                # Add the section if it doesn't already exist
                if not self.config.has_section(section):
                    self.config.add_section(section)
                # Set the option value within the section
                self.config.set(section, option, value)
            # Write the updated configuration to the custom configuration file
            with open(self.custom_config_path, 'w', encoding='utf-8') as f:
                self.config.write(f)
            # Log the successful save of multiple settings
            self.custom_logger.info("Successfully saved multiple settings to configuration.")
        except Exception as e:
            # Log failure and trigger a debug break if in a debug environment
            self.custom_logger.error(f"Failed to save multiple settings: {e}")
            trigger_debug_break()

    def reset_settings(self, settings):
        """
        Reset specific configuration settings to their default values by removing them from the custom configuration file.

        Args:
            settings (list of tuples): A list where each tuple contains (section, option) to be reset.
        """
        try:
            for section, option in settings:
                # Remove the specified option from the section if it exists
                if self.config.has_section(section) and self.config.has_option(section, option):
                    self.config.remove_option(section, option)
            # Write the updated configuration to reflect the removals
            with open(self.custom_config_path, 'w', encoding='utf-8') as f:
                self.config.write(f)
            # Log the successful reset of specified settings
            self.custom_logger.info("Successfully reset specified settings to default values.")
        except Exception as e:
            # Log failure and trigger a debug break if in a debug environment
            self.custom_logger.error(f"Failed to reset specified settings: {e}")
            trigger_debug_break()

    def reset_all_settings(self):
        """
        Reset all configuration settings to their default values by removing the custom configuration file.
        """
        try:
            # Remove the custom configuration file if it exists
            if os.path.exists(self.custom_config_path):
                os.remove(self.custom_config_path)
            # Reload configuration to revert to default settings
            self.load_config()
            # Log the successful reset of all settings
            self.custom_logger.info("Successfully reset all settings to default values.")
        except Exception as e:
            # Log failure and trigger a debug break if in a debug environment
            self.custom_logger.error(f"Failed to reset all settings: {e}")
            trigger_debug_break()

    def add_variable(self, name, value):
        """
        Add a runtime variable to the dynamic store.

        Args:
            name (str): The name of the variable to add.
            value: The value of the variable.
        """
        try:
            # Add the variable to the dynamic store
            self.dynamic_store[name] = value
            # Log the successful addition of the variable
            self.custom_logger.info(f"Added variable '{name}' to dynamic store.")
        except Exception as e:
            # Log failure and trigger a debug break if in a debug environment
            self.custom_logger.error(f"Failed to add variable '{name}' to dynamic store: {e}")
            trigger_debug_break()

    def add_variables(self, variables):
        """
        Add multiple runtime variables to the dynamic store.

        Args:
            variables (dict): A dictionary of variable names and their corresponding values.
        """
        try:
            # Add the variables to the dynamic store
            self.dynamic_store.update(variables)
            # Log the successful addition of the variables
            self.custom_logger.info("Added multiple variables to dynamic store.")
        except Exception as e:
            # Log failure and trigger a debug break if in a debug environment
            self.custom_logger.error(f"Failed to add multiple variables to dynamic store: {e}")
            trigger_debug_break()

    def remove_variable(self, name):
        """
        Remove a runtime variable from the dynamic store.

        Args:
            name (str): The name of the variable to remove.
        """
        try:
            # Remove the variable from the dynamic store
            del self.dynamic_store[name]
            # Log the successful removal of the variable
            self.custom_logger.info(f"Removed variable '{name}' from dynamic store.")
        except Exception as e:
            # Log failure and trigger a debug break if in a debug environment
            self.custom_logger.error(f"Failed to remove variable '{name}' from dynamic store: {e}")
            trigger_debug_break()

    def remove_variables(self, names):
        """
        Remove multiple runtime variables from the dynamic store.

        Args:
            names (list): A list of variable names to remove.
        """
        try:
            # Remove the variables from the dynamic store
            for name in names:
                del self.dynamic_store[name]
            # Log the successful removal of the variables
            self.custom_logger.info("Removed multiple variables from dynamic store.")
        except Exception as e:
            # Log failure and trigger a debug break if in a debug environment
            self.custom_logger.error(f"Failed to remove multiple variables from dynamic store: {e}")
            trigger_debug_break()

    def get_var(self, name, default_value=None):
        """
        Get a runtime variable from the dynamic store, returning a default value if the variable is not found.

        Args:
            name (str): The name of the variable to retrieve.
            default_value: The default value to return if the variable is not found.

        Returns:
            The value of the variable if found; otherwise, the specified default value.
        """
        try:
            # Retrieve the variable from the dynamic store, or return the default value if not found
            return self.dynamic_store.get(name, default_value)
        except Exception as e:
            # Log failure and trigger a debug break if in a debug environment
            self.custom_logger.error(f"Failed to get variable '{name}' from dynamic store: {e}")
            trigger_debug_break()
            return default_value

    def set_var(self, name, value):
        """
        Set the value of a runtime variable in the dynamic store.

        Args:
            name (str): The name of the variable to set.
            value: The new value for the variable.
        """
        try:
            # Set the variable in the dynamic store
            self.dynamic_store[name] = value
            # Log the successful update of the variable
            self.custom_logger.info(f"Set variable '{name}' in dynamic store.")
        except Exception as e:
            # Log failure and trigger a debug break if in a debug environment
            self.custom_logger.error(f"Failed to set variable '{name}' in dynamic store: {e}")
            trigger_debug_break()
