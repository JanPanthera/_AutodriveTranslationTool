# languages_frame.py ~ AutoDriveTranslationTool

import re
import os
import customtkinter as ctk

from GuiFramework.src.utilities import update_widget_text
from GuiFramework.src.widgets import CustomPopupMessageBox


class LanguagesFrame(ctk.CTkFrame):
    def __init__(self, app_instance, tab_view):
        super().__init__(tab_view)

        self.app_instance = app_instance
        self.gui_manager = app_instance.gui_manager
        self.window_instance = self.app_instance.window
        self.localization_manager = self.app_instance.localization_manager

        self.dev_path = self.app_instance.dev_path
        self.GUI_FILE_PATH = os.path.join(self.dev_path, "resources", "gui", "languages_frame.gui.json")

        self.loc = self.localization_manager.translate

        self.config_manager = self.app_instance.config_manager
        self.set_var = self.config_manager.set_variable
        self.get_var = self.config_manager.get_variable
        self.load_setting = self.config_manager.load_setting

        self.localization_manager.subscribe(self)
        self.gui_manager.subscribe(self)
        self._register_gui_components()

    def set_widget_references(self):
        self.widgets = self.gui_manager.widgets.get("languages_frame")
        for widget_name, widget_ref in self.widgets.items():
            setattr(self, widget_name, widget_ref)
        self.dropdown_language_select = self.gui_manager.widgets.get("dictionary_frame").get("dropdown_language_select")
        self.scroll_list_language_selection = self.gui_manager.widgets.get("translation_frame").get("scroll_list_language_selection")
        self.scroll_list_languages = self.widgets.get("scroll_list_languages")

    def update_language(self):
        widgets = self.gui_manager.widgets.get("languages_frame")
        for name_id, widget_ref in widgets.items():
            update_widget_text(widget_ref, self.loc(name_id))

    def _register_gui_components(self):
        self.gui_manager.register(
            "languages_frame",
            self.GUI_FILE_PATH,
            self,  # master frame
            self,  # self
        )

    def _on_add_language(self):
        new_language = self.entry_new_language.get()
        pattern = r'[^a-zA-Z0-9äöüÄÖÜß_\-]'
        invalid_chars = re.findall(pattern, new_language)
        if invalid_chars:
            invalid_chars_str = ', '.join(set(invalid_chars))
            popup_message = self.loc("Invalid characters: ")
            popup_message += f"{invalid_chars_str}"
            CustomPopupMessageBox(
                self,
                title=self.loc("Invalid Input"),
                message=popup_message,
            )
        else:
            self.scroll_list_languages.add_entry(new_language)
            self.scroll_list_languages.sort_entries()
            self.entry_new_language.delete(0, ctk.END)

    def _on_remove_language(self):
        self.scroll_list_languages.remove_checked_entries()

    def _on_save_custom(self):
        def on_yes(is_yes):
            if is_yes:
                supported_languages = self.scroll_list_languages.get_all_entries()
                self.set_var("supported_languages", supported_languages)
                self.dropdown_language_select.configure(values=supported_languages)
                self.scroll_list_language_selection.remove_all_entries()
                self.scroll_list_language_selection.add_entries(supported_languages)
                self.entry_new_language.delete(0, ctk.END)
                self.scroll_list_languages.sort_entries()
        CustomPopupMessageBox(
            self,
            title=self.loc("Save Custom"),
            message=self.loc("Are you sure you want to save the languages to the custom configuration file?"),
            interactive=True,
            yes_button_text=self.loc("Yes"),
            no_button_text=self.loc("No"),
            on_yes=on_yes
        )

    def _on_load_custom(self):
        def on_yes(is_yes):
            if is_yes:
                supported_languages = self.load_setting("TranslationSettings", "supported_languages", default_value=["English"]).split(",")
                self.scroll_list_languages.remove_all_entries()
                self.scroll_list_languages.add_entries(supported_languages)
                self.scroll_list_languages.sort_entries()
        CustomPopupMessageBox(
            self,
            title=self.loc("Load Custom"),
            message=self.loc("Are you sure you want to load the languages from the custom configuration file?"),
            interactive=True,
            yes_button_text=self.loc("Yes"),
            no_button_text=self.loc("No"),
            on_yes=on_yes
        )

    def _on_load_default(self):
        def on_yes(is_yes):
            if is_yes:
                supported_languages = self.load_setting("TranslationSettings", "supported_languages", default_value=["English"], force_default=True).split(",")
                self.scroll_list_languages.remove_all_entries()
                self.scroll_list_languages.add_entries(supported_languages)
                self.scroll_list_languages.sort_entries()
        CustomPopupMessageBox(
            self,
            title=self.loc("Load Default"),
            message=self.loc("Are you sure you want to load the languages from the default configuration file?"),
            interactive=True,
            yes_button_text=self.loc("Yes"),
            no_button_text=self.loc("No"),
            on_yes=on_yes
        )
