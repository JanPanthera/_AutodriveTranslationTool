# config_setup.py

import os
import customtkinter as ctk

import src.utilities as utils
from GuiFramework.src.utilities import ConfigManager, file_ops


class ConfigSetup:
    def __init__(self, dev_path, window, logger):
        self.dev_path = dev_path
        self.window = window
        self.logger = logger
        self.config_manager = None
        self.setup_configuration()

    def setup_configuration(self):
        config_path = os.path.join(self.dev_path, "config")
        self.config_manager = ConfigManager(
            default_config_creator_func=self._create_default_config,
            config_path=config_path,
            default_config_name='default_config',
            custom_config_name='custom_config',
            logger=self.logger
        )
        self.config_manager.load_config()
        # self.config_manager.reset_all_settings() # DEBUG
        self._register_config_variables()
        self._load_settings()

    def _register_config_variables(self):
        self.config_manager.register_variable_type(ctk.StringVar, lambda value: ctk.StringVar(self.window, value), utils.string_var_saver)
        self.config_manager.register_variable_type(ctk.BooleanVar, lambda value: ctk.BooleanVar(self.window, value), utils.boolean_var_saver)
        self.config_manager.register_variable_type(list, utils.list_creator, utils.list_saver)

    def _load_settings(self):
        join = os.path.join
        add_var = self.config_manager.add_variable
        get_var = self.config_manager.get_variable
        set_var = self.config_manager.set_variable
        add_var(name="ui_theme", value=ctk.StringVar(self.window, "System"), section="AppSettings")
        add_var(name="ui_color_theme", value=ctk.StringVar(self.window, "Blue"), section="AppSettings")
        add_var(name="ui_language", value=ctk.StringVar(self.window, "English"), section="AppSettings")
        add_var(name="locales_dir", value=join(self.dev_path, "locales"))
        add_var(name="locale_updater", value=ctk.BooleanVar(self.window, True))

        add_var(name="dropdown_ui_themes", value=["light", "dark", "system"])
        add_var(name="dropdown_ui_color_themes", value=["blue", "dark-blue", "green", "ad-green"])
        add_var(name="dropdown_ui_languages", value=["english", "german"])

        add_var(name="use_high_dpi_scaling", value=ctk.BooleanVar(self.window, True), section="WindowSettings")

        add_var(name="save_window_size", value=ctk.BooleanVar(self.window, True), section="SaveOnWindowClose")
        add_var(name="save_window_pos", value=ctk.BooleanVar(self.window, True), section="SaveOnWindowClose")
        add_var(name="save_selected_languages", value=ctk.BooleanVar(self.window, False), section="SaveOnWindowClose")

        add_var(name="input_path", value="_input", section="TranslationSettings")
        add_var(name="output_path", value="_output", section="TranslationSettings")
        add_var(name="dictionaries_path", value="_dictionaries", section="TranslationSettings")
        add_var(name="selected_languages", value="", section="TranslationSettings")

        add_var(name="supported_languages", value=["English"], section="TranslationSettings")

        add_var(name="dictionary_files_list", value=file_ops.get_all_file_names_in_directory(join(self.dev_path, get_var("dictionaries_path"))))
        add_var(name="whole_word_replacement", value=ctk.BooleanVar(self.window, True), section="TranslationSettings")

    def _create_default_config(self):
        return {
            "AppSettings": {
                "ui_theme": "System",
                "ui_color_theme": "green",
                "ui_language": "English",
                "locales_dir": "locales",
                "locale_updater": "False"
            },
            "WindowSettings": {
                "window_title": "AutoDrive Translation Tool",
                "window_icon": "resources/ad_icon.ico",
                "window_size": "2560x1440",
                "window_position": "0+0",
                "use_high_dpi_scaling": "True",
                "centered": "True"
            },
            "SaveOnWindowClose": {
                "save_window_size": "True",
                "save_window_pos": "True",
                "save_selected_languages": "False"
            },
            "TranslationSettings": {
                "selected_languages": "English",
                "supported_languages": "Chinese,English,French,German,Italian,Japanese,Korean,Portuguese,Russian,Spanish",
                "input_path": "_input",
                "output_path": "_output",
                "dictionaries_path": "_dictionaries",
                "whole_word_replacement": "False"
            }
        }
