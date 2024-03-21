# AutoDriveTranslationTool/src/components/dictionary_frame/dictionary_frame_logic.py

from GuiFramework.widgets import CustomPopupMessageBox

from GuiFramework.utilities import EventManager, FileOps, CtkHelper
from GuiFramework.utilities.config import ConfigHandler as CH
from GuiFramework.utilities.config.config_types import ConfigKeyList as CKL

from AutoDriveTranslationTool.src.core.constants import (
    EVENT_ON_SAVE_DICTIONARY_FILE, EVENT_ON_LOAD_DICTIONARY_FILE, EVENT_ON_CLEAR_DICTIONARY_EDIT_TEXTBOX,
    EVENT_ON_CREATE_DICTIONARY_FILE, EVENT_ON_DELETE_DICTIONARY_FILE
)

from AutoDriveTranslationTool.src.functions import DictionaryCreator
from AutoDriveTranslationTool.src.functions.exceptions import InvalidFileNameError


class DictionaryFrameLogic:
    """Initialize the dictionary frame logic components."""

    def __init__(self, app_instance, gui_instance) -> None:
        """Initialize the dictionary frame logic components."""
        self.app_instance = app_instance
        self.gui_instance = gui_instance

        self.localization_manager = self.app_instance.localization_manager
        self.loc = self.localization_manager.localize

        self.file_tree_view = self.gui_instance.file_tree_view
        self.custom_textbox_dictionary_edit_box = self.gui_instance.custom_textbox_dictionary_edit_box
        self.entry_new_dictionary_file = self.gui_instance.entry_new_dictionary_file
        self.dropdown_language_select = self.gui_instance.dropdown_language_select

        self._setup_event_handlers()

    def _setup_event_handlers(self) -> None:
        """Register event handlers for dictionary actions."""
        EventManager.subscribe(EVENT_ON_SAVE_DICTIONARY_FILE, self._on_save_dictionary_file)
        EventManager.subscribe(EVENT_ON_LOAD_DICTIONARY_FILE, self._on_load_dictionary_file)
        EventManager.subscribe(EVENT_ON_CLEAR_DICTIONARY_EDIT_TEXTBOX, self._on_clear_dictionary_edit_textbox)
        EventManager.subscribe(EVENT_ON_CREATE_DICTIONARY_FILE, self._on_create_dictionary_file)
        EventManager.subscribe(EVENT_ON_DELETE_DICTIONARY_FILE, self._on_delete_dictionary_file)

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
