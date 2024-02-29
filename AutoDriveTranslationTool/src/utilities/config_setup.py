# config_setup.py

import os
import customtkinter as ctk

import src.utilities as utils
from GuiFramework.utilities import ConfigManager, file_ops


class ConfigSetup:
    UI_THEMES = ["light", "dark", "system"]
    UI_COLOR_THEMES = ["blue", "dark-blue", "green", "ad-green"]
    UI_LANGUAGES = ["english", "german"]
    DEV_PATH = "AutoDriveTranslationTool" if 'VSAPPIDDIR' in os.environ else ""

    def __init__(self, window, logger):
        self.window = window
        self.logger = logger
        self.config_manager = None
        self.setup_configuration()

    def setup_configuration(self):
        """Sets up the configuration for the application."""
        config_path = os.path.join(self.DEV_PATH, "config")
        self.config_manager = ConfigManager(
            default_config_creator_func=self._create_default_config,
            config_path=config_path,
            default_config_name='default_config.ini',
            custom_config_name='custom_config.ini',
            logger=self.logger
        )
        self.config_manager.load_config()
        self._register_config_variables()
        self._load_settings()

    def _register_config_variables(self):
        """Registers custom variable types and their respective creators and savers."""
        self.config_manager.register_variable_type(ctk.StringVar, lambda value: ctk.StringVar(self.window, value), utils.string_var_saver)
        self.config_manager.register_variable_type(ctk.BooleanVar, lambda value: ctk.BooleanVar(self.window, value), utils.boolean_var_saver)
        self.config_manager.register_variable_type(list, utils.list_creator, utils.list_saver)

    def _load_settings(self):
        """Loads the settings from the configuration and stores them in the ConfigManager."""
        add_var = self.config_manager.add_variable

        add_var(name="locales_dir", value=ctk.StringVar(self.window, "locales"), section="AppSettings")
        add_var(name="locale_updater", value=ctk.BooleanVar(self.window, True), section="AppSettings")

        add_var(name="save_window_size", value=ctk.BooleanVar(self.window, True), section="WindowSettings")
        add_var(name="save_window_pos", value=ctk.BooleanVar(self.window, True), section="WindowSettings")
        add_var(name="center_window_on_startup", value=ctk.BooleanVar(self.window, True), section="WindowSettings")
        add_var(name="window_size", value=ctk.StringVar(self.window, "1366x768"), section="WindowSettings")
        add_var(name="window_position", value=ctk.StringVar(self.window, "0+0"), section="WindowSettings")
        add_var(name="resizeable", value=ctk.BooleanVar(self.window, True), section="WindowSettings")

        add_var(name="use_high_dpi_scaling", value=ctk.BooleanVar(self.window, True), section="AppearanceSettings")
        add_var(name="ui_theme", value=ctk.StringVar(self.window, "System"), section="AppearanceSettings")
        add_var(name="ui_color_theme", value=ctk.StringVar(self.window, "Blue"), section="AppearanceSettings")
        add_var(name="ui_language", value=ctk.StringVar(self.window, "English"), section="AppearanceSettings")

        add_var(name="selected_languages", value=[""], section="TranslationSettings")
        add_var(name="supported_languages", value=["English"], section="TranslationSettings")
        add_var(name="input_path", value="_input", section="TranslationSettings")
        add_var(name="output_path", value="_output", section="TranslationSettings")
        add_var(name="dictionaries_path", value="_dictionaries", section="TranslationSettings")
        add_var(name="whole_word_replacement", value=ctk.BooleanVar(self.window, True), section="TranslationSettings")

        add_var(name="dropdown_ui_themes", value=self.UI_THEMES)
        add_var(name="dropdown_ui_color_themes", value=self.UI_COLOR_THEMES)
        add_var(name="dropdown_ui_languages", value=self.UI_LANGUAGES)

    def _create_default_config(self):
        """Creates the default configuration."""
        return {
            "AppSettings": {
                "locales_dir": "locales",
                "locale_updater": "False"
            },
            "WindowSettings": {
                "save_window_size": "True",
                "save_window_pos": "True",
                "center_window_on_startup": "True",
                "window_size": "1366x768",
                "window_position": "0+0",
                "resizeable": "True",
            },
            "AppearanceSettings": {
                "use_high_dpi_scaling": "True",
                "ui_theme": "System",
                "ui_color_theme": "Blue",
                "ui_language": "English"
            },
            "TranslationSettings": {
                "selected_languages": "English",
                "supported_languages": "English,French,German,Italian,Russian",
                "input_path": "_input",
                "output_path": "_output",
                "dictionaries_path": "_dictionaries",
                "whole_word_replacement": "True"
            }
        }
