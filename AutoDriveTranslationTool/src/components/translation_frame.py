# translation_frame.py ~ AutoDriveTranslationTool

import os
import customtkinter as ctk

from GuiFramework.utilities import update_widget_text
from GuiFramework.widgets import CustomPopupMessageBox

from src.functions import (
    TranslationFinder, Validator, Translator
)


class TranslationFrame(ctk.CTkFrame):
    def __init__(self, app_instance, tab_view):
        super().__init__(tab_view)

        self.app_instance = app_instance
        self.gui_manager = app_instance.gui_manager
        self.window_instance = self.app_instance.window
        self.localization_manager = self.app_instance.localization_manager

        self.dev_path = self.app_instance.dev_path
        self.GUI_FILE_PATH = os.path.join(self.dev_path, "resources", "gui", "translation_frame.gui.json")

        self.loc = self.localization_manager.translate

        self.config_manager = self.app_instance.config_manager
        self.add_var = self.config_manager.add_variable
        self.set_var = self.config_manager.set_variable
        self.get_var = self.config_manager.get_variable

        self.localization_manager.subscribe(self)
        self.gui_manager.subscribe(self)
        self._register_gui_components()

    def set_widget_references(self):
        self.widgets = self.gui_manager.widgets.get("translation_frame")
        for widget_name, widget_ref in self.widgets.items():
            setattr(self, widget_name, widget_ref)

    def update_language(self):
        widgets = self.gui_manager.widgets.get("translation_frame")
        for name_id, widget_ref in widgets.items():
            update_widget_text(widget_ref, self.loc(name_id))

    def _register_gui_components(self):
        self.gui_manager.register_gui_file(
            "translation_frame",
            self.GUI_FILE_PATH,
            self,
            self
        )

    def _on_select_all(self):
        self.scroll_list_language_selection.set_all_entries_state(True)

    def _on_deselect_all(self):
        self.scroll_list_language_selection.set_all_entries_state(False)

    def _on_translate(self):
        def on_yes(is_yes):
            if is_yes:
                Translator(
                    input_path=os.path.join(self.dev_path, self.get_var("input_path")),
                    output_path=os.path.join(self.dev_path, self.get_var("output_path")),
                    dictionaries_path=os.path.join(self.dev_path, self.get_var("dictionaries_path")),
                    languages=self.scroll_list_language_selection.get_checked_entries(),
                    output_widget=self.widgets.get("textbox_output_console"),
                    logger=self.app_instance.logger,
                    console=False,
                    whole_word=self.get_var("whole_word_replacement"),
                )
        CustomPopupMessageBox(
            self,
            title=self.loc("Translation Process"),
            message=self.loc("The translation process will take a while. Please be patient."),
            interactive=True,
            yes_button_text=self.loc("Start Translation"),
            no_button_text=self.loc("Cancel"),
            on_yes=on_yes
        )

    def _on_validate_output_files(self):
        Validator(
            input_path=os.path.join(self.dev_path, self.get_var("output_path")),
            languages=self.scroll_list_language_selection.get_checked_entries(),
            output_widget=self.widgets.get("textbox_output_console"),
            logger=self.app_instance.logger,
            console=False,
        )

    def _on_find_missing_translations(self):
        checked_entries = self.scroll_list_language_selection.get_checked_entries()
        if not checked_entries:
            return
        TranslationFinder(
            input_path=os.path.join(self.dev_path, self.get_var("input_path")),
            output_path=os.path.join(self.dev_path, "missing_translations.txt"),
            dictionary_path=os.path.join(self.dev_path, self.get_var("dictionaries_path")),
            languages=checked_entries,
            output_widget=self.widgets.get("textbox_output_console"),
            logger=self.app_instance.logger,
            console=False,
        )

    def _on_clear_console(self):
        self.widgets.get("textbox_output_console").clear_console()
