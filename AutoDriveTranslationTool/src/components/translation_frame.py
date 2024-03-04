# translation_frame.py ~ AutoDriveTranslationTool

import os
import customtkinter as ctk
import GuiFramework.utilities.gui_utils as gui_utils

from GuiFramework.widgets import CustomPopupMessageBox

from src.functions import (
    TranslationFinder, Validator, Translator
)


class TranslationFrame(ctk.CTkFrame):
    GUI_COMPONENT_NAME = "translation_frame"
    GUI_FILE_PATH = os.path.join("resources", "gui", f"{GUI_COMPONENT_NAME}.gui.json")

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

    def _register_gui_components(self):
        """Register the GUI components."""
        self.gui_manager.register_gui_file(
            self.GUI_COMPONENT_NAME,
            self.GUI_FILE_PATH,
            self,
            self
        )

    # Manager Event Handlers
    def on_gui_build(self):
        """Set widget references for the frame."""
        gui_utils.on_gui_build(self, self.GUI_COMPONENT_NAME, self.gui_manager)
        self.on_language_updated(self.localization_manager.get_language(), "init")

    def on_language_updated(self, language_code, event_type):
        """Update the language of the widgets in the frame."""
        if event_type == "lang_update" or event_type == "init":
            gui_utils.update_language(self.gui_manager, self.loc, self.GUI_COMPONENT_NAME)

    # Widget Event Handlers
    def _on_select_all(self):
        """Select all languages."""
        self.scroll_list_language_selection.set_all_entries_state(True)

    def _on_deselect_all(self):
        """Deselect all languages."""
        self.scroll_list_language_selection.set_all_entries_state(False)

    def _on_translate(self):
        """Start the translation process."""
        def callback_handler(is_confirmed):
            if is_confirmed:
                Translator(
                    input_path=os.path.join(self.dev_path, self.get_var("input_path")),
                    output_path=os.path.join(self.dev_path, self.get_var("output_path")),
                    dictionaries_path=os.path.join(self.dev_path, self.get_var("dictionaries_path")),
                    languages=self.scroll_list_language_selection.get_checked_entries(),
                    output_widget=self.textbox_output_console,
                    logger=self.app_instance.logger,
                    localization_manager=self.localization_manager,
                    console=False,
                    whole_word=self.get_var("whole_word_replacement"),
                )
        CustomPopupMessageBox(
            self,
            title=self.loc("translation_process"),
            message=self.loc("waiting_for_translation"),
            buttons=[
                {"text": self.loc("start_translation"), "callback": lambda: callback_handler(True)},
                {"text": self.loc("cancel"), "callback": lambda: callback_handler(False)}
            ]
        )

    def _on_validate_output_files(self):
        """Validate the output files."""
        Validator(
            input_path=os.path.join(self.dev_path, self.get_var("output_path")),
            languages=self.scroll_list_language_selection.get_checked_entries(),
            output_widget=self.textbox_output_console,
            localization_manager=self.localization_manager,
            logger=self.app_instance.logger,
            console=False,
        )

    def _on_find_missing_translations(self):
        """Find missing translations."""
        checked_entries = self.scroll_list_language_selection.get_checked_entries()
        if not checked_entries:
            return
        TranslationFinder(
            input_path=os.path.join(self.dev_path, self.get_var("input_path")),
            output_path=os.path.join(self.dev_path, "missing_translations.txt"),
            dictionary_path=os.path.join(self.dev_path, self.get_var("dictionaries_path")),
            languages=checked_entries,
            output_widget=self.textbox_output_console,
            logger=self.app_instance.logger,
            localization_manager=self.localization_manager,
            console=False,
        )

    def _on_clear_console(self):
        """Clear the console."""
        self.textbox_output_console.clear_console()
