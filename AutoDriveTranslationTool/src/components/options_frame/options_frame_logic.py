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
        self.window = self.app_instance.window

        self.localization_manager = self.app_instance.localization_manager
        self.loc = self.localization_manager.localize

    def _on_center_window_on_startup_checkbox(self) -> None:
        """Toggle centering the window on startup."""
        CH.set_variable_value(CKL.CENTER_WINDOW_ON_STARTUP, ctk.BooleanVar(self.gui_instance, self.gui_instance.checkbox_center_window_on_startup.get()))

    def _on_save_window_size_checkbox(self) -> None:
        """Toggle saving the window size."""
        CH.set_variable_value(CKL.SAVE_WINDOW_SIZE, ctk.BooleanVar(self.gui_instance, self.gui_instance.checkbox_save_window_size.get()))

    def _on_save_window_pos_checkbox(self) -> None:
        """Toggle saving the window position."""
        CH.set_variable_value(CKL.SAVE_WINDOW_POS, ctk.BooleanVar(self.gui_instance, self.gui_instance.checkbox_save_window_pos.get()))

    def _on_reset_window_settings_button(self) -> None:
        """Reset window settings to default."""
        CH.reset_settings([
            CKL.CENTER_WINDOW_ON_STARTUP,
            CKL.SAVE_WINDOW_SIZE,
            CKL.SAVE_WINDOW_POS
        ])
        self._update_checkboxes({
            CKL.CENTER_WINDOW_ON_STARTUP: self.gui_instance.checkbox_center_window_on_startup,
            CKL.SAVE_WINDOW_SIZE: self.gui_instance.checkbox_save_window_size,
            CKL.SAVE_WINDOW_POS: self.gui_instance.checkbox_save_window_pos
        })

    def _on_reset_window_size_button(self) -> None:
        """Reset window size to default."""
        CH.reset_setting(CKL.WINDOW_SIZE)
        width, height = map(int, (CH.get_variable_value(CKL.WINDOW_SIZE)).get().split("x"))
        self.window.set_window_size((width, height))

    def _on_reset_window_pos_button(self) -> None:
        """Reset window position to default."""
        CH.reset_setting(CKL.WINDOW_POSITION)
        pos_x, pos_y = map(int, (CH.get_variable_value(CKL.WINDOW_POSITION)).get().split("+"))
        self.window.set_window_position((pos_x, pos_y))

    def _on_use_high_dpi_scaling_checkbox(self) -> None:
        """Toggle high DPI scaling."""
        CH.set_variable_value(CKL.USE_HIGH_DPI_SCALING, ctk.BooleanVar(self.gui_instance, self.gui_instance.checkbox_use_high_dpi_scaling.get()))
        self.app_instance.window.set_high_dpi(CH.get_variable_value(CKL.USE_HIGH_DPI_SCALING).get())

    def _on_ui_theme_dropdown(self, selected_theme=None) -> None:
        """Set the UI theme."""
        theme_key = self.localization_manager.reverse_localize(selected_theme)
        CH.set_variable_value(CKL.UI_THEME, ctk.StringVar(self.gui_instance, theme_key[0].upper() + theme_key[1:]))
        self.app_instance.window.set_ui_theme(theme_key)

    def _on_ui_color_theme_dropdown(self, selected_color_theme=None) -> None:
        """Set the UI color theme."""
        color_theme_key = self.localization_manager.reverse_localize(selected_color_theme)
        CH.set_variable_value(CKL.UI_COLOR_THEME, ctk.StringVar(self.gui_instance, color_theme_key[0].upper() + color_theme_key[1:]))
        ui_color_theme = color_theme_key if color_theme_key in ["blue", "dark-blue", "green"] else FileOps.join_paths(CH.get_variable_value(CKL.RESOURCES_PATH), "themes", f"{color_theme_key}.json")
        self.app_instance.window.set_ui_color_theme(ui_color_theme)

    def _on_ui_language_dropdown(self, selected_language=None) -> None:
        """Set the UI language."""
        language_key = self.localization_manager.reverse_localize(selected_language)
        CH.set_variable_value(CKL.UI_LANGUAGE, ctk.StringVar(self.gui_instance, language_key[0].upper() + language_key[1:]))
        self.localization_manager.set_active_language(language_key)

    def _on_reset_ui_appearance_settings_button(self) -> None:
        """Reset UI appearance settings to default."""
        CH.reset_settings([
            CKL.USE_HIGH_DPI_SCALING,
            CKL.UI_THEME,
            CKL.UI_COLOR_THEME,
            CKL.UI_LANGUAGE
        ])
        self._update_checkboxes({
            CKL.USE_HIGH_DPI_SCALING: self.gui_instance.checkbox_use_high_dpi_scaling
        })
        self.window.set_ui_theme(CH.get_variable_value(CKL.UI_THEME).get().lower())
        self.window.set_ui_color_theme((CH.get_variable_value(CKL.UI_COLOR_THEME)).get().lower())
        self.localization_manager.set_active_language((CH.get_variable_value(CKL.UI_LANGUAGE)).get())

    def _on_whole_word_replacement_checkbox(self) -> None:
        """Toggle whole word replacement."""
        CH.set_variable_value(CKL.WHOLE_WORD_REPLACEMENT, ctk.BooleanVar(self.gui_instance, self.gui_instance.checkbox_whole_word_replacement.get()))

    def _on_reset_everything_button(self) -> None:
        """Reset all settings to default."""
        CH.reset_settings([
            CKL.WINDOW_SIZE,
            CKL.WINDOW_POSITION,
            CKL.CENTER_WINDOW_ON_STARTUP,
            CKL.SAVE_WINDOW_SIZE,
            CKL.SAVE_WINDOW_POS,
            CKL.USE_HIGH_DPI_SCALING,
            CKL.UI_THEME,
            CKL.UI_COLOR_THEME,
            CKL.UI_LANGUAGE,
            CKL.WHOLE_WORD_REPLACEMENT
        ])
        self._update_checkboxes({
            CKL.CENTER_WINDOW_ON_STARTUP: self.gui_instance.checkbox_center_window_on_startup,
            CKL.SAVE_WINDOW_SIZE: self.gui_instance.checkbox_save_window_size,
            CKL.SAVE_WINDOW_POS: self.gui_instance.checkbox_save_window_pos,
            CKL.USE_HIGH_DPI_SCALING: self.gui_instance.checkbox_use_high_dpi_scaling,
            CKL.WHOLE_WORD_REPLACEMENT: self.gui_instance.checkbox_whole_word_replacement
        })

        self.window.set_ui_theme((CH.get_variable_value(CKL.UI_THEME)).get().lower())
        self.window.set_ui_color_theme((CH.get_variable_value(CKL.UI_COLOR_THEME)).get().lower())
        self.localization_manager.set_active_language((CH.get_variable_value(CKL.UI_LANGUAGE)).get())

    def _on_language_updated(self) -> None:
        """Update the localization for the options frame."""
        self.gui_instance.btn_reset_everything.update_localization()

        self.gui_instance.lbl_window_settings.update_localization()
        self.gui_instance.checkbox_save_window_size.update_localization()
        self.gui_instance.checkbox_save_window_pos.update_localization()
        self.gui_instance.checkbox_center_window_on_startup.update_localization()
        self.gui_instance.btn_reset_window_size.update_localization()
        self.gui_instance.btn_reset_window_pos.update_localization()
        self.gui_instance.btn_reset_window_settings.update_localization()

        self.gui_instance.lbl_ui_appearance_settings.update_localization()
        self.gui_instance.checkbox_use_high_dpi_scaling.update_localization()
        self.gui_instance.lbl_ui_theme.update_localization()
        self.gui_instance.dropdown_ui_theme.update_localization()
        self.gui_instance.lbl_ui_color_theme.update_localization()
        self.gui_instance.dropdown_ui_color_theme.update_localization()
        self.gui_instance.lbl_ui_language.update_localization()
        self.gui_instance.dropdown_ui_language.update_localization()
        self.gui_instance.btn_reset_ui_appearance_settings.update_localization()

        self.gui_instance.lbl_translation_settings.update_localization()
        self.gui_instance.checkbox_whole_word_replacement.update_localization()

    # Helper methods
    def _translate_list(self, list_to_translate: list) -> list:
        """Translate a list of strings."""
        return [self.loc(item) for item in list_to_translate]

    def _update_checkboxes(self, checkbox_map: dict) -> None:
        """Update the checkboxes based on the current settings."""
        for setting in checkbox_map:
            checkbox = checkbox_map[setting]
            value = CH.get_variable_value(setting).get()
            if value:
                checkbox.select()
            else:
                checkbox.deselect()
