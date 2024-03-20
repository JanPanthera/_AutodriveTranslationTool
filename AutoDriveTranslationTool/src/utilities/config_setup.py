# AutoDriveTranslationTool/src/utilities/config_setup.py

import customtkinter as ctk

from AutoDriveTranslationTool.src.utilities.custom_type_handlers import (
    CtkStringVarTypeHandler, CtkBooleanVarTypeHandler, ListTypeHandler, TupleTypeHandler
)
from AutoDriveTranslationTool.src.core.constants import (
    LOGGER_NAME, CONFIG_NAME, UI_THEMES, UI_COLOR_THEMES, UI_LANGUAGES
)

from GuiFramework.utilities import FileOps, Logger
from GuiFramework.utilities.config import ConfigHandler, ConfigFileHandlerConfig
from GuiFramework.utilities.config.config_types import ConfigKeyList as CKL


class ConfigSetup:

    def __init__(self, window):
        self.window = window
        self.logger = Logger.get_logger(LOGGER_NAME)

        ConfigHandler.add_config(
            config_name=CONFIG_NAME,
            handler_config=ConfigFileHandlerConfig(
                config_path=FileOps.resolve_development_path(__file__, "config", root_marker="main.py"),
                default_config_name="default_config.ini",
                custom_config_name="custom_config.ini",
            ),
            default_config=self._create_default_config(),
            custom_type_handlers=[
                ListTypeHandler(),
                TupleTypeHandler(),
                CtkStringVarTypeHandler(self.window),
                CtkBooleanVarTypeHandler(self.window),
            ]
        )
        self.create_config_keys()

    def create_config_keys(self):
        config_data = [
            {"name": "locale_updater", "section": "AppSettings", "type_": ctk.BooleanVar, "value": ctk.BooleanVar(value=False)},

            {"name": "locales_path", "section": "AppSettings", "type_": str, "value": "locales", "init_from_file": False, "save_to_file": False},
            {"name": "resources_path", "section": "AppSettings", "type_": str, "value": "resources", "init_from_file": False, "save_to_file": False},
            {"name": "input_path", "section": "AppSettings", "type_": str, "value": "_input", "init_from_file": False, "save_to_file": False},
            {"name": "output_path", "section": "AppSettings", "type_": str, "value": "_output", "init_from_file": False, "save_to_file": False},
            {"name": "dictionaries_path", "section": "AppSettings", "type_": str, "value": "_dictionaries", "init_from_file": False, "save_to_file": False},

            {"name": "save_window_size", "section": "WindowSettings", "type_": ctk.BooleanVar, "value": ctk.BooleanVar(value=True)},
            {"name": "save_window_pos", "section": "WindowSettings", "type_": ctk.BooleanVar, "value": ctk.BooleanVar(value=True)},
            {"name": "center_window_on_startup", "section": "WindowSettings", "type_": ctk.BooleanVar, "value": ctk.BooleanVar(value=True)},
            {"name": "window_size", "section": "WindowSettings", "type_": ctk.StringVar, "value": ctk.StringVar(value="1366x768")},
            {"name": "window_position", "section": "WindowSettings", "type_": ctk.StringVar, "value": ctk.StringVar(value="0+0")},
            {"name": "resizeable", "section": "WindowSettings", "type_": ctk.BooleanVar, "value": ctk.BooleanVar(value=True)},

            {"name": "use_high_dpi_scaling", "section": "AppearanceSettings", "type_": ctk.BooleanVar, "value": ctk.BooleanVar(value=True)},
            {"name": "ui_theme", "section": "AppearanceSettings", "type_": ctk.StringVar, "value": ctk.StringVar(value="System")},
            {"name": "ui_color_theme", "section": "AppearanceSettings", "type_": ctk.StringVar, "value": ctk.StringVar(value="Blue")},
            {"name": "ui_language", "section": "AppearanceSettings", "type_": ctk.StringVar, "value": ctk.StringVar(value="English")},

            {"name": "selected_languages", "section": "TranslationSettings", "type_": list, "value": [""]},
            {"name": "supported_languages", "section": "TranslationSettings", "type_": list, "value": ["English", "French", "German", "Italian", "Russian"]},
            {"name": "whole_word_replacement", "section": "TranslationSettings", "type_": ctk.BooleanVar, "value": ctk.BooleanVar(value=True)},

            {"name": "dropdown_ui_themes", "section": "DropdownSettings", "type_": list, "value": UI_THEMES},
            {"name": "dropdown_ui_color_themes", "section": "DropdownSettings", "type_": list, "value": UI_COLOR_THEMES},
            {"name": "dropdown_ui_languages", "section": "DropdownSettings", "type_": list, "value": UI_LANGUAGES}
        ]
        for data in config_data:
            CKL.add_ConfigKey(
                name=data["name"],
                section=data.get("section", "Default"),
                type_=data.get("type_", None),
                save_to_file=data.get("save_to_file", True),
                auto_save=data.get("auto_save", True),
                config_name=data.get("config_name", CONFIG_NAME)
            )
            ConfigHandler.add_variable(
                config_key=getattr(CKL, data["name"].upper()),
                value=data.get("value", None),
                default_value=data.get("default_value", None),
                init_from_file=data.get("init_from_file", True)
            )
        paths = [CKL.LOCALES_PATH, CKL.RESOURCES_PATH, CKL.INPUT_PATH, CKL.OUTPUT_PATH, CKL.DICTIONARIES_PATH]
        for path in paths:
            original_path = ConfigHandler.get_variable_value(path)
            ConfigHandler.set_variable_value(path, FileOps.resolve_development_path(__file__, original_path, root_marker="main.py"))

    def _create_default_config(self):
        """Creates the default configuration."""
        return {
            "AppSettings": {
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
                "supported_languages": "English,French,German,Italian,Russian,Spanish",
                "whole_word_replacement": "True"
            }
        }
