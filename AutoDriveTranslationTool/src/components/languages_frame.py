# languages_frame.py ~ AutoDriveTranslationTool

import customtkinter as ctk

from GuiFramework.widgets import CustomPopupMessageBox

from GuiFramework.utilities import FileOps
from GuiFramework.utilities.gui_utils import GuiUtils

from GuiFramework.utilities.config import ConfigHandler as CH
from GuiFramework.utilities.config.config_types import ConfigKeyList as CKL


class LanguagesFrame(ctk.CTkFrame):
    GUI_COMPONENT_NAME = "languages_frame"
    GUI_FILE_PATH = FileOps.join_paths("gui", f"{GUI_COMPONENT_NAME}.gui.json")

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

        self.loc = self.localization_manager.localize

        self.GUI_FILE_PATH = FileOps.join_paths(CH.get_variable_value(CKL.RESOURCES_PATH), self.GUI_FILE_PATH)

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
        GuiUtils.on_gui_build(self, self.GUI_COMPONENT_NAME, self.gui_manager)
        self.dropdown_language_select = self.gui_manager.widgets.get("dictionary_frame").get("dropdown_language_select")
        self.scroll_list_language_selection = self.gui_manager.widgets.get("translation_frame").get("scroll_list_language_selection")
        self.on_language_updated(self.localization_manager.get_language(), "init")

    def on_language_updated(self, language_code, event_type):
        """Update the language of the widgets in the frame."""
        if event_type == "lang_update" or event_type == "init":
            GuiUtils.update_language(self.gui_manager, self.loc, self.GUI_COMPONENT_NAME)

    # Widget Event Handlers
    def _on_add_language(self):
        """Add a new language to the list of supported languages."""
        new_language = self.entry_new_language.get()
        if not new_language:
            return
        invalid_chars = [char for char in new_language if not char.isalnum() and char not in 'äöüÄÖÜß_-']
        if invalid_chars:
            invalid_chars_str = ', '.join(set(invalid_chars))
            popup_message = self.loc("invalid_characters") + invalid_chars_str
            CustomPopupMessageBox(self, title=self.loc("invalid_language_title"), message=popup_message)
        else:
            self.scroll_list_languages.add_entry(new_language)
            self.scroll_list_languages.sort_entries()
            self.entry_new_language.delete(0, ctk.END)

    def _on_remove_language(self):
        """Remove the selected languages from the list of supported languages."""
        def callback_handler(is_confirmed):
            if is_confirmed:
                self.scroll_list_languages.remove_checked_entries()
        self._create_PopupMessageBox(
            self.loc("confirm_remove_lang_msg_title"),
            self.loc("confirm_remove_lang_msg"),
            callback_handler
        )

    def _on_save_custom(self):
        """Save the custom list of supported languages."""
        def callback_handler(is_confirmed):
            if is_confirmed:
                supported_languages = self.scroll_list_languages.get_all_entries()
                CH.set_variable_value(CKL.SUPPORTED_LANGUAGES, supported_languages)
                self.dropdown_language_select.configure(values=supported_languages)
                self.scroll_list_language_selection.remove_all_entries()
                self.scroll_list_language_selection.add_entries(supported_languages)
                self.entry_new_language.delete(0, ctk.END)
                self.scroll_list_languages.sort_entries()
        self._create_PopupMessageBox(
            self.loc("confirm_save_custom_lang_msg_title"),
            self.loc("confirm_save_custom_lang_msg"),
            callback_handler
        )

    def _on_load_custom(self):
        """Load the custom list of supported languages."""
        def callback_handler(is_confirmed):
            if is_confirmed:
                supported_languages = CH.get_setting(CKL.SUPPORTED_LANGUAGES, fallback_value=["English"]).split(",")
                self.scroll_list_languages.remove_all_entries()
                self.scroll_list_languages.add_entries(supported_languages)
                self.scroll_list_languages.sort_entries()
        self._create_PopupMessageBox(
            self.loc("confirm_load_custom_lang_msg_title"),
            self.loc("confirm_load_custom_lang_msg"),
            callback_handler
        )

    def _on_load_default(self):
        """Load the default list of supported languages."""
        def callback_handler(is_confirmed):
            if is_confirmed:
                supported_languages = CH.get_setting(CKL.SUPPORTED_LANGUAGES, fallback_value=["English"], force_default=True).split(",")
                self.scroll_list_languages.remove_all_entries()
                self.scroll_list_languages.add_entries(supported_languages)
                self.scroll_list_languages.sort_entries()
        self._create_PopupMessageBox(
            self.loc("confirm_load_default_lang_msg_title"),
            self.loc("confirm_load_default_lang_msg"),
            callback_handler
        )

    # Helper Methods
    def _create_PopupMessageBox(self, title, message, on_callback):
        """Create a popup message box with yes/no buttons."""
        buttons = [
            {"text": self.loc("yes"), "callback": lambda: on_callback(True)},
            {"text": self.loc("no"), "callback": lambda: on_callback(False)}
        ]
        return CustomPopupMessageBox(
            self,
            title=title,
            message=message,
            buttons=buttons
        )