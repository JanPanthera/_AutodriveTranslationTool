# AutoDriveTranslationTool/src/components/languages_frame/languages_frame_logic.py

import customtkinter as ctk

from GuiFramework.widgets import CustomPopupMessageBox

from GuiFramework.utilities import EventManager
from GuiFramework.utilities.config import ConfigHandler as CH
from GuiFramework.utilities.config.config_types import ConfigKeyList as CKL

from AutoDriveTranslationTool.src.core.constants import (
    EVENT_ON_ADD_LANGUAGE, EVENT_ON_REMOVE_LANGUAGE,
    EVENT_ON_SAVE_CUSTOM, EVENT_ON_LOAD_CUSTOM, EVENT_ON_LOAD_DEFAULT
)


class LanguagesFrameLogic:
    """Initialize the languages frame logic components."""

    def __init__(self, app_instance, gui_instance) -> None:
        """Initialize languages frame logic components."""
        self.app_instance = app_instance
        self.gui_instance = gui_instance

        self.localization_manager = self.app_instance.localization_manager
        self.loc = self.localization_manager.localize

        self._setup_event_handlers()

    def _setup_event_handlers(self) -> None:
        """Register event handlers for language actions."""
        EventManager.subscribe(EVENT_ON_ADD_LANGUAGE, self._on_add_language)
        EventManager.subscribe(EVENT_ON_REMOVE_LANGUAGE, self._on_remove_language)
        EventManager.subscribe(EVENT_ON_SAVE_CUSTOM, self._on_save_custom)
        EventManager.subscribe(EVENT_ON_LOAD_CUSTOM, self._on_load_custom)
        EventManager.subscribe(EVENT_ON_LOAD_DEFAULT, self._on_load_default)

    def _on_add_language(self):
        """Add a new language to the supported languages list."""
        new_language = self.gui_instance.entry_new_language.get()
        if not new_language:
            return
        invalid_chars = [char for char in new_language if not char.isalnum() and char not in 'äöüÄÖÜß_-']
        if invalid_chars:
            invalid_chars_str = ', '.join(set(invalid_chars))
            popup_message = self.loc("invalid_characters") + invalid_chars_str
            CustomPopupMessageBox(self, title=self.loc("invalid_language_title"), message=popup_message)
        else:
            self.gui_instance.scroll_list_languages.add_entry(new_language)
            self.gui_instance.scroll_list_languages.sort_entries()
            self.gui_instance.entry_new_language.delete(0, ctk.END)

    def _on_remove_language(self):
        """Remove selected languages from the supported languages list."""
        def callback_handler(is_confirmed):
            if is_confirmed:
                self.gui_instance.scroll_list_languages.remove_checked_entries()
        self._create_PopupMessageBox(
            self.loc("confirm_remove_lang_msg_title"),
            self.loc("confirm_remove_lang_msg"),
            callback_handler
        )

    def _on_save_custom(self):
        """Save the custom list of supported languages."""
        def callback_handler(is_confirmed):
            if is_confirmed:
                scroll_list_languages = self.gui_instance.scroll_list_languages
                supported_languages = scroll_list_languages.get_all_entries()
                CH.set_variable_value(CKL.SUPPORTED_LANGUAGES, supported_languages)
                self.dictionary_frame.dropdown_language_select.configure(values=supported_languages)
                scroll_list_languages.remove_all_entries()
                scroll_list_languages.add_entries(supported_languages)
                self.gui_instance.entry_new_language.delete(0, ctk.END)
                scroll_list_languages.sort_entries()
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