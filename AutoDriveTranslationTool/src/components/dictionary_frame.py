# dictionary_frame.py ~ AutoDriveTranslationTool

import customtkinter as ctk
import GuiFramework.utilities.gui_utils as gui_utils

from GuiFramework.utilities import FileOps
from GuiFramework.utilities import CtkHelper
from GuiFramework.widgets import CustomPopupMessageBox

from GuiFramework.utilities.config import ConfigHandler as CH
from GuiFramework.utilities.config.config_types import ConfigKeyList as CKL

from AutoDriveTranslationTool.src.functions import DictionaryCreator
from AutoDriveTranslationTool.src.functions.exceptions import InvalidFileNameError


class DictionaryFrame(ctk.CTkFrame):
    GUI_COMPONENT_NAME = "dictionary_frame"
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
        self.file_tree_view.create_tree(CH.get_variable_value(CKL.DICTIONARIES_PATH), expand_root_node=True)
        self.on_language_updated(self.localization_manager.get_language(), "init")

    def on_language_updated(self, language_code, event_type):
        if event_type in {"lang_update", "init"}:
            gui_utils.update_language(self.gui_manager, self.loc, self.GUI_COMPONENT_NAME)

    # Widget Event Handlers
    def _on_save_dictionary_file(self):
        """Save the text in the dictionary edit box to a file."""
        selected_file = self.file_tree_view.get_selected_files()
        if selected_file:
            file_path = next(iter(selected_file.values()))
            self._create_popup_message_box(
                self.loc("confirm_save_dic_title"), self.loc("confirm_save_dic_msg"),
                lambda is_confirmed: CtkHelper.save_textbox_to_file(self.custom_textbox_dictionary_edit_box, file_path) if is_confirmed else None
            )

    def _on_load_dictionary_file(self):
        """Load the text from a dictionary file to the dictionary edit box."""
        selected_file = self.file_tree_view.get_selected_files()
        if selected_file:
            file_path = next(iter(selected_file.values()))
            if self.custom_textbox_dictionary_edit_box.is_empty() or self._confirm_action(self.loc("confirm_load_dic_title"), self.loc("confirm_load_dic_msg")):
                CtkHelper.load_file_to_textbox(self.custom_textbox_dictionary_edit_box, file_path, overwrite=True)

    def _on_clear_dictionary_edit_textbox(self):
        """Clear the text in the dictionary edit box."""
        if not self.custom_textbox_dictionary_edit_box.is_empty() and self._confirm_action(self.loc("confirm_clear_editbox_title"), self.loc("confirm_clear_editbox_msg")):
            self.custom_textbox_dictionary_edit_box.clear_text()

    def _on_create_dictionary_file(self):
        """Create a new dictionary file."""
        file_name = self.entry_new_dictionary_file.get()
        if file_name:
            selected_language = self.dropdown_language_select.get()
            dictionaries_path = CH.get_variable_value(CKL.DICTIONARIES_PATH)
            try:
                DictionaryCreator.create(dictionaries_path, selected_language, file_name)
                self.file_tree_view.recreate_tree(dictionaries_path, expand_root_node=True)
            except InvalidFileNameError as e:
                buttons = [{"text": self.loc("ok"), "callback": lambda: None}]
                CustomPopupMessageBox(
                    self,
                    title=self.loc("invalid_input"),
                    message=f"{self.loc('invalid_characters')}{e.invalid_chars}",
                    buttons=buttons
                )

    def _on_delete_dictionary_file(self):
        """Delete the selected dictionary file."""
        selected_file = self.file_tree_view.get_selected_files()
        if selected_file and self._confirm_action(self.loc("confirm_del_dic_title"), self.loc("confirm_del_dic_msg")):
            file_path = next(iter(selected_file.values()))
            FileOps.delete_file(file_path)
            dir_name = FileOps.get_directory_name(file_path)
            if FileOps.is_directory_empty(dir_name):
                FileOps.delete_directory(dir_name)
            self.file_tree_view.recreate_tree(CH.get_variable_value(CKL.DICTIONARIES_PATH), expand_root_node=True)

    # Helper Methods
    def _create_popup_message_box(self, title, message, on_callback):
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

    def _confirm_action(self, title, message):
        """Confirm an action with a popup message box."""
        return self._create_popup_message_box(title, message, lambda is_confirmed: is_confirmed)
