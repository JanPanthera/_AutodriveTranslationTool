# AutoDriveTranslationTool/src/components/options_frame/options_frame_logic.py

import customtkinter as ctk

from GuiFramework.utilities import FileOps
from GuiFramework.utilities.gui_utils import GuiUtils
from GuiFramework.utilities.config import ConfigHandler as CH
from GuiFramework.utilities.config.config_types import ConfigKeyList as CKL


class OptionsFrameLogic:

    def __init__(self, app_instance, gui_instance) -> None:
        self.app_instance = app_instance
        self.gui_instance = gui_instance
        self.localization_manager = self.app_instance.localization_manager
        self.loc = self.localization_manager.localize

    def _on_reset_everything_button(self):
        settings_to_reset = [
            ["WindowSettings", self.WINDOW_SIZE],
            ["WindowSettings", self.WINDOW_POSITION],
            ["WindowSettings", self.CENTER_WINDOW_ON_STARTUP],
            ["WindowSettings", self.SAVE_WINDOW_SIZE],
            ["WindowSettings", self.SAVE_WINDOW_POS],

            ["AppearanceSettings", self.USE_HIGH_DPI_SCALING],
            ["AppearanceSettings", self.UI_THEME],
            ["AppearanceSettings", self.UI_COLOR_THEME],
            ["AppearanceSettings", self.UI_LANGUAGE],

            ["TranslationSettings", self.WHOLE_WORD_REPLACEMENT]
        ]
        # TODO: Adapt to new system here, as well make sure the ConfigHandler uses the ConfigKeys as well
        # def reset_settings(config_name: str, settings: Dict[str, List[str]], auto_save: bool = True) -> None:
        GuiUtils.update_checkbox_state(self.checkbox_save_window_size, self.SAVE_WINDOW_SIZE, self.config_manager)
        GuiUtils.update_checkbox_state(self.checkbox_save_window_pos, self.SAVE_WINDOW_POS, self.config_manager)
        GuiUtils.update_checkbox_state(self.checkbox_center_window_on_startup, self.CENTER_WINDOW_ON_STARTUP, self.config_manager)
        GuiUtils.update_checkbox_state(self.checkbox_use_high_dpi_scaling, self.USE_HIGH_DPI_SCALING, self.config_manager)
        GuiUtils.update_checkbox_state(self.checkbox_whole_word_replacement, self.WHOLE_WORD_REPLACEMENT, self.config_manager)
        self.window.set_ui_theme((CH.get_variable_value(CKL.UI_THEME)).get().lower())
        self.window.set_ui_color_theme((CH.get_variable_value(CKL.UI_COLOR_THEME)).get().lower())
        self.localization_manager.set_active_language((CH.get_variable_value(CKL.UI_LANGUAGE)).get())

    def _on_center_window_on_startup_checkbox(self):
        CH.set_variable_value(CKL.CENTER_WINDOW_ON_STARTUP, ctk.BooleanVar(self, self.checkbox_center_window_on_startup.get()))

    def _on_save_window_size_checkbox(self):
        CH.set_variable_value(CKL.SAVE_WINDOW_SIZE, ctk.BooleanVar(self, self.checkbox_save_window_size.get()))

    def _on_save_window_pos_checkbox(self):
        CH.set_variable_value(CKL.SAVE_WINDOW_POS, ctk.BooleanVar(self, self.checkbox_save_window_pos.get()))

    def _on_reset_window_settings_button(self):
        settings_to_reset = [
            ["WindowSettings", self.CENTER_WINDOW_ON_STARTUP],
            ["WindowSettings", self.SAVE_WINDOW_SIZE],
            ["WindowSettings", self.SAVE_WINDOW_POS],
        ]
        # TODO: Adapt to new system here, as well make sure the ConfigHandler uses the ConfigKeys as well
        # def reset_settings(config_name: str, settings: Dict[str, List[str]], auto_save: bool = True) -> None:
        # CH.reset_settings(settings_to_reset)
        # gui_utils.update_checkbox_state(self.checkbox_save_window_size, self.SAVE_WINDOW_SIZE, self.config_manager)
        # gui_utils.update_checkbox_state(self.checkbox_save_window_pos, self.SAVE_WINDOW_POS, self.config_manager)
        GuiUtils.update_checkbox_state(self.checkbox_center_window_on_startup, self.CENTER_WINDOW_ON_STARTUP, self.config_manager)

    def _on_reset_window_size_button(self):
        settings_to_reset = [
            ["WindowSettings", self.WINDOW_SIZE]
        ]
        # TODO: Adapt to new system here, as well make sure the ConfigHandler uses the ConfigKeys as well
        # def reset_settings(config_name: str, settings: Dict[str, List[str]], auto_save: bool = True) -> None:
        # CH.reset_settings(settings_to_reset)
        width, height = map(int, (CH.get_variable_value(CKL.WINDOW_SIZE)).split("x"))
        self.window.set_window_size((width, height))

    def _on_reset_window_pos_button(self):
        settings_to_reset = [
            ["WindowSettings", self.WINDOW_POSITION]
        ]
        # TODO: Adapt to new system here, as well make sure the ConfigHandler uses the ConfigKeys as well
        # def reset_settings(config_name: str, settings: Dict[str, List[str]], auto_save: bool = True) -> None:
        # CH.reset_settings(settings_to_reset)
        pos_x, pos_y = map(int, (CH.get_variable_value(CKL.WINDOW_POSITION)).split("+"))
        self.window.set_window_position((pos_x, pos_y))

    def _on_use_high_dpi_scaling_checkbox(self):
        CH.set_variable_value(CKL.USE_HIGH_DPI_SCALING, ctk.BooleanVar(self, self.checkbox_use_high_dpi_scaling.get()))
        self.window.set_high_dpi(CH.get_variable_value(CKL.USE_HIGH_DPI_SCALING).get())

    def _on_ui_theme_dropdown(self, selected_theme=None):
        theme_key = self.localization_manager.reverse_localize(selected_theme)
        CH.set_variable_value(CKL.UI_THEME, ctk.StringVar(self, theme_key[0].upper() + theme_key[1:]))
        self.window.set_ui_theme(theme_key)

    def _on_ui_color_theme_dropdown(self, selected_color_theme=None):
        color_theme_key = self.localization_manager.reverse_localize(selected_color_theme)
        CH.set_variable_value(CKL.UI_COLOR_THEME, ctk.StringVar(self, color_theme_key[0].upper() + color_theme_key[1:]))
        ui_color_theme = color_theme_key if color_theme_key in ["blue", "dark-blue", "green"] else FileOps.join_paths(CH.get_variable_value(CKL.RESOURCES_PATH), "themes", f"{color_theme_key}.json")
        self.window.set_ui_color_theme(ui_color_theme)

    def _on_ui_language_dropdown(self, selected_language=None):
        language_key = self.localization_manager.reverse_localize(selected_language)
        CH.set_variable_value(CKL.UI_LANGUAGE, ctk.StringVar(self, language_key[0].upper() + language_key[1:]))
        self.localization_manager.set_active_language(language_key)

    def _on_reset_ui_appearance_settings_button(self):
        settings_to_reset = [
            ["AppearanceSettings", self.USE_HIGH_DPI_SCALING],
            ["AppearanceSettings", self.UI_THEME],
            ["AppearanceSettings", self.UI_COLOR_THEME],
            ["AppearanceSettings", self.UI_LANGUAGE]
        ]
        # CH.reset_settings(settings_to_reset)
        # gui_utils.update_checkbox_state(self.checkbox_use_high_dpi_scaling, self.USE_HIGH_DPI_SCALING, self.config_manager)
        # self.window.set_ui_theme(self.get_var(self.UI_THEME).get().lower())
        self.window.set_ui_color_theme((CH.get_variable_value(CKL.UI_COLOR_THEME)).get().lower())
        self.localization_manager.set_active_language((CH.get_variable_value(CKL.UI_LANGUAGE)).get())

    def _on_whole_word_replacement_checkbox(self):
        CH.set_variable_value(CKL.WHOLE_WORD_REPLACEMENT, ctk.BooleanVar(self, self.checkbox_whole_word_replacement.get()))

    # Helper methods
    def _translate_list(self, list_to_translate):
        return [self.loc(item) for item in list_to_translate]