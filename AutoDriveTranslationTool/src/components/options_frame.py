# options_frame.py ~ AutoDriveTranslationTool

import os
import customtkinter as ctk

from GuiFramework.utilities import update_widget_text


class OptionsFrame(ctk.CTkFrame):

    def __init__(self, app_instance, tab_view):
        super().__init__(tab_view)

        self.app_instance = app_instance
        self.gui_manager = app_instance.gui_manager
        self.window = self.app_instance.window
        self.localization_manager = self.app_instance.localization_manager

        self.dev_path = self.app_instance.dev_path
        self.GUI_FILE_PATH = os.path.join(self.dev_path, "resources", "gui", "options_frame.gui.json")

        self.loc = self.localization_manager.translate

        self.config_manager = self.app_instance.config_manager
        self.add_var = self.config_manager.add_variable
        self.set_var = self.config_manager.set_variable
        self.get_var = self.config_manager.get_variable
        self.load_setting = self.config_manager.load_setting
        self.reset_settings = self.config_manager.reset_settings

        self.localization_manager.subscribe(self)
        self.gui_manager.subscribe(self)
        self._create_func_vars()
        self._register_gui_components()

    def _create_func_vars(self):
        self.add_var(name="_on_reset_everything_button", value=self._on_reset_everything_button)
        self.add_var(name="_on_save_window_size_checkbox", value=self._on_save_window_size_checkbox)
        self.add_var(name="_on_save_window_pos_checkbox", value=self._on_save_window_pos_checkbox)
        self.add_var(name="_on_save_selected_languages_checkbox", value=self._on_save_selected_languages_checkbox)
        self.add_var(name="_on_reset_save_on_window_close_settings_button", value=self._on_reset_save_on_window_close_settings_button)
        self.add_var(name="_on_use_high_dpi_scaling_checkbox", value=self._on_use_high_dpi_scaling_checkbox)
        self.add_var(name="_on_ui_theme_dropdown", value=self._on_ui_theme_dropdown)
        self.add_var(name="_on_ui_color_theme", value=self._on_ui_color_theme)
        self.add_var(name="_on_ui_language_dropdown", value=self._on_ui_language_dropdown)
        self.add_var(name="_on_reset_ui_appearance_settings_button", value=self._on_reset_ui_appearance_settings_button)
        self.add_var(name="_on_reset_window_size_button", value=self._on_reset_window_size_button)
        self.add_var(name="_on_reset_window_pos_button", value=self._on_reset_window_pos_button)
        self.add_var(name="_on_whole_word_replacement_checkbox", value=self._on_whole_word_replacement_checkbox)

    def set_widget_references(self):
        widgets = self.gui_manager.widgets.get("options_frame")
        for widget_name, widget_ref in widgets.items():
            setattr(self, widget_name, widget_ref)

    def update_language(self):
        widgets = self.gui_manager.widgets.get("options_frame")
        for name_id, widget_ref in widgets.items():
            update_widget_text(widget_ref, self.loc(name_id))

        # ensure that we use the key for translation
        self.dropdown_ui_theme.configure(
            variable=ctk.StringVar(self, self.loc(self.localization_manager.get_key(self.get_var("ui_theme").get()))),
            values=self._translate_list(self.get_var("dropdown_ui_themes"))
        )
        self.dropdown_ui_color_theme.configure(
            variable=ctk.StringVar(self, self.loc(self.localization_manager.get_key(self.get_var("ui_color_theme").get()))),
            values=self._translate_list(self.get_var("dropdown_ui_color_themes"))
        )
        self.dropdown_ui_language.configure(
            variable=ctk.StringVar(self, self.loc(self.localization_manager.get_key(self.get_var("ui_language").get()))),
            values=self._translate_list(self.get_var("dropdown_ui_languages"))
        )

    def _register_gui_components(self):
        self.gui_manager.register_gui_file(
            "options_frame",
            self.GUI_FILE_PATH,
            self
        )

    def _on_reset_everything_button(self):
        settings_to_reset = [
            ["AppSettings", "ui_theme"],
            ["AppSettings", "ui_language"],
            ["WindowSettings", "window_size"],
            ["WindowSettings", "window_position"],
            ["WindowSettings", "use_high_dpi_scaling"],
            ["SaveOnWindowClose", "save_window_size"],
            ["SaveOnWindowClose", "save_window_pos"],
            ["SaveOnWindowClose", "save_selected_languages"],
            ["TranslationSettings", "whole_word_replacement"]
        ]
        self.reset_settings(settings_to_reset)
        self._update_checkboxes_and_window()

    def _on_save_window_size_checkbox(self):
        self.set_var("save_window_size", ctk.BooleanVar(self, self.checkbox_save_window_size.get()))

    def _on_save_window_pos_checkbox(self):
        self.set_var("save_window_pos", ctk.BooleanVar(self, self.checkbox_save_window_pos.get()))

    def _on_save_selected_languages_checkbox(self):
        self.set_var("save_selected_languages", ctk.BooleanVar(self, self.checkbox_save_selected_languages.get()))

    def _on_reset_save_on_window_close_settings_button(self):
        settings_to_reset = [
            ["SaveOnWindowClose", "save_window_size"],
            ["SaveOnWindowClose", "save_window_pos"],
            ["SaveOnWindowClose", "save_selected_languages"]
        ]
        self.reset_settings(settings_to_reset)
        self._update_checkboxes()

    def _on_use_high_dpi_scaling_checkbox(self):
        self.set_var("use_high_dpi_scaling", ctk.BooleanVar(self, self.checkbox_use_high_dpi_scaling.get()))
        self.window.set_high_dpi(self.get_var("use_high_dpi_scaling").get())

    def _on_ui_theme_dropdown(self, selected_theme=None):
        if selected_theme is None:
            self.logger.error("dropdown_ui_theme: on_ui_theme_dropdown_select called with selected_theme=None")
            return
        theme_key = self.localization_manager.get_key(selected_theme)

        self.set_var("ui_theme", ctk.StringVar(self, theme_key[0].upper() + theme_key[1:]))
        self.window.set_ui_theme(theme_key)

    def _on_ui_color_theme(self, selected_color_theme=None):
        if selected_color_theme is None:
            self.logger.error("dropdown_ui_color_theme: on_ui_color_theme_command called with selected_color_theme=None")
            return
        color_theme_key = self.localization_manager.get_key(selected_color_theme)
        self.set_var("ui_color_theme", ctk.StringVar(self, color_theme_key[0].upper() + color_theme_key[1:]))
        ui_color_theme = color_theme_key if color_theme_key in ["blue", "dark-blue", "green"] else os.path.join(self.dev_path, "resources", "themes", f"{color_theme_key}.json")
        self.window.set_ui_color_theme(ui_color_theme)

    def _on_ui_language_dropdown(self, selected_language=None):
        if selected_language is None:
            self.logger.error("dropdown_ui_language: on_ui_language_dropdown_select called with selected_language=None")
            return
        language_key = self.localization_manager.get_key(selected_language)
        self.set_var("ui_language", ctk.StringVar(self, language_key[0].upper() + language_key[1:]))
        self.localization_manager.set_language(language_key)

    def _on_reset_ui_appearance_settings_button(self):
        settings_to_reset = [
            ["AppSettings", "ui_theme"],
            ["AppSettings", "ui_language"],
            ["WindowSettings", "use_high_dpi_scaling"]
        ]
        self.reset_settings(settings_to_reset)
        self._update_checkboxes_and_window()

    def _on_reset_window_size_button(self):
        settings_to_reset = [
            ["WindowSettings", "window_size"]
        ]
        self.reset_settings(settings_to_reset)
        width, height = map(int, self.load_setting("WindowSettings", "window_size").split("x"))
        self.window.set_window_size((width, height))

    def _on_reset_window_pos_button(self):
        settings_to_reset = [
            ["WindowSettings", "save_window_pos"]
        ]
        self.reset_settings(settings_to_reset)
        pos_x, pos_y = map(int, self.load_setting("WindowSettings", "window_position").split("+"))
        self.window.set_window_position((pos_x, pos_y))

    def _on_whole_word_replacement_checkbox(self):
        self.set_var("whole_word_replacement", ctk.BooleanVar(self, self.checkbox_whole_word_replacement.get()))

    def _update_checkboxes(self):
        self._select_checkbox_if_true(self.checkbox_save_window_size, self.get_var("save_window_size"))
        self._select_checkbox_if_true(self.checkbox_save_window_pos, self.get_var("save_window_pos"))
        self._select_checkbox_if_true(self.checkbox_save_selected_languages, self.get_var("save_selected_languages"))

    def _update_checkboxes_and_window(self):
        self._select_checkbox_if_true(self.checkbox_save_window_size, self.get_var("save_window_size"))
        self._select_checkbox_if_true(self.checkbox_save_window_pos, self.get_var("save_window_pos"))
        self._select_checkbox_if_true(self.checkbox_save_selected_languages, self.get_var("save_selected_languages"))
        self._select_checkbox_if_true(self.checkbox_use_high_dpi_scaling, self.get_var("use_high_dpi_scaling"))
        self._select_checkbox_if_true(self.checkbox_whole_word_replacement, self.get_var("whole_word_replacement"))
        self.window.set_ui_theme(self.get_var("ui_theme").get())
        self.window.set_high_dpi(self.get_var("use_high_dpi_scaling").get())
        width, height = map(int, self.load_setting("WindowSettings", "window_size").split("x"))
        pos_x, pos_y = map(int, self.load_setting("WindowSettings", "window_position").split("+"))
        self.window.set_window_geometry((width, height), (pos_x, pos_y))
        self.localization_manager.set_language(self.get_var("ui_language").get())

    def _translate_list(self, list_to_translate):
        return [self.loc(self.localization_manager.get_key(item)) for item in list_to_translate]

    def _select_checkbox_if_true(self, checkbox, variable):
        if variable.get():
            checkbox.select()
        else:
            checkbox.deselect()
