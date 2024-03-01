# options_frame.py ~ AutoDriveTranslationTool

import os
import customtkinter as ctk

import GuiFramework.utilities.utils as utils
import GuiFramework.utilities.gui_utils as gui_utils


class OptionsFrame(ctk.CTkFrame):
    GUI_COMPONENT_NAME = "options_frame"
    GUI_FILE_PATH = os.path.join("resources", "gui", f"{GUI_COMPONENT_NAME}.gui.json")

    # Settings keys
    SAVE_WINDOW_SIZE = "save_window_size"
    SAVE_WINDOW_POS = "save_window_pos"
    CENTER_WINDOW_ON_STARTUP = "center_window_on_startup"
    WINDOW_SIZE = "window_size"
    WINDOW_POSITION = "window_position"

    USE_HIGH_DPI_SCALING = "use_high_dpi_scaling"
    UI_THEME = "ui_theme"
    UI_COLOR_THEME = "ui_color_theme"
    UI_LANGUAGE = "ui_language"

    WHOLE_WORD_REPLACEMENT = "whole_word_replacement"

    DROPDOWN_UI_THEMES = "dropdown_ui_themes"
    DROPDOWN_UI_COLOR_THEMES = "dropdown_ui_color_themes"
    DROPDOWN_UI_LANGUAGES = "dropdown_ui_languages"

    def __init__(self, app_instance, tab_view):
        super().__init__(tab_view)
        self.app_instance = app_instance

        self._initialize_components()

        self._subscribe_to_managers()
        self._register_gui_components()

    def _initialize_components(self):
        """Initialize essential components"""
        self.window = self.app_instance.window
        self.gui_manager = self.app_instance.gui_manager
        self.localization_manager = self.app_instance.localization_manager
        self.config_manager = self.app_instance.config_manager
        self.dev_path = self.app_instance.config_setup.DEV_PATH

        self.add_var, self.set_var, self.get_var = self.config_manager.add_variable, self.config_manager.set_variable, self.config_manager.get_variable
        self.load_setting, self.reset_settings = self.config_manager.load_setting, self.config_manager.reset_settings
        self.loc = self.localization_manager.localize

        self.GUI_FILE_PATH = os.path.join(self.dev_path, self.GUI_FILE_PATH)

    def _subscribe_to_managers(self):
        """Subscribe to GUI and Localization managers."""
        self.localization_manager.subscribe(self, ["lang_update"])
        self.gui_manager.subscribe(self)

    def set_widget_references(self):
        """Set widget references for the frame."""
        gui_utils.set_widget_references(self, self.GUI_COMPONENT_NAME, self.gui_manager)
        self.on_language_updated(self.localization_manager.get_language(), "init")

    def on_language_updated(self, language_code, event_type):
        """Update the language of the widgets in the frame."""
        if event_type == "lang_update":
            gui_utils.update_language(self.gui_manager, self.loc, self.GUI_COMPONENT_NAME)
            self.dropdown_ui_theme.configure(
                variable=ctk.StringVar(self, self.loc(self.get_var(self.UI_THEME).get())),
                values=self._translate_list(self.get_var(self.DROPDOWN_UI_THEMES))
            )
            self.dropdown_ui_color_theme.configure(
                variable=ctk.StringVar(self, self.loc(self.get_var(self.UI_COLOR_THEME).get())),
                values=self._translate_list(self.get_var(self.DROPDOWN_UI_COLOR_THEMES))
            )
            self.dropdown_ui_language.configure(
                variable=ctk.StringVar(self, self.loc(self.get_var(self.UI_LANGUAGE).get())),
                values=self._translate_list(self.get_var(self.DROPDOWN_UI_LANGUAGES))
            )

    def _register_gui_components(self):
        """Register the GUI components."""
        self.gui_manager.register_gui_file(
            self.GUI_COMPONENT_NAME,
            self.GUI_FILE_PATH,
            self,
            self
        )

    # main frame callbacks
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
        self.reset_settings(settings_to_reset)
        gui_utils.update_checkbox_state(self.checkbox_save_window_size, self.SAVE_WINDOW_SIZE, self.config_manager)
        gui_utils.update_checkbox_state(self.checkbox_save_window_pos, self.SAVE_WINDOW_POS, self.config_manager)
        gui_utils.update_checkbox_state(self.checkbox_center_window_on_startup, self.CENTER_WINDOW_ON_STARTUP, self.config_manager)
        gui_utils.update_checkbox_state(self.checkbox_use_high_dpi_scaling, self.USE_HIGH_DPI_SCALING, self.config_manager)
        gui_utils.update_checkbox_state(self.checkbox_whole_word_replacement, self.WHOLE_WORD_REPLACEMENT, self.config_manager)
        self.window.set_ui_theme(self.get_var(self.UI_THEME).get().lower())
        self.window.set_ui_color_theme(self.get_var(self.UI_COLOR_THEME).get().lower())
        self.localization_manager.set_active_language(self.get_var(self.UI_LANGUAGE).get())

    # Window settings callbacks
    def _on_center_window_on_startup_checkbox(self):
        self.set_var(self.CENTER_WINDOW_ON_STARTUP, ctk.BooleanVar(self, self.checkbox_center_window_on_startup.get()))

    def _on_save_window_size_checkbox(self):
        self.set_var(self.SAVE_WINDOW_SIZE, ctk.BooleanVar(self, self.checkbox_save_window_size.get()))

    def _on_save_window_pos_checkbox(self):
        self.set_var(self.SAVE_WINDOW_POS, ctk.BooleanVar(self, self.checkbox_save_window_pos.get()))

    def _on_reset_window_settings_button(self):
        settings_to_reset = [
            ["WindowSettings", self.CENTER_WINDOW_ON_STARTUP],
            ["WindowSettings", self.SAVE_WINDOW_SIZE],
            ["WindowSettings", self.SAVE_WINDOW_POS],
        ]
        self.reset_settings(settings_to_reset)
        gui_utils.update_checkbox_state(self.checkbox_save_window_size, self.SAVE_WINDOW_SIZE, self.config_manager)
        gui_utils.update_checkbox_state(self.checkbox_save_window_pos, self.SAVE_WINDOW_POS, self.config_manager)
        gui_utils.update_checkbox_state(self.checkbox_center_window_on_startup, self.CENTER_WINDOW_ON_STARTUP, self.config_manager)

    def _on_reset_window_size_button(self):
        settings_to_reset = [
            ["WindowSettings", self.WINDOW_SIZE]
        ]
        self.reset_settings(settings_to_reset)
        width, height = map(int, self.load_setting("WindowSettings", self.WINDOW_SIZE).split("x"))
        self.window.set_window_size((width, height))

    def _on_reset_window_pos_button(self):
        settings_to_reset = [
            ["WindowSettings", self.WINDOW_POSITION]
        ]
        self.reset_settings(settings_to_reset)
        pos_x, pos_y = map(int, self.load_setting("WindowSettings", self.WINDOW_POSITION).split("+"))
        self.window.set_window_position((pos_x, pos_y))

    # UI appearance settings callbacks
    def _on_use_high_dpi_scaling_checkbox(self):
        self.set_var(self.USE_HIGH_DPI_SCALING, ctk.BooleanVar(self, self.checkbox_use_high_dpi_scaling.get()))
        self.window.set_high_dpi(self.get_var(self.USE_HIGH_DPI_SCALING).get())

    def _on_ui_theme_dropdown(self, selected_theme=None):
        theme_key = self.localization_manager.reverse_localize(selected_theme)
        self.set_var("ui_theme", ctk.StringVar(self, theme_key[0].upper() + theme_key[1:]))
        self.window.set_ui_theme(theme_key)

    def _on_ui_color_theme(self, selected_color_theme=None):
        color_theme_key = self.localization_manager.reverse_localize(selected_color_theme)
        self.set_var("ui_color_theme", ctk.StringVar(self, color_theme_key[0].upper() + color_theme_key[1:]))
        ui_color_theme = color_theme_key if color_theme_key in ["blue", "dark-blue", "green"] else os.path.join(self.dev_path, "resources", "themes", f"{color_theme_key}.json")
        self.window.set_ui_color_theme(ui_color_theme)

    def _on_ui_language_dropdown(self, selected_language=None):
        language_key = self.localization_manager.reverse_localize(selected_language)
        self.set_var("ui_language", ctk.StringVar(self, language_key[0].upper() + language_key[1:]))
        self.localization_manager.set_active_language(language_key)

    def _on_reset_ui_appearance_settings_button(self):
        settings_to_reset = [
            ["AppearanceSettings", self.USE_HIGH_DPI_SCALING],
            ["AppearanceSettings", self.UI_THEME],
            ["AppearanceSettings", self.UI_COLOR_THEME],
            ["AppearanceSettings", self.UI_LANGUAGE]
        ]
        self.reset_settings(settings_to_reset)
        gui_utils.update_checkbox_state(self.checkbox_use_high_dpi_scaling, self.USE_HIGH_DPI_SCALING, self.config_manager)
        self.window.set_ui_theme(self.get_var(self.UI_THEME).get().lower())
        self.window.set_ui_color_theme(self.get_var(self.UI_COLOR_THEME).get().lower())
        self.localization_manager.set_active_language(self.get_var(self.UI_LANGUAGE).get())

    # Translation settings callbacks
    def _on_whole_word_replacement_checkbox(self):
        self.set_var(self.WHOLE_WORD_REPLACEMENT, ctk.BooleanVar(self, self.checkbox_whole_word_replacement.get()))

    # Helper methods
    def _translate_list(self, list_to_translate):
        return [self.loc(item) for item in list_to_translate]
