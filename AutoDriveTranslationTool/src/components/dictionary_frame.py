# dictionary_frame.py ~ AutoDriveTranslationTool

import os
import customtkinter as ctk
import GuiFramework.utilities.gui_utils as gui_utils

from GuiFramework.utilities import file_ops
from GuiFramework.widgets import CustomPopupMessageBox


class DictionaryFrame(ctk.CTkFrame):
    GUI_COMPONENT_NAME = "dictionary_frame"
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
        self.gui_manager.register_gui_file(
            self.GUI_COMPONENT_NAME,
            self.GUI_FILE_PATH,
            self,
            self
        )

    # Manager Event Handlers
    def on_gui_build(self):
        """Set widget references for the frame and initialize gui components."""
        gui_utils.on_gui_build(self, self.GUI_COMPONENT_NAME, self.gui_manager)
        self.scroll_list_dictionaries.add_entries(file_ops.get_all_file_names_in_directory(os.path.join(self.dev_path, self.get_var('dictionaries_path'))))
        self.on_language_updated(self.localization_manager.get_language(), "init")

    def on_language_updated(self, language_code, event_type):
        if event_type == "lang_update" or event_type == "init":
            gui_utils.update_language(self.gui_manager, self.loc, self.GUI_COMPONENT_NAME)

    # Widget Event Handlers
    def _on_save_dictionary_file(self):
        """Save the text in the dictionary edit box to a file."""
        checked_entries = self.scroll_list_dictionaries.get_checked_entries()
        if checked_entries:
            file_path = os.path.join(self.dev_path, self.get_var('dictionaries_path'), checked_entries[0])
            self._create_popup_message_box(self.loc("confirm_save_dic_title"), self.loc("confirm_save_dic_msg"),
                                           lambda is_confirmed: file_ops.save_textbox_to_file(self.custom_textbox_dictionary_edit_box, file_path) if is_confirmed else None)

    def _on_load_dictionary_file(self):
        """Load the text from a dictionary file to the dictionary edit box."""
        checked_entries = self.scroll_list_dictionaries.get_checked_entries()
        if checked_entries:
            file_path = os.path.join(self.dev_path, self.get_var('dictionaries_path'), checked_entries[0])
            if self.custom_textbox_dictionary_edit_box.is_empty():
                file_ops.load_file_to_textbox(self.custom_textbox_dictionary_edit_box, file_path)
            else:
                self._create_PopupMessageBox(self.loc("confirm_load_dic_title"), self.loc("confirm_load_dic_msg"), 
                                             lambda is_confirmed: file_ops.load_file_to_textbox(self.custom_textbox_dictionary_edit_box, file_path) if is_confirmed else None)

    def _on_clear_dictionary_edit_textbox(self):
        """Clear the text in the dictionary edit box."""
        def callback_handler(is_confirmed):
            if is_confirmed:
                self.custom_textbox_dictionary_edit_box.clear_text()
        self._create_PopupMessageBox(
            self.loc("confirm_clear_editbox_title"),
            self.loc("confirm_clear_editbox_msg"),
            callback_handler
        )

    def _on_create_dictionary_file(self):
        """Create a new dictionary file."""
        selected_language = self.dropdown_language_select.get()
        if selected_language != self.loc("select_language"):
            file_name = f"Dictionary_{selected_language}.dic"
            if file_name not in self.scroll_list_dictionaries.get_all_entries():
                file_path = os.path.join(self.dev_path, self.get_var('dictionaries_path'), file_name)
                file_ops.create_file(file_path)
                self.scroll_list_dictionaries.add_entry(file_name)

    def _on_delete_dictionary_file(self):
        """Delete the selected dictionary file."""
        def callback_handler(is_confirmed):
            if is_confirmed:
                file_path = os.path.join(self.dev_path, self.get_var('dictionaries_path'), self.scroll_list_dictionaries.get_checked_entries()[0])
                file_ops.delete_file(file_path)
                self.scroll_list_dictionaries.remove_checked_entries()
        checked_entries = self.scroll_list_dictionaries.get_checked_entries()
        if checked_entries:
            self._create_popup_message_box(
                self.loc("confirm_delete_dic_title"),
                self.loc("confirm_delete_dic_msg"),
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